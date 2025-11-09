from flask import Blueprint, render_template, flash, redirect, url_for
from app.forms import ContactForm
from loguru import logger

main_bp = Blueprint("main_bp", __name__)


# Налаштовуємо логування
logger.add("logs/contact.log", format="{time} {level} {message}", level="INFO", rotation="1 MB")

@main_bp.route("/")
def main():
    return render_template("base.html")

@main_bp.route("/resume")
def resume():
    return render_template("resume.html")

@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        logger.info(
            f"New message from {form.name.data} ({form.email.data}, {form.phone.data}) | Subject: {form.subject.data} | Message: {form.message.data}"
        )
        flash(f"Дякуємо, {form.name.data}! Повідомлення успішно надіслано.", "success")
        return redirect(url_for("main_bp.contact"))
    elif form.is_submitted() and not form.validate():
        flash("Будь ласка, виправте помилки у формі.", "danger")
    return render_template("contacts.html", form=form)
