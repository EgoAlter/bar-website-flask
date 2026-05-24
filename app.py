from flask import Flask, render_template
from data import venues

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", venues=venues)

@app.route("/menu/pink-lane")
def menu_pink_lane():
    return render_template("menu_pink_lane.html", venues=venues)

@app.route("/menu/dean-street")
def menu_dean_street():
    return render_template("menu_dean_street.html", venues=venues)

@app.route("/bottomless-brunch")
def bottomless_brunch():
    return render_template("bottomless_brunch.html", venues=venues)

@app.route("/private-hire")
def private_hire():
    return render_template("private_hire.html", venues=venues)

@app.route("/gallery")
def gallery():
    return render_template("gallery.html", venues=venues)

@app.route("/contact")
def contact():
    return render_template("contact.html", venues=venues)

@app.route("/gift-cards")
def gift_cards():
    return render_template("gift_cards.html", venues=venues)

@app.route("/book")
def book():
    return render_template("book.html", venues=venues)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)