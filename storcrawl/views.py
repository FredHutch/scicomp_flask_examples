"""
See
https://docs.google.com/document/d/1IvzWOgbeQDLxkTlWX0bg2lcQBmxvba8mAaZgy0Ymxck/edit#
"""

import os

# import requests

from flask.blueprints import Blueprint
from flask import request, abort, jsonify, render_template

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.types
import sqlalchemy.ext.declarative
import sqlalchemy.dialects.postgresql

from database import db
from models import FileMetadata, UidMapping

GB = 1024 * 1024 * 1024


main_blueprint = Blueprint('main_blueprint', __name__, # pylint: disable=invalid-name
                           template_folder='templates',
                           static_folder='static')

Base = sqlalchemy.ext.declarative.declarative_base() # pylint: disable=invalid-name

@main_blueprint.route('/test')
def test():
    "a test route"
    thing = FileMetadata.query.first()
    return str(thing.mtime)

@main_blueprint.route('/')
def index():
    """Return static index page"""
    # req = requests.get('https://toolbox.fhcrc.org/json/pi_all.json')

    return render_template('index.html')

@main_blueprint.route('/query')
def query():
    """
    Call me like this:
    curl "http://localhost:5000/query?pi=peters_u&foldersize=10&rows_per_page=15&offset=15"
    """
    pi = request.args.get('pi') # pylint: disable=invalid-name
    foldersize = request.args.get('foldersize')
    rows_per_page = request.args.get('rows_per_page')
    offset = request.args.get('offset')
    if any([x is None for x in [pi, foldersize, rows_per_page, offset]]):
        abort(400, 'missing some parameters')
    try:
        foldersize = int(foldersize)
        rows_per_page = int(rows_per_page)
        offset = int(offset)
    except ValueError:
        abort(400, 'foldersize, rows_per_page, and offset must be numbers')

    res = db.session.query(FileMetadata.owner,
                           UidMapping.name,
                           FileMetadata.filename,
                           sqlalchemy.func.to_timestamp(FileMetadata.mtime),
                           FileMetadata.sum / GB).\
                        join(UidMapping,
                             FileMetadata.uid == UidMapping.uid).\
                        filter(FileMetadata.count > -1,
                               FileMetadata.owner == pi,
                               (FileMetadata.sum / GB) > \
                               foldersize).\
                        order_by(sqlalchemy.desc(FileMetadata.sum)).\
                        limit(rows_per_page).offset(offset)
    out = []
    for item in res:
        row = []
        for cell in item:
            row.append(cell)
        out.append(row)

    return jsonify(out)

@main_blueprint.route('/pi_list')
def pi_list():
    import IPython;IPython.embed()
    pi_file = os.path.join(main_blueprint.staticfolder, "pi_list.txt")
    pi_fh = open(pi_file)
    raw_lines = pi_fh.readlines()
    lines = [x.strip() for x in raw_lines]
    return jsonify(lines)
