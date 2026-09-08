import sqlite3

import click
from flask import current_app, g


def get_db():
    """Retorna uma conexão com o banco de dados."""

    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE']
        )

        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """Fecha a conexão com o banco."""

    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Cria as tabelas do banco."""

    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(
            f.read().decode('utf8')
        )


@click.command('init-db')
def init_db_command():
    """Comando para inicializar o banco."""

    init_db()

    click.echo('Banco de dados inicializado.')


def init_app(app):
    """Registra as funções no Flask."""

    app.teardown_appcontext(close_db)

    app.cli.add_command(init_db_command)