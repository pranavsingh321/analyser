import os
from flask import Flask
from core.api import api
from core.models import db
from config import configs


def create_app(config='config.ProductionConfig'):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config.from_envvar('FLASK_APP_SETTINGS', silent=True)
    app.register_blueprint(api)
    db.init_app(app)
    return app


if __name__ == '__main__':
    """
    Main entry point of the program.
    """
    env = os.environ.get('FLASK_APP_ENV', 'default')
    app = create_app(config=configs[env])
    app.run()
