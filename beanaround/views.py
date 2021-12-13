from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from datetime import datetime
from .forms import CheckoutForm
from .models import Product, Order
from random import randint


bp = Blueprint('main', __name__)

# Mock Database
product1 = Product('1', 'Coffee Beans', 'coffee', 'Aromatic Coffee', 'product1.jpg', 25.50)
product2 = Product('2', 'Other beans', 'coffee','Very delicious', 'product2.jpg', 55.25)

# machines
product3 = Product('3', 'The Expensive Machine', 'machine', 'You are better than everyone. Now prove it.', 'product3.jpg', 3000)

# accessories
product4 = Product('4', 'Le Expensive Grinder', 'accessory', "What you think you're better than me? Nah...You are better than everyone. No really.", 'product4.jpg', 1200)

products = [product1, product2, product3, product4]

coffee = []
machine = []
accessory = []

# Category Databases
for product in products:
    if product.category == 'coffee':
        coffee.append(product)
    if product.category == 'machine':
        machine.append(product)
    if product.category == 'accessory':
        accessory.append(product)

# Orders

order1 = Order('1', False, '', '','', datetime.now(), [product1,product2], product1.price+product2.price) # simulating order not checked out
order2 = Order('2', False, '', '','', datetime.now(), [product3], product3.price+product1.price) # simulating order not checked out

orders = [order1, order2]

# Routes

# generic page route
@bp.route('/')
def index():
    # generate three random products
    n_ran = 3
    prod_list = products.copy()
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
    categories = {0: 'Coffee Beans', 1: 'Machines', 2: 'Accessories'}
    title = categories[catID]
    if catID == 0:
        products = coffee
    if catID == 1:
        products = machine
    if catID == 2:
        products = accessory
    return render_template('category.html', header=str(title), products=products)

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
