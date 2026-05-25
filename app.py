from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv
from data import venues, menu
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'madhouse-dev-key'

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'

mail = Mail(app)

@app.route("/")
def home():
    return render_template("index.html", venues=venues)

@app.route("/menu/pink-lane")
def menu_pink_lane():
    return render_template("menu_pink_lane.html", venues=venues, menu=menu["pink_lane"])

@app.route("/menu/dean-street")
def menu_dean_street():
    return render_template("menu_dean_street.html", venues=venues, menu=menu["dean_street"])

@app.route("/bottomless-brunch")
def bottomless_brunch():
    return render_template("bottomless_brunch.html", venues=venues, menu=menu)

@app.route("/private-hire")
def private_hire():
    return render_template("private_hire.html", venues=venues)

@app.route("/gallery")
def gallery():
    return render_template("gallery.html", venues=venues)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)