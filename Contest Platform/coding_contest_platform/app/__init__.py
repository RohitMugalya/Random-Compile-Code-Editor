from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Create the Flask application
    app = Flask(__name__)

    # Load configuration based on the environment
    env = os.environ.get('FLASK_ENV') or 'development'
    app.config.from_object(f'instance.config.{env.capitalize()}Config')

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints (routes)
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Create database tables (if they don't exist)
    with app.app_context():
        db.create_all()

    return app