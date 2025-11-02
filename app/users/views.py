from flask import request, render_template, url_for, redirect
from . import users_bp

@users_bp.route('/hi/<string:name>')
def hi(name):
    name = name.upper()
    age = request.args.get('age', None, int)

    return render_template('hi.html', name=name, age=age)

@users_bp.route('/admin')
def admin():
    to_url = url_for('users.hi', name='administrator', age=30, _external=True)
    return redirect(to_url)

