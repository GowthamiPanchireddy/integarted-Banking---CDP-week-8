import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

DB_PATH = BASE_DIR / "database" / "cdp.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"


def initialize_database():
    connection = sqlite3.connect(DB_PATH)

    try:
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema)
        connection.commit()

        print("CDP database created successfully!")
        print(f"Database location: {DB_PATH}")

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()