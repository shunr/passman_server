import psycopg2
import time
import os
from typing import Optional

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")

class DBError(Exception):
    pass

class DBInstance:
    def __init__(self, conn: psycopg2.extensions.connection):
        self.conn = conn
        print("Connected to DB!", flush=True)

    def create_account(
        self,
        username: str,
        auth_salt: bytes,
        muk_salt: bytes,
        auth_verifier: bytes,
        display_name: Optional[str],
    ):
        sql = """INSERT INTO accounts(username, display_name, auth_salt, muk_salt, auth_verifier)
             VALUES(%s, %s, %s, %s, %s);"""
        cur = self.conn.cursor()
        if display_name is None:
            display_name = ""
        try:
            cur.execute(sql, (username, display_name, auth_salt, muk_salt, auth_verifier))
            self.conn.commit()
        except Exception as e:
            raise DBError(str(e))

