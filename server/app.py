#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, abort
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakery_list = [bakery.to_dict() for bakery in bakeries]
    return make_response(jsonify(bakery_list), 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = db.session.get(Bakery, id)
    if not bakery:
        abort(404)
    bakery_dict = bakery.to_dict()
    bakery_dict["baked_goods"] = [bg.to_dict() for bg in bakery.baked_goods]
    return make_response(jsonify(bakery_dict), 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = [bg.to_dict() for bg in baked_goods]
    return make_response(jsonify(baked_goods_list), 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return make_response(jsonify(most_expensive.to_dict()), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)


