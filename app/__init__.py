from flask import Flask
from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy
from pymysql.cursors import DictCursor

# Globally accessible libraries
db = SQLAlchemy()
mysql = MySQL(cursorclass=DictCursor)

def init_app():
    """Initialize the core application."""
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)
    mysql.init_app(app)

    with app.app_context():
        # Include our Routes
        import routes

        # Register Blueprints
        # app.register_blueprint(auth.auth_bp)
        # app.register_blueprint(admin.admin_bp)

        return app