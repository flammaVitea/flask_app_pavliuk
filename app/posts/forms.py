from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField, DateTimeLocalField
from wtforms.validators import DataRequired, Length
from datetime import datetime

class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(min=2, max=150)])
    content = TextAreaField('Текст посту', validators=[DataRequired()])
    is_active = BooleanField('Активний пост', default=True)
    publish_date = DateTimeLocalField('Дата публікації', format='%Y-%m-%dT%H:%M', default=datetime.utcnow)
    
    category = SelectField('Категорія', choices=[
        ('news', 'Новини'),
        ('publication', 'Публікація'),
        ('tech', 'Технології'),
        ('other', 'Інше')
    ], validators=[DataRequired()])
    
    # Додаємо поле вибору автора. coerce=int обов'язково, бо value буде ID (число)
    author_id = SelectField('Автор', coerce=int, validators=[DataRequired()])
    
    submit = SubmitField('Зберегти')