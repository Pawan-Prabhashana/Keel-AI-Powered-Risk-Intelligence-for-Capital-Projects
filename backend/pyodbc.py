"""Database access shim: routes connect() to the SQLite factory (utils/db.py)
so every data-access call site shares one connection path."""

from utils.db import connect as _connect


class Error(Exception):
    """Stand-in for pyodbc.Error."""


def connect(connection_string=None, *args, **kwargs):
    return _connect(connection_string)
