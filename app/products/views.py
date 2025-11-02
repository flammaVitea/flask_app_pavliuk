from flask import render_template
from . import products_bp

# Словник з продуктами та їх цінами
products = {
    'apple': 25,
    'banana': 40,
    'milk': 55,
    'bread': 30
}

@products_bp.route('/product/<string:name>')
def product(name):
    name = name.lower()
    price = products.get(name)
    return render_template('products.html', name=name, price=price)
