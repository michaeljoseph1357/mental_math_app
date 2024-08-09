from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap4  # Import Flask-Bootstrap

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    login_manager.init_app(app)
    
    # Initialize Flask-Bootstrap
    Bootstrap4(app)
    
    # Import routes inside the app context to avoid circular import issues
    with app.app_context():
        from . import routes, models
        db.create_all()
        
    return app
