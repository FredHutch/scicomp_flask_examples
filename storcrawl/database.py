"""
Database goes in a separate file to avoid circular dependencies.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # pylint: disable=invalid-name
