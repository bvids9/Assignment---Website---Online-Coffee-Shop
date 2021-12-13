#import flask - from the package import class
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()
app= Flask(__name__)

#create a function that creates a web application
# a web server will run this web application
def create_app():
    app.debug=True
    app.secret_key="Thisissecret"

    # set configuration data
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///coffee.sqlite'

    # initialise database
    db.init_app(app)

    bootstrap = Bootstrap(app)

    #importing modules here to avoid circular references, register blueprints of routes
    from . import views
    app.register_blueprint(views.bp)
    return app

@app.errorhandler(404)
# error page
def not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
# error page
def internal_error(e):
    return render_template("404.html")