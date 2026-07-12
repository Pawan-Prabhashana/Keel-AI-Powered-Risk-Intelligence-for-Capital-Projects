"""Build the local SQLite database from schema + sample data.

Run once before starting the app:  python setup_database.py
"""

import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.getenv("DB_PATH", os.path.join(HERE, "keel.db"))
SCHEMA = os.path.join(HERE, "sql", "schema_sqlite.sql")
# The original SQL Server sample data is plain INSERT statements -> reused as-is.
SEED = os.path.join(HERE, "sql", "create_data.sql")


def build():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Removed existing {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    with open(SCHEMA, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    print("Schema created.")

    with open(SEED, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    print("Sample data loaded.")

    conn.commit()

    # Quick summary
    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()]
    print(f"\n{len(tables)} tables:")
    for t in tables:
        n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  {t:<35} {n} rows")

    conn.close()
    print(f"\nDatabase ready at: {DB_PATH}")


if __name__ == "__main__":
    build()
