import sqlite3
from pathlib import Path

import pytest

from src.integration.schema_checks import (
    get_table_names,
    check_required_tables,
)


SCHEMA_PATH = (
    Path(__file__).resolve().parents[2]
    / "integrated-banking-capstone week 8"
    / "database"
    / "schema.sql"
)


@pytest.fixture
def connection(tmp_path):
    database_path = tmp_path / "integration_test.db"

    conn = sqlite3.connect(database_path)
    conn.execute("PRAGMA foreign_keys = ON")

    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    conn.executescript(schema)

    yield conn
    conn.close()


def test_all_pipeline_tables_are_created(connection):
    rows = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        """
    ).fetchall()

    table_names = {row[0] for row in rows}

    expected_tables = {
        "pipeline_runs",
        "bronze_transactions",
        "silver_transactions",
        "exceptions",
        "gold_branch_daily",
    }

    assert expected_tables.issubset(table_names)


def test_silver_rejects_non_positive_amount(connection):
    connection.execute(
        """
        INSERT INTO pipeline_runs (started_at, status)
        VALUES ('2026-10-26 12:00:00', 'RUNNING')
        """
    )

    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(
            """
            INSERT INTO silver_transactions (
                transaction_id, account_id, transaction_date,
                transaction_type, amount, currency, branch_id,
                source_file, run_id
            )
            VALUES (
                'TX001', 'ACC001', '2026-10-26',
                'CREDIT', 0, 'INR', 'BR001',
                'test.csv', 1
            )
            """
        )


def test_silver_rejects_duplicate_transaction_id(connection):
    connection.execute(
        """
        INSERT INTO pipeline_runs (started_at, status)
        VALUES ('2026-10-26 12:00:00', 'RUNNING')
        """
    )

    transaction = (
        "TX001", "ACC001", "2026-10-26",
        "CREDIT", 100.0, "INR", "BR001",
        "test.csv", 1
    )

    connection.execute(
        """
        INSERT INTO silver_transactions (
            transaction_id, account_id, transaction_date,
            transaction_type, amount, currency, branch_id,
            source_file, run_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        transaction
    )

    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(
            """
            INSERT INTO silver_transactions (
                transaction_id, account_id, transaction_date,
                transaction_type, amount, currency, branch_id,
                source_file, run_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            transaction
        )


def test_silver_rejects_unknown_pipeline_run(connection):
    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(
            """
            INSERT INTO silver_transactions (
                transaction_id, account_id, transaction_date,
                transaction_type, amount, currency, branch_id,
                source_file, run_id
            )
            VALUES (
                'TX002', 'ACC002', '2026-10-26',
                'CREDIT', 100.0, 'INR', 'BR001',
                'test.csv', 999
            )
            """
        )


def test_get_table_names_returns_existing_tables(connection):
    table_names = get_table_names(connection)

    assert {
        "pipeline_runs",
        "bronze_transactions",
        "silver_transactions",
        "exceptions",
        "gold_branch_daily",
    }.issubset(table_names)


def test_check_required_tables_returns_true(connection):
    expected_tables = {
        "pipeline_runs",
        "silver_transactions",
        "gold_branch_daily",
    }

    assert check_required_tables(connection, expected_tables) is True
