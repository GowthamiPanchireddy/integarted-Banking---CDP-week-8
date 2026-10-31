
import csv
import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "database" / "cdp.db"
FIXTURE_FILE = BASE_DIR / "data" / "test_fixtures" / "invalid_records.csv"


def record_exceptions():
    connection = sqlite3.connect(DB_PATH)

    try:
        with open(FIXTURE_FILE, newline="", encoding="utf-8") as file:
            records = list(csv.DictReader(file))

        exceptions = []

        for record in records:
            reason = ""

            if record["record_type"] == "TRANSACTION":

                # Check required transaction fields
                required_fields = [
                    "record_id",
                    "account_id",
                    "amount",
                    "transaction_date",
                    "transaction_type"
                ]

                missing_fields = [
                    field for field in required_fields
                    if not record.get(field, "").strip()
                ]

                if missing_fields:
                    reason = (
                        "Missing essential transaction field: "
                        + ", ".join(missing_fields)
                    )

                else:
                    existing = connection.execute(
                        "SELECT 1 FROM transactions WHERE transaction_id = ?",
                        (record["record_id"],)
                    ).fetchone()

                    account = connection.execute(
                        "SELECT 1 FROM accounts WHERE account_id = ?",
                        (record["account_id"],)
                    ).fetchone()

                    if existing:
                        reason = "Duplicate transaction ID"

                    elif not account:
                        reason = "Unknown account ID"

            elif record["record_type"] == "ACCOUNT":

                # Check required account fields
                if not record.get("record_id", "").strip() or not record.get("customer_id", "").strip():
                    reason = "Missing essential account field"

                else:
                    customer = connection.execute(
                        "SELECT 1 FROM customers WHERE customer_id = ?",
                        (record["customer_id"],)
                    ).fetchone()

                    if not customer:
                        reason = "Unknown customer ID"

            if reason:
                already_exists = connection.execute(
                    """
                    SELECT 1
                    FROM exceptions
                    WHERE record_id = ?
                      AND record_type = ?
                      AND rejection_reason = ?
                    """,
                    (
                        record["record_id"],
                        record["record_type"],
                        reason
                    )
                ).fetchone()

                if not already_exists:
                    exceptions.append((
                        record["record_id"],
                        record["record_type"],
                        reason,
                        json.dumps(record)
                    ))

        if exceptions:
            connection.executemany(
                """
                INSERT INTO exceptions (
                    record_id,
                    record_type,
                    rejection_reason,
                    raw_record
                )
                VALUES (?, ?, ?, ?)
                """,
                exceptions
            )

        connection.commit()

        print("Exception validation completed!")
        print(f"New exception records inserted: {len(exceptions)}")

        for item in exceptions:
            print(f"{item[0]}: {item[2]}")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    record_exceptions()

