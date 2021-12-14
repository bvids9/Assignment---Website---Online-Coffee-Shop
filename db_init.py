# SQL Data Base Initialisation

from beanaround import db, create_app

db.create_all(app=create_app())
