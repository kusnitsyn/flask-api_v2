from flask import Flask, request, Response, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://python:python@db_ip/python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


#Creating model table for our CRUD database
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    arrival_date = db.Column(db.String, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    price = db.Column(db.String(80), nullable=False)

    def __init__(self, name, arrival_date, category, country, price):
        self.name = name.strip()
        self.arrival_date = arrival_date.strip()
        self.category = category.strip()
        self.country = country.strip()
        self.price = price.strip()


db.create_all()


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Products
        load_instance = True
        sqla_session = db.session


products = Products.query.all()
product_schema = ProductSchema()


#This is the main route with all products data
@app.route('/', methods=['GET'])
def api_main():
    json_data = request.get_json()
    if not json_data:
        return render_template('main.html', products=Products.query.all())



@app.route('/json')
def json_info():
    output = product_schema.dumps(products, many=True)
    return output


#this route is for inserting data to postgres database via html forms
@app.route('/add_product', methods=['POST'])
def api_write():
    name = request.form['name']
    arrival_date = request.form['arrival_date']
    category = request.form['category']
    country = request.form['country']
    price = request.form['price']

    db.session.add(Products(name, arrival_date, category, country, price))
    db.session.commit()

    return redirect(url_for('api_main'))


@app.route('/json_add', methods=['POST'])
def json_add():
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    else:
        name = request.json.get('name', '')
        arrival_date = request.json.get('arrival_date', '')
        category = request.json.get('category', '')
        country = request.json.get('country', '')
        price = request.json.get('price', '')

        new_product = Products(name=name, arrival_date=arrival_date, category=category, country=country, price=price)

        db.session.add(new_product)
        db.session.commit()
        return product_schema.jsonify(new_product)


#this is update products route
@app.route('/update', methods = ['GET', 'POST'])
def api_update():
    row = Products.query.get(request.form.get('id'))
    row.name = request.form['name']
    row.arrival_date = request.form['arrival_date']
    row.category = request.form['category']
    row.country = request.form['country']
    row.price = request.form['price']

    db.session.commit()

    return redirect(url_for('api_main'))


@app.route('/json_update/<id>/', methods=['PUT'])
def json_update(id):
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    else:
        name = request.json.get('name', '')
        arrival_date = request.json.get('arrival_date', '')
        category = request.json.get('category', '')
        country = request.json.get('country', '')
        price = request.json.get('price', '')

        product = Products.query.get(id)

        product.name = name
        product.arrival_date = arrival_date
        product.category = category
        product.country = country
        product.price = price

        db.session.add(product)
        db.session.commit()

        return product_schema.jsonify(product)


#This route is for deleting products
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    product = Products.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('api_main'))


@app.route('/json_delete/<id>/', methods=['DELETE'])
def json_delete(id):
    json_data = request.get_json()
    product = Products.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
