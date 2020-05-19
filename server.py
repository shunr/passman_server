import os

from psycopg2 import pool
from flask import Flask, g, jsonify, request
from passman_server.db import DBInstance

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")


def get_db():
    if "db" not in g:
        g.db = app.config["db_pool"].getconn()
    return DBInstance(g.db)


def create_app():
    _app = Flask(__name__)
    _app.config["db_pool"] = pool.ThreadedConnectionPool(
        1, 100, user=DB_USER, host="db", database=DB_NAME
    )

    @_app.teardown_appcontext
    def close_conn(e):
        db = g.pop("db", None)
        if db is not None:
            _app.config["db_pool"].putconn(db)

    @_app.route("/create_account", methods=["GET", "POST"])
    def create_account():
        body = request.json
        auth_salt = bytes.fromhex(body["auth_salt_hex"])
        muk_salt = bytes.fromhex(body["muk_salt_hex"])
        auth_verifier = bytes.fromhex(body["auth_verifier_hex"])
        db = get_db()
        db.create_account(
            username=body.get("username"),
            auth_salt=auth_salt,
            muk_salt=muk_salt,
            auth_verifier=auth_verifier,
            display_name=body.get("display_name")
        )
        return jsonify({"success": True})

    return _app


app = create_app()
