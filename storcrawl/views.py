"""
See
https://docs.google.com/document/d/1IvzWOgbeQDLxkTlWX0bg2lcQBmxvba8mAaZgy0Ymxck/edit#
"""

from flask.blueprints import Blueprint


import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.types
import sqlalchemy.ext.declarative
import sqlalchemy.dialects.postgresql

# from database import db

from models import FileMetadata, UidMapping

main_blueprint = Blueprint('main_blueprint', __name__,
                 template_folder='templates',
                 static_folder='static')

Base = sqlalchemy.ext.declarative.declarative_base()

@main_blueprint.route('/')
def test():
    thing = FileMetadata.query.first()
    return str(thing.mtime)
  # user = User.query.filter_by(username="Tom").first()
  # return "Test: Username %s " % user.username
