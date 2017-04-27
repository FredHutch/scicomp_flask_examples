import os
import sys

from database import db
from flask import Flask
import os.path
from views import FileMetadata
from views import UidMapping
from views import main_blueprint


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    url = os.getenv("STORCRAWL_DB_URL")
    if not url:
        print("Can't run! Define STORCRAWL_DB_URL in the environment.")
        sys.exit(1)
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # suppress warning
    db.init_app(app)
    app.register_blueprint(main_blueprint, url_prefix='')
    return app


def setup_database(app):
    pass
    # with app.app_context():
    #     db.create_all()
    # user = User()
    # user.username = "Tom"
    # db.session.add(user)
    # db.session.commit()


if __name__ == '__main__':
    app = create_app()
    # import IPython;IPython.embed()
    #Because this is just a demostration we set up the database like this.
    # if not os.path.isfile('/tmp/test.db'):
    #   setup_database(app)
    app.run()
