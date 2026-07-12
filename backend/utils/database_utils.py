"""Database utilities for Keel (SQLite).

Public API is unchanged: get_connection, execute_query_with_retry,
close_connections. Callers do not need to change.
"""

import threading
from utils import db as _db

_thread_local = threading.local()


def get_connection():
    """Gets a thread-local SQLite connection (kept for API compatibility)."""
    if not hasattr(_thread_local, "connection") or _thread_local.connection is None:
        _thread_local.connection = _db.connect()
        print("Created new database connection")

    try:
        _thread_local.connection.execute("SELECT 1")
        return _thread_local.connection
    except Exception:
        try:
            _thread_local.connection.close()
        except Exception:
            pass
        _thread_local.connection = _db.connect()
        print("Created new database connection after stale connection")
        return _thread_local.connection


def execute_query_with_retry(query, params=None, max_retries=3):
    """Executes a query with retry logic. Returns list[dict] for SELECT,
    True for writes."""
    import time

    retry_count = 0
    last_error = None
    while retry_count < max_retries:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params or [])

            if query.strip().upper().startswith("SELECT") or " RETURNING " in query.upper():
                rows = cursor.fetchall()
                results = [dict(row) for row in rows]
                cursor.close()
                return results
            else:
                conn.commit()
                cursor.close()
                return True
        except Exception as e:
            retry_count += 1
            last_error = e
            print(f"Database query failed (attempt {retry_count}/{max_retries}): {e}")
            if retry_count < max_retries:
                time.sleep(0.5)
            else:
                print(f"Failed to execute query after {max_retries} attempts")
                raise last_error


def close_connections():
    """Closes the thread-local connection."""
    if hasattr(_thread_local, "connection") and _thread_local.connection is not None:
        try:
            _thread_local.connection.close()
            _thread_local.connection = None
            print("Closed thread-local database connection")
        except Exception as e:
            print(f"Error closing connection: {e}")
