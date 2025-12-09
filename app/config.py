import os
from dotenv import load_dotenv

load_dotenv()

# basedir = /home/bogdan/flask_app_pavliuk/app
basedir = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(basedir)  # один рівень вверх

class BaseConfig:
    SECRET_KEY = os.environ.get("qwerfdsazxcv", "dev-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    FLASK_DEBUG = 1
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL",
        "sqlite:///" + os.path.join(PROJECT_ROOT, "instance", "data.sqlite"),
    )


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


config_map = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig,
}
