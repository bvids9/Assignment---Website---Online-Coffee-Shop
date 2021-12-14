from datetime import datetime
from . import db

class Product(db.Model):
    __tablename__='products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(64), db.ForeignKey('categories.id'))

    def __repr__(self):
        str = f"ID: {self.id}, Name: {self.name}, Category: {self.category}, Description: {self.description}, Image: {self.image}, Price: {self.price} \n"
        return str

orderdetails = db.Table('orderdetails',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), nullable=False),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), nullable=False),
    db.PrimaryKeyConstraint('order_id', 'product_id'))

class Category(db.Model):
    __tablename__='categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)


class Order(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer, primary_key=True)
    status= db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    address = db.Column(db.String(128))
    totalcost = db.Column(db.Float)
    date = db.Column(db.DateTime)
    products = db.relationship("Product", secondary=orderdetails, backref="orders")

    def __repr__(self):
        str = (f"ID: {self.id}, Status: {self.status}, Name: {self.name}, E-mail: {self.email}, Phone: {self.phone}, Address: {self.address} Date: {self.date}, Products: {self.product}, Total Cost: {self.totalcost} \n")
        return str

