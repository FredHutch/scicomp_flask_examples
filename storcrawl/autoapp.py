"""
Command-line interface to SQLAlchemy models.

You can use me as follows. If there is a method below
named `foo` with an @app.cli.command() decorator,
you can run it like this:

FLASK_APP=autoapp flask foo
"""

import click
from app import create_app
from models import FileMetadata
from sqlalchemy import distinct
from database import db

app = create_app() # pylint: disable=invalid-name

@app.cli.command()
def get_pi_list():
    """Get a list of PIs. This will take a couple minutes."""
    res = db.session.query(distinct(FileMetadata.owner)).order_by(FileMetadata.owner)
    pis = []
    for item in res:
        pis.append(item[0])
    for item in sorted(pis): # for case-sensitive sorting
        click.echo(item)

@app.cli.command()
def haha():
    """hahaha"""
    thing = FileMetadata.query.first()
    click.echo(str(thing.mtime))
