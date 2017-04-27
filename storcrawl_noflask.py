"""
See
https://docs.google.com/document/d/1IvzWOgbeQDLxkTlWX0bg2lcQBmxvba8mAaZgy0Ymxck/edit#
"""

import os
import sys

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.types
import sqlalchemy.ext.declarative
import sqlalchemy.dialects.postgresql

Base = sqlalchemy.ext.declarative.declarative_base()

class FileMetadata(Base):
    __tablename__ = "file_metadata"
    # only listing the columns we care about...
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    owner = sqlalchemy.Column(sqlalchemy.String)
    uid = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    filename = sqlalchemy.Column(sqlalchemy.String)
    count = sqlalchemy.Column(sqlalchemy.Integer)
    mtime = sqlalchemy.Column(sqlalchemy.dialects.postgresql.DOUBLE_PRECISION)
    sum = sqlalchemy.Column(sqlalchemy.dialects.postgresql.DOUBLE_PRECISION)

class UidMapping(Base):
    __tablename__ = "uid_mapping"
    # composite key, which is also the only columns we care about....
    name = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    uid = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    homedir = sqlalchemy.Column(sqlalchemy.String, primary_key=True)

url = os.getenv("STORCRAWL_DB_URL")
if not url:
    print("Can't run! Define STORCRAWL_DB_URL in the environment.")
    sys.exit(1)

echo = 'debug'
engine = sqlalchemy.create_engine(url, echo=echo)
metadata = sqlalchemy.MetaData(engine)
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

items_per_page = 15
offset = 15
folder_sizes_larger_than = 10
pi = 'peters_u'

res = session.query(FileMetadata.owner,
                    UidMapping.name,
                    FileMetadata.filename,
                    sqlalchemy.func.to_timestamp(FileMetadata.mtime),
                    FileMetadata.sum / 1024.0 / 1024.0 / 1024.0).\
                    join(UidMapping,
                         FileMetadata.uid == UidMapping.uid).\
                    filter(FileMetadata.count > -1,
                           FileMetadata.owner == pi,
                           (FileMetadata.sum / 1024.0 / 1024.0 / 1024.0) > \
                           folder_sizes_larger_than).\
                    order_by(sqlalchemy.desc(FileMetadata.sum)).\
                    limit(items_per_page).offset(offset)

for item in res:
    print(item)
