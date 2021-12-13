from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from datetime import datetime
from .forms import CheckoutForm
from .models import Product, Order, Category
from random import randint
from . import db


bp = Blueprint('main', __name__)
# Routes

# generic page route
@bp.route('/')
def index():
    # generate three random products
    prod_list = Product.query.order_by(Product.id).all()
    print(prod_list)
    carousel_prod = []
    i = 0

    while i != 3:
        x = randint(0, len(prod_list)-1)
        carousel_prod.append(prod_list.pop(x))
        i += 1
    return render_template('index.html', display_products = carousel_prod)

@bp.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@bp.route('/contact')
def contact():
    return render_template('contact.html')

# category page routes
# extends show function
@bp.route('/category/<int:catID>')
def category(catID):
    products = Product.query.filter(Product.category == catID).all()
    title = Category.query.filter(Category.id == catID).first()
    print(title.name)
    print(products)
    return render_template('category.html', header=str(title.name), products=products)

# product pages
@bp.route('/product/<productID>')
def product(productID):
    #item = product1
    item = None
    for product in products:
        if productID == (product.id):
            selected_item = product
    return render_template('product.html', item=selected_item)

@bp.route('/order/', methods=['POST', 'GET'])
def order():
    # check if new order
    if 'order_id' not in session:
        session['order_id'] = 1

    # retrieve order object
    for x in orders:
        if int(x.id) == int(session['order_id']):
            order = x
    return render_template('order.html', order=order, totalprice = order.total_cost)


@bp.route('/checkout/', methods=['POST', 'GET'])
def checkout():
    form = CheckoutForm()
    if 'order_id' in session:
        #retrieve correct order object
        for x in orders:
                if int(x.id) == int(session['order_id']): 
                    order = x
       
        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.email = form.email.data
            order.phone = form.phone.data
            print(order)
            flash('Thank you! Your order will be shipped soon!')
    return render_template('checkout.html', form = form)

@bp.route('/deleteorder')
def deleteorder():
    if 'order_id' in session: 
        del session['order_id']
    return redirect(url_for('main.index'))

@bp.route('/deleteorderitem', methods=['POST'])
def deleteorderitem():
    print('User wants to delete item with id={}'.format(request.form['id']))
    return redirect(url_for('main.index'))


# Load Database function
@bp.route('/dbseed')
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