from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine

Base = declarative_base()


class Fruit(Base):
    __tablename__ = 'fruits'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    keywords = relationship("Keyword", backref="fruit", lazy="dynamic")

class Keyword(Base):
    __tablename__ = "keywords"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fruit_id = Column(Integer, ForeignKey('fruits.id'))



cassava = Fruit(name='cassava')
kws = ['woody', 'shrub', 'spurge']
for keyword in kws:
    cassava.keywords.append(Keyword(name=keyword))
