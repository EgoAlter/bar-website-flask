from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from dotenv import load_dotenv
from data import venues, menu
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'madhouse-dev-key'

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///madhouse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mail config
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'

db = SQLAlchemy(app)
mail = Mail(app)

# --- Models ---

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    venue = db.Column(db.String(50), nullable=False)
    available = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<MenuItem {self.name}>'

# --- Routes ---

@app.route("/")
def home():
    return render_template("index.html", venues=venues)

@app.route("/menu/pink-lane")
def menu_pink_lane():
    items = MenuItem.query.filter_by(venue='pink_lane', available=True).all()
    categories = sorted(set(item.category for item in items))
    return render_template("menu_pink_lane.html", venues=venues, items=items, categories=categories)

@app.route("/menu/dean-street")
def menu_dean_street():
    items = MenuItem.query.filter_by(venue='dean_street', available=True).all()
    categories = sorted(set(item.category for item in items))
    return render_template("menu_dean_street.html", venues=venues, items=items, categories=categories)

@app.route("/bottomless-brunch")
def bottomless_brunch():
    items = MenuItem.query.filter_by(venue='dean_street', category='bottomless_brunch', available=True).all()
    return render_template("bottomless_brunch.html", venues=venues, items=items)

@app.route("/private-hire")
def private_hire():
    return render_template("private_hire.html", venues=venues)

@app.route("/gallery")
def gallery():
    img_folder = os.path.join(app.static_folder, 'img/gallery')
    images = [f for f in os.listdir(img_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    images.sort()
    return render_template("gallery.html", venues=venues, images=images)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        msg = Message(
            subject=f"Mad House enquiry from {name}",
            sender=os.getenv('MAIL_USERNAME'),
            recipients=["test@madhouse.dev"],
            body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        )
        mail.send(msg)
        flash("Message sent! We'll be in touch soon.", "success")
        return redirect(url_for('contact'))
    return render_template("contact.html", venues=venues)

@app.route("/gift-cards")
def gift_cards():
    return render_template("gift_cards.html", venues=venues)

@app.route("/book")
def book():
    return render_template("book.html", venues=venues)

# --- Admin auth decorator ---

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Admin routes ---

@app.route("/admin")
def admin():
    return redirect(url_for('admin_dashboard'))

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == os.getenv('ADMIN_PASSWORD'):
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        flash("Incorrect password.", "danger")
    return render_template("admin/login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    items = MenuItem.query.order_by(MenuItem.venue, MenuItem.category).all()
    return render_template("admin/dashboard.html", items=items)

@app.route("/admin/menu/add", methods=["GET", "POST"])
@admin_required
def admin_add():
    if request.method == "POST":
        item = MenuItem(
            name=request.form.get("name"),
            description=request.form.get("description"),
            price=float(request.form.get("price")),
            category=request.form.get("category"),
            venue=request.form.get("venue"),
            available=True
        )
        db.session.add(item)
        db.session.commit()
        flash(f"'{item.name}' added successfully.", "success")
        return redirect(url_for('admin_dashboard'))
    return render_template("admin/add.html")

@app.route("/admin/menu/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def admin_edit(id):
    item = MenuItem.query.get_or_404(id)
    if request.method == "POST":
        item.name = request.form.get("name")
        item.description = request.form.get("description")
        item.price = float(request.form.get("price"))
        item.category = request.form.get("category")
        item.venue = request.form.get("venue")
        db.session.commit()
        flash(f"'{item.name}' updated successfully.", "success")
        return redirect(url_for('admin_dashboard'))
    return render_template("admin/edit.html", item=item)

@app.route("/admin/menu/toggle/<int:id>")
@admin_required
def admin_toggle(id):
    item = MenuItem.query.get_or_404(id)
    item.available = not item.available
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route("/admin/menu/delete/<int:id>", methods=["POST"])
@admin_required
def admin_delete(id):
    item = MenuItem.query.get_or_404(id)
    db.session.commit()
    db.session.delete(item)
    db.session.commit()
    flash(f"'{item.name}' deleted.", "warning")
    return redirect(url_for('admin_dashboard'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)