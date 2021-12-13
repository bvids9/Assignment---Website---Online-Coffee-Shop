from flask import Blueprint
from . import db
from .models import Product, Category, Order
import datetime

bp = Blueprint('admin', __name__, url_prefix='/admin/')

@bp.route('/dbseed/')
def dbseed():
    # Categories
    category1 = Category(name='coffee')
    category2 = Category(name='machine')
    category3 = Category(name='accessory')

    try:
        db.session.add(category1)
        db.session.add(category2)
        db.session.add(category3)
        db.session.commit()
    except:
        return 'There was an issue adding the categories in the dbseed function.'
    # Products
    product1 = Product(name="Great Coffee", image="product1.jpg", \
        price = 25.50, \
        description= "Really awesome coffee.", category=category1.id)
    product2 = Product(name="Really Expensive Coffee", image="product2.jpg",\
        price=450.75,\
        description= "Too rich for most. Prove them wrong.", category=category1.id)
    product3 = Product(name="Breville Grinder", image="product3.jpg",\
        price=1300.45,\
        description= "Can grind and make just about anything into coffee.", category=category2.id)

    try:
        db.session.add(product1)
        db.session.add(product2)
        db.session.add(product3)
        db.session.commit()
    except:
        return 'There was an issue adding the products in the dbseed function.'
    
    return 'DATA LOADED'