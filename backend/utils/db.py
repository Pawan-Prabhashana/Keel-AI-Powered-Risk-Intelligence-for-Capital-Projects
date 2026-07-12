"""SQLite connection factory for Keel.

Registers GETDATE() and NEWID() as SQLite functions so the SQL used across the
plugins works directly.
"""

import os
import sqlite3
import uuid
from datetime import datetime

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB = os.path.join(HERE, "keel.db")


def _register_compat(conn: sqlite3.Connection):
    # GETDATE() -> current timestamp
    conn.create_function("GETDATE", 0, lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    # NEWID() -> uuid string
    conn.create_function("NEWID", 0, lambda: str(uuid.uuid4()))
    # Identity values are handled via cursor.lastrowid in code
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")


def connect(connection_string: str = None) -> sqlite3.Connection:
    """Opens a SQLite connection.

    `connection_string` is treated as a path to the SQLite file. If it looks
    like an old SQL Server DSN (or is empty), we fall back to the default
    keel.db so nothing breaks.
    """
    path = connection_string
    if not path or "=" in str(path) or "server" in str(path).lower():
        path = os.getenv("DB_PATH", DEFAULT_DB)
    conn = sqlite3.connect(path, check_same_thread=False)
    _register_compat(conn)
    return conn
