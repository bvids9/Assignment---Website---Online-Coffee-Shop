from datetime import datetime
from . import db

class Product:
    def __init__(self, id, name, category, description, image, price):
        self.id = id
        self.name = name
        self.category = category
        self.description = description
        self.image = image
        self.price = price

    def get_product_details(self):
        return str(self)
    
    def __repr__(self):
        str = f"ID: {self.id}, Name: {self.name}, Category: {self.category}, Description: {self.description}, Image: {self.image}, Price: {self.price} \n"
        return str

class Order:
    def __init__(self, id, status, name, email, phone, date, products, total_cost):
        self.id = id
        self.status = status
        self.name = name
        self.email = email
        self.phone = phone
        self.date = date
        self.products = products
        self.total_cost = total_cost

    def __repr__(self):
        str = (f"ID: {self.id}, Status: {self.status}, Name: {self.name}, E-mail: {self.email}, Phone: {self.phone}, Date: {self.date}, Products: {self.product}, Total Cost: {self.total_cost} \n")
        return str
