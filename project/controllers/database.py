# -*- coding: utf-8 -*-
import os

import psycopg2
import psycopg2.extras

from flask import g as flask_global
from project import app, config


def init_db():
    with app.app_context():
        db = get_db()

        for mode in config.modes:
            database_request = "create table if not exists " \
                               + mode.get("route") \
                               + " (" \
                                 "    id serial primary key," \
                                 "    title text not null," \
                                 "    text text not null" \
                                 ");"
            db.cursor().execute(database_request)
            db.commit()


def get_db():
    if not hasattr(flask_global, 'postgres_db'):
        flask_global.postgres_db = connect_db()
    return flask_global.postgres_db


@app.teardown_appcontext
def close_db(error):
    if error is not None:
        raise Exception(str(error))
    else:
        if hasattr(flask_global, 'postgres_db'):
            flask_global.postgres_db.close()
        else:
            pass
            # abort(500, "Database not loaded yet")


def connect_db():
    db = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        host=os.getenv('POSTGRES_HOST'),
        password=os.getenv('POSTGRES_PASSWORD'),
    )
    return db
