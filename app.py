"""
A simple RESTful web application allowing clients to have basic
CRUD (create, read, update, delete) operations to track their
favorite fruits and the attributes thereof.
"""
# standard library imports
import sys
import os

# third party imports
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

# local imports
import util

app = Flask(__name__) # pylint: disable=invalid-name
api = Api(app) # pylint: disable=invalid-name

if app.config['TESTING']:
    url_key = 'TEST_DB_URL' # pylint: disable=invalid-name
else:
    url_key = 'LIVE_DB_URL' # pylint: disable=invalid-name

if not os.getenv(url_key):
    err = "{} not defined in environment, can't connect to database." # pylint: disable=invalid-name
    print(err.format(url_key))
    sys.exit(1)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(url_key)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # suppress warning

db = SQLAlchemy(app) # pylint: disable=invalid-name

# util.set_db(db.Model)

# Models
# class Fruit(db.Model): # pylint: disable=too-few-public-methods
#     """
#     Model for Fruit.
#     Each Fruit can have many Atrributes.
#     """
#     id = db.Column(db.Integer, primary_key=True) # pylint: disable=invalid-name
#     name = db.Column(db.String())
#     attributes = db.relationship('Attribute', backref='fruit')
#
#     def __repr__(self):
#         return "<Fruit: id={}, name={}>".format(self.id, self.name)
#
# class Attribute(db.Model): # pylint: disable=too-few-public-methods
#     """
#     Model for Attribute.
#     Each Fruit can have many Attributes.
#     """
#     id = db.Column(db.Integer, primary_key=True) # pylint: disable=invalid-name
#     name = db.Column(db.String())
#     fruit_id = db.Column(db.Integer, db.ForeignKey('fruit.id'))
#
#     def __repr__(self):
#         return "<Attribute: id={}, name={}>".format(self.id, self.name)
#
# if not all([x in db.engine.table_names() for x in ['fruit', 'attribute']]):
#     # create tables
#     db.create_all()

class HelloWorld(Resource):
    """
    A test resource.
    """
    def get(self): # pylint: disable=no-self-use
        """When HTTP GET method is used"""
        return {'hello': 'world'}

    def post(self): # pylint: disable=no-self-use
        """When HTTP POST method is used"""
        return {'goodbye': 'world'}

api.add_resource(HelloWorld, '/')

# import IPython;IPython.embed()


if __name__ == '__main__':
    # don't run me this way, do FLASK_APP=app.py FLASK_DEBUG=true flask run
    app.run(debug=True)
