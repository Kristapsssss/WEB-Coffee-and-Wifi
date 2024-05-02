from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Select

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'

db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    map_url = db.Column(db.String(100))
    img_url = db.Column(db.String(100))
    location = db.Column(db.String(100))
    has_sockets = db.Column(db.Boolean)
    has_toilet = db.Column(db.Boolean)
    has_wifi = db.Column(db.Boolean)
    can_take_calls = db.Column(db.Boolean)
    seats = db.Column(db.Integer)
    coffee_price = db.Column(db.String(50))


def currency_convert(price):
    new_price = price.replace("$", "").replace("£", "").replace("€", "").replace(",", "")
    return float(new_price)


@app.route("/")
def home():
    cafes = Cafe.query.all()
    all_prices = [currency_convert(cafe.coffee_price) for cafe in cafes]
    lowest_price = float(min(all_prices))
    highest_price = float(max(all_prices))
    print((3-lowest_price) / (highest_price - lowest_price) * 100)
    return render_template('index.html',
                           cafes=cafes,
                           lowest_price=lowest_price,
                           highest_price=highest_price,
                           currency_convert=currency_convert)


if __name__ == '__main__':
    app.run(debug=True)