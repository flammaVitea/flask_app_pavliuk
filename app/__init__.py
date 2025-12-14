import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase  # <--- Додано імпорт
from .config import config_map

# 1. Створюємо клас Base з налаштуванням іменування (Naming Convention)
class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

# 2. Ініціалізуємо SQLAlchemy з використанням нашого класу Base
db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'dev')

    app = Flask(__name__, instance_relative_config=True)
    
    config_class = config_map.get(config_name, config_map['dev'])
    app.config.from_object(config_class)

    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    db.init_app(app)
    migrate.init_app(app, db)

    from app.users import users_bp
    from app.products import products_bp
    from app.views import main_bp
    from app.posts import post_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(post_bp, url_prefix='/post')
    
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404
    
    return app