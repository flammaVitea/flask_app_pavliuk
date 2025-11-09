from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=4, max=10)])
    remember = BooleanField("Запам’ятати мене")
    submit = SubmitField("Увійти")
