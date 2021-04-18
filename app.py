from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app=Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
# init DB
db = SQLAlchemy(app)
# init ma
ma = Marshmallow(app)

# Product Class/Model

class Product(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(length=100),unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self,name,description,price,qty) -> None:
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

# Product Schema

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name','description','price','qty')

# Init Schema

product_schema = ProductSchema()
product_schema = ProductSchema(many = True)

@app.route('/product',methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name,description,price,qty)
    db.session.add(new_product)
    db.session.commit()

    # print(f"Product Schema ===========>: \n{}")
    result = product_schema.dump(new_product).data

    return jsonify(result)

# Get All Products
@app.route('/product',methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = product_schema.dump(all_products)
    return jsonify(result)



#Run Server
if __name__ == '__main__':
    app.run(debug=True)