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
    # attach to carousel
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
def categorypage(catID):
    products = Product.query.filter(Product.category == catID).all()
    title = Category.query.filter(Category.id == catID).first()
    return render_template('category.html', header=str(title.name), products=products)

# product pages
@bp.route('/product/<productID>')
def productpage(productID):
    product = Product.query.filter(Product.id == productID).first()
    return render_template('product.html', product=product)

# Referred to as "Basket" to the user

@bp.route('/order', methods=['POST','GET'])
def order():
    product_id = request.values.get('product_id')

    # retrieve order if there is one
    if 'order_id'in session.keys():
        order = Order.query.get(session['order_id'])
        # order will be None if order_id stale
    else:
        # there is no order
        order = None

    # create new order if needed
    if order is None:
        order = Order(status = False, name='', email='', phone='', totalcost=0, date=datetime.now())
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('failed at creating a new order')
            order = None
    
    # calcultate totalprice
    totalprice = 0
    if order is not None:
        for product in order.products:
            totalprice = totalprice + product.price
    
    # are we adding an item?
    if product_id is not None and order is not None:
        product = Product.query.get(product_id)
        if product not in order.products:
            try:
                order.products.append(product)
                db.session.commit()
            except:
                return 'There was an issue adding the item to your basket'
            return redirect(url_for('main.order'))
        else:
            flash('item already in basket')
            return redirect(url_for('main.order'))
    
    return render_template('order.html', order = order, totalprice = totalprice)

@bp.route('/checkout/', methods=['POST', 'GET'])
def checkout():
    form = CheckoutForm()
    if 'order_id' in session:
        #retrieve correct order object     
        if form.validate_on_submit():
            order.status = True
            order.name = form.name.data
            order.email = form.email.data
            order.phone = form.phone.data
            order.address = form.address.data
            order.date = datetime.now()
            try:
                db.session.commit()
                del session['order_id']
                flash('Thank you! Your order will be shipped soon!')
                return redirect(url_for('main.index'))
            except:
                return('There was an issue completing your order.')
    return render_template('checkout.html', form = form)

@bp.route('/deleteorder')
def deleteorder():
    if 'order_id' in session: 
        del session['order_id']
    return redirect(url_for('main.index'))

@bp.route('/deleteorderitem', methods=['POST'])
def deleteorderitem():
    id=request.form['id']
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        item_to_delete = Product.query.get(id)
        try:
            order.products.remove(item_to_delete)
            db.session.commit()
            return redirect(url_for('main.order'))
        except:
            return 'Problem deleting item from order'
    return redirect(url_for('main.order'))


# Load Database function
@bp.route('/dbseed')
def dbseed():
    # Categories
    category1 = Category(name='Coffee Beans')
    category2 = Category(name='Machines')
    category3 = Category(name='Accessories')

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
    product4 = Product(name="Grind-o-Matic", image="product4.jpg",\
        price=350.75,\
        description="Experience luxury. No more hand grinding.", category=category3.id)

    try:
        db.session.add(product1)
        db.session.add(product2)
        db.session.add(product3)
        db.session.add(product4)
        db.session.commit()
    except:
        return 'There was an issue adding the products in the dbseed function.'
    
    return 'DATA LOADED'