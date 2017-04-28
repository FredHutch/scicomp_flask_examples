"""
Create app here, using application factory pattern.
"""
import os
import os.path
import sys

from flask import Flask

from database import db
from views import main_blueprint


def create_app():
    """
    Helper method to create app. Means that app can be used both
    by the web app and the command line (see autoapp.py).
    """
    app = Flask(__name__)
    app.config['DEBUG'] = True
    url = os.getenv("STORCRAWL_DB_URL")
    if not url:
        print("Can't run! Define STORCRAWL_DB_URL in the environment.")
        sys.exit(1)
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    # Comment this out if you don't want to see SQL queries emitted:
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # suppress warning
    db.init_app(app)
    app.register_blueprint(main_blueprint, url_prefix='')
    return app

if __name__ == '__main__':
    """
    Run me like this:
    FLASK_DEBUG=True python app.py
    """
    APP = create_app()
    APP.run()
