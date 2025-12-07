import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .config import config_map

from app.users import users_bp
from app.products import products_bp
from app.views import main_bp
from app.posts import post_bp

# Extensions (initialized in factory)
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name: str | None = None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'development')

    config_class = config_map.get(config_name, config_map['development'])

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except Exception:
        pass

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(post_bp)

    # 404 handler
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    return app

app = create_app(os.environ.get('FLASK_CONFIG', 'development'))
