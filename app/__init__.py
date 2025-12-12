import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import config_map

# 1. Ініціалізація розширень глобально (щоб їх могли імпортувати моделі)
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    # Визначення конфігурації
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'dev')

    app = Flask(__name__, instance_relative_config=True)
    
    # Завантаження налаштувань
    config_class = config_map.get(config_name, config_map['dev'])
    app.config.from_object(config_class)

    # Створення папки instance, якщо немає
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # 2. Ініціалізація розширень з додатком
    db.init_app(app)
    migrate.init_app(app, db)

    # 3. Імпорт та реєстрація блюпринтів
    # Імпортуємо ТУТ, щоб уникнути циклічних імпортів (Circular Import),
    # оскільки модулі блюпринтів можуть імпортувати 'db' з цього файлу.
    from app.users import users_bp
    from app.products import products_bp
    from app.views import main_bp
    from app.posts import post_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(post_bp, url_prefix='/post')
    
    # Обробник помилок
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404
    
    return app