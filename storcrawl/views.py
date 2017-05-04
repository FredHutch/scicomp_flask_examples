"""
See
https://docs.google.com/document/d/1IvzWOgbeQDLxkTlWX0bg2lcQBmxvba8mAaZgy0Ymxck/edit#
"""

import datetime
import locale

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

locale.setlocale(locale.LC_ALL, 'en_US')

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
    """Render index template"""
    # This SQL is necessary because postgres does not optimize DISTINCT
    # queries very well, so they are slow. This is faster. More info here:
    # https://github.com/FredHutch/storage-crawler/issues/8#issuecomment-298399973
    res = db.engine.execute("""
         with recursive fm(n) as
         (
             select min(owner) from file_metadata union all
                 select(select file_metadata.owner from file_metadata where
                 file_metadata.owner > n order by file_metadata.owner limit 1)
                 from fm where n is not null) select n from fm;""")
    pi_list = []
    for item in res:
        if item[0]is not None:
            pi_list.append(item[0])
    pi_list = sorted(pi_list)
    pi_list.insert(0, 'None')
    return render_template('index.html', pi_list=pi_list)

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

    filters = [FileMetadata.count > -1, FileMetadata.sum > (foldersize * GB)]
    if pi != "None":
        filters.append(FileMetadata.owner == pi)

    res = db.session.query(FileMetadata.owner,
                           UidMapping.name,
                           FileMetadata.filename,
                           sqlalchemy.func.to_timestamp(FileMetadata.mtime),
                           FileMetadata.sum / GB).\
                        join(UidMapping,
                             FileMetadata.uid == UidMapping.uid).\
                        filter(*filters).\
                        order_by(sqlalchemy.desc(FileMetadata.sum)).\
                        limit(rows_per_page).offset(offset)
    out = []
    for item in res:
        row = []
        for cell in item:
            if isinstance(cell, datetime.datetime):
                cell = cell.isoformat()
            elif isinstance(cell, int):
                cell = locale.format("%d", cell, grouping=True)
            row.append(cell)

        out.append(row)

    return jsonify(out)
