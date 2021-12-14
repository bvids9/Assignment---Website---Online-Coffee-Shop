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
    db.Column('order_id', db.Integer, db.ForeignKey('orderitems.id'), nullable=False),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), nullable=False),
    db.PrimaryKeyConstraint('order_id', 'product_id'))

'''''''''''''''''
class OrderItem(db.Model):
    __tablename__="orderitems"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column('product_id', db.Integer, db.ForeignKey('products.id'), nullable=False)
    products = db.relationship("Product", secondary=orderdetails, backref="orderitems")
    quantity= db.Column(db.Integer, nullable=False)
'''''''''''''''''

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
    totalcost = db.Column(db.Float)
    date = db.Column(db.DateTime)
    orderitems = db.relationship("OrderItem", backref='orders', uselist=True)

    def __repr__(self):
        str = (f"ID: {self.id}, Status: {self.status}, Name: {self.name}, E-mail: {self.email}, Phone: {self.phone}, Date: {self.date}, OrdersItems: {self.orderitems}, Total Cost: {self.totalcost} \n")
        return str