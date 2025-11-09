from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp

class ContactForm(FlaskForm):
    name = StringField(
        "Ім’я",
        validators=[DataRequired(message="Поле обов'язкове"), Length(min=4, max=10)],
        render_kw={"placeholder": "Введіть ваше ім'я (4-10 символів)"}
    )
    email = StringField(
        "Email",
        validators=[DataRequired(message="Поле обов'язкове"), Email(message="Невірний формат email")],
        render_kw={"placeholder": "Введіть ваш email"}
    )
    
    phone = StringField(
        "Телефон",
        validators=[
            DataRequired(message="Поле обов'язкове"),
            Regexp(r'^\+380\d{9}$', message="Формат: +380*********")
        ],
        render_kw={"placeholder": "+380*********"}
    )
    subject = SelectField(
        "Тема",
        choices=[("support", "Підтримка"), ("sales", "Продаж"), ("other", "Інше")],
        validators=[DataRequired(message="Оберіть тему")]
    )
    message = TextAreaField(
        "Повідомлення",
        validators=[DataRequired(message="Поле обов'язкове"), Length(max=500)],
        render_kw={"placeholder": "Напишіть повідомлення (до 500 символів)", "rows": 4}
    )
    submit = SubmitField("Надіслати")
