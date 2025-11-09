from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from . import users_bp
from app.users.forms import LoginForm

# Тестові дані для входу
VALID_USERNAME = "admin"
VALID_PASSWORD = "1234"


@users_bp.route('/hi/<string:name>')
def hi(name):
    name = name.upper()
    age = request.args.get('age', type=int)
    return render_template('hi.html', name=name, age=age)


@users_bp.route('/admin')
def admin():
    to_url = url_for('users_bp.hi', name='administrator', age=30, _external=True)
    return redirect(to_url)


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["username"] = username
            flash_msg = f"Вхід успішний! Користувач: {username}."
            if remember:
                flash_msg += " Опція 'Запам’ятати мене' активована."
            flash(flash_msg, "success")
            return redirect(url_for("users_bp.profile"))
        else:
            flash("Невірні дані входу!", "danger")
            return redirect(url_for("users_bp.login"))
    
    return render_template("login.html", form=form)


@users_bp.route("/profile")
def profile():
    username = session.get("username")
    if not username:
        flash("Будь ласка, увійдіть у систему!", "warning")
        return redirect(url_for("users_bp.login"))

    cookies = request.cookies
    color = cookies.get("color_scheme", "light")

    return render_template("profile.html", username=username, cookies=cookies, color=color)


@users_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Ви вийшли із системи!", "info")
    return redirect(url_for("users_bp.login"))


@users_bp.route("/add_cookie", methods=["POST"])
def add_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть!", "warning")
        return redirect(url_for("users_bp.login"))

    key = request.form.get("key")
    value = request.form.get("value")
    resp = make_response(redirect(url_for("users_bp.profile")))

    if key and value:
        resp.set_cookie(key, value)
        flash(f"Кукі '{key}' додано!", "success")
    else:
        flash("Введіть ключ і значення!", "danger")

    return resp


@users_bp.route("/delete_cookie", methods=["POST"])
def delete_cookie():
    key = request.form.get("key")
    resp = make_response(redirect(url_for("users_bp.profile")))

    if key:
        resp.delete_cookie(key)
        flash(f"Кукі '{key}' видалено!", "info")
    else:
        for k in request.cookies:
            resp.delete_cookie(k)
        flash("Усі кукі видалено!", "info")

    return resp


@users_bp.route("/set_color/<scheme>")
def set_color(scheme):
    resp = make_response(redirect(url_for("users_bp.profile")))
    resp.set_cookie("color_scheme", scheme)
    flash(f"Колірну схему змінено на {scheme}", "success")
    return resp