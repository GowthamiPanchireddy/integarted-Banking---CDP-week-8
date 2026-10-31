
import sqlite3


def get_table_names(connection: sqlite3.Connection) -> set[str]:
    """Return the names of all tables in the database."""
    rows = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        """
    ).fetchall()

    return {row[0] for row in rows}


def check_required_tables(
    connection: sqlite3.Connection,
    expected_tables: set[str],
) -> bool:
    """Check whether all required tables exist."""
    actual_tables = get_table_names(connection)
    return expected_tables.issubset(actual_tables)
