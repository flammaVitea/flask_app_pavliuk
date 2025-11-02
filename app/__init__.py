from flask import Flask
from app.users import users_bp 
from app.products import products_bp

app = Flask(__name__)
app.config.from_pyfile('../config.py')

from . import views


app.register_blueprint(users_bp)
app.register_blueprint(products_bp)