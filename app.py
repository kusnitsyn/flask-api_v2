from flask import Flask, request, Response, json, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://python:python@localhost/python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Creating model table for our CRUD database
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    arrival_date = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, name, arrival_date, category, country, price):
        self.name = name.strip()
        self.arrival_date = arrival_date.strip()
        self.category = category.strip()
        self.country = country.strip()
        self.price = price.strip()

db.create_all()


#This is Just for test :)
#@app.route('/', methods=['GET'])
#def hello_world():
#    return render_template('index.html')


#This is the main route with all products data
@app.route('/', methods=['GET'])
def api_main():
    return render_template('main.html', products=Products.query.all())


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

#this is update products route
@app.route('/update', methods = ['GET', 'POST'])
def api_update():
    if request.method == 'POST':
        product = Products.query.get(request.form.get('id'))

        product.name = request.form['name']
        product.arrival_date = request.form['arrival_date']
        product.category = request.form['category']
        product.country = request.form['country']
        product.price = request.form['price']

        db.session.commit()

        return redirect(url_for('api_main'))


#This route is for deleting products
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    product = Products.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('api_main'))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
