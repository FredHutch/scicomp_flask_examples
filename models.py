# from sqlalchemy import Column, String, Integer, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
# # from sqlalchemy import create_engine
#
# Base = declarative_base()

from app import db


class Fruit(db.Model): # pylint: disable=too-few-public-methods
    """
    Model for Fruit.
    Each Fruit can have many Atrributes.
    """
    id = db.Column(db.Integer, primary_key=True) # pylint: disable=invalid-name
    name = db.Column(db.String())
    attributes = db.relationship('Attribute', backref='fruit')

    def __repr__(self):
        return "<Fruit: id={}, name={}>".format(self.id, self.name)

class Attribute(db.Model): # pylint: disable=too-few-public-methods
    """
    Model for Attribute.
    Each Fruit can have many Attributes.
    """
    id = db.Column(db.Integer, primary_key=True) # pylint: disable=invalid-name
    name = db.Column(db.String())
    fruit_id = db.Column(db.Integer, db.ForeignKey('fruit.id'))

    def __repr__(self):
        return "<Attribute: id={}, name={}>".format(self.id, self.name)

if not all([x in db.engine.table_names() for x in ['fruit', 'attribute']]):
    # create tables
    db.create_all()
