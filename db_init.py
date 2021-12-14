# SQL Data Base Initialisation
# Initialise a fresh database after deleting previous.

from beanaround import db, create_app

db.create_all(app=create_app())
