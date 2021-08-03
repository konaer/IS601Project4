from os import environ

"""Flask configuration."""

class Config:
    """Set Flask config variables."""
    MYSQL_DATABASE_HOST = 'db'
    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_PASSWORD = 'root'
    MYSQL_DATABASE_PORT = 3306
    MYSQL_DATABASE_DB = 'oscarData'

    SECRET_KEY = "IHUGVFIYUJYIGUibt6gh"
    FLASK_APP = "development"
    FLASK_ENV = "app.py"

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False