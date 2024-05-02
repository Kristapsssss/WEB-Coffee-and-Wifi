from flask import Flask, render_template, request, redirect, url_for
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
    try:
        all_prices = [currency_convert(cafe.coffee_price) for cafe in cafes]
        lowest_price = float(min(all_prices))
        highest_price = float(max(all_prices))
        percentages = [100 - ((currency_convert(cafe.coffee_price) - lowest_price) / (highest_price - lowest_price) * 100)
                       for cafe in cafes]
    except:
        lowest_price = 0
        highest_price = 0
        percentages = []
    return render_template('index.html',
                           cafes=cafes,
                           lowest_price=lowest_price,
                           highest_price=highest_price,
                           currency_convert=currency_convert,
                           percentages=percentages)


# Handle API requests towards DB file
@app.route("/api/cafe/<int:cafe_id>", methods=['GET'])
def get_cafe(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)
    cafe_json = {'id': cafe.id,
                 'name': cafe.name,
                 'map_url': cafe.map_url,
                 'img_url': cafe.img_url,
                 'location': cafe.location,
                 'has_sockets': cafe.has_sockets,
                 'has_toilet': cafe.has_toilet,
                 'has_wifi': cafe.has_wifi,
                 'can_take_calls': cafe.can_take_calls,
                 'seats': cafe.seats,
                 'coffee_price': cafe.coffee_price}
    return cafe_json


@app.route('/update_cafe', methods=['POST'])
def update_cafe():
    cafe_id = request.form['selectedCafeId']
    cafe = Cafe.query.get(cafe_id)
    if cafe:
        cafe.name = request.form['editCafeName']
        cafe.location = request.form['editCafeLocation']
        cafe.map_url = request.form['editCafeMap_url']
        cafe.img_url = request.form['editCafeImg_url']
        if request.form.get('editCafeHas_Sockets'):
            cafe.has_sockets = True
        else:
            cafe.has_sockets = False
        if request.form.get('editCafeHas_Toilet'):
            cafe.has_toilet = True
        else:
            cafe.has_toilet = False
        if request.form.get('editCafeHas_Wifi'):
            cafe.has_wifi = True
        else:
            cafe.has_wifi = False
        if request.form.get('editCafeCanTakeCalls'):
            cafe.can_take_calls = True
        else:
            cafe.can_take_calls = False
        cafe.seats = request.form['editCafeSeats']
        cafe.coffee_price = request.form['editCafeCoffeePrice']

        db.session.commit()
    return redirect(url_for('home'))


@app.route("/delete_cafe/<int:cafe_id>", methods=["GET"])
def delete_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/new_cafe', methods=['POST'])
def add_cafe():
    if request.form.get('CafeHas_Sockets'):
        has_sockets = True
    else:
        has_sockets = False
    if request.form.get('CafeHas_Toilet'):
        has_toilet = True
    else:
        has_toilet = False
    if request.form.get('CafeHas_Wifi'):
        has_wifi = True
    else:
        has_wifi = False
    if request.form.get('CafeCanTakeCalls'):
        can_take_calls = True
    else:
        can_take_calls = False
    cafe = Cafe(name=request.form['CafeName'],
                location=request.form['CafeLocation'],
                map_url=request.form['CafeMap_url'],
                img_url=request.form['CafeImg_url'],
                has_sockets=has_sockets,
                has_toilet=has_toilet,
                has_wifi=has_wifi,
                can_take_calls=can_take_calls,
                seats=request.form['CafeSeats'],
                coffee_price=request.form['CafeCoffeePrice'])
    db.session.add(cafe)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)