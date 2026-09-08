import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__,
    instance_relative_config=True)
    # ... configurações iniciais ...
    from . import db
    db.init_app(app)
    return app

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)