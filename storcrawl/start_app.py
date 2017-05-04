"""
Entry point for gunicorn
"""
from app import create_app

app = create_app() # pylint: disable=invalid-name
