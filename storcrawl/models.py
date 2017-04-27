import sqlalchemy
from database import db


class FileMetadata(db.Model):
    __tablename__ = "file_metadata"
    # only listing the columns we care about...
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String)
    uid = db.Column(db.BigInteger, primary_key=True)
    filename = db.Column(db.String)
    count = db.Column(db.Integer)
    mtime = db.Column(sqlalchemy.dialects.postgresql.DOUBLE_PRECISION)
    sum = db.Column(sqlalchemy.dialects.postgresql.DOUBLE_PRECISION)

class UidMapping(db.Model):
    __tablename__ = "uid_mapping"
    # composite key, which is also the only columns we care about....
    name = db.Column(db.String, primary_key=True)
    uid = db.Column(db.BigInteger, primary_key=True)
    homedir = db.Column(db.String, primary_key=True)
