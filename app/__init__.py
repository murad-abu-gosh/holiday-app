from flask import Flask

from app.config import Config
from app.repository.database import Database

db = None


def create_app():
    app = Flask(__name__, template_folder='./templates', static_folder='./static')
    app.config.from_object(Config)
    # Initialize database
    global db
    db = Database(app.config['MONGO_URI'], app.config['MONGO_DB_NAME'])

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    # clear database
    # db.db.holidays.delete_many({})

    return app
