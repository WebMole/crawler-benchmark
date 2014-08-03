# -*- coding: utf-8 -*-
import sqlite3

from flask import g

from project import app, config


def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()

        for mode in config.modes:
            # create tables if not already created
            database_request = "create table if not exists " \
                               + mode.get("route") \
                               + " (" \
                                 "    id integer primary key autoincrement," \
                                 "    title text not null," \
                                 "    text text not null" \
                                 ");"
            db.cursor().executescript(database_request)
            db.commit()


def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db(app.config["DATABASE"])
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if error is not None:
        raise Exception(str(error))
    else:
        if hasattr(g, 'sqlite_db'):
            g.sqlite_db.close()
        else:
            pass
            # abort(500, "Database not loaded yet")


def connect_db(database_name):
    """Connects to the specific database."""
    rv = sqlite3.connect(database_name)
    rv.row_factory = sqlite3.Row
    return rv