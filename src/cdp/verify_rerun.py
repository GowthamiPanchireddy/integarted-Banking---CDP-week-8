
import sqlite3
from pathlib import Path

from build_customer360 import build_customer360

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "database" / "cdp.db"


def get_gold_records():
    connection = sqlite3.connect(DB_PATH)

    try:
        records = connection.execute("""
            SELECT
                customer_id,
                customer_name,
                account_count,
                transaction_count,
                total_transaction_amount,
                last_transaction_date
            FROM customer_360
            ORDER BY customer_id
        """).fetchall()

        return records

    finally:
        connection.close()


def verify_rerun():
    print("Reading Gold records before rebuild...")

    before_records = get_gold_records()

    print(f"Records before rebuild: {len(before_records)}")

    print("\nRebuilding Customer 360 Gold table...")

    build_customer360()

    print("\nReading Gold records after rebuild...")

    after_records = get_gold_records()

    print(f"Records after rebuild: {len(after_records)}")

    if before_records == after_records:
        print("\nPASS: Gold records are identical after rebuilding!")
    else:
        print("\nFAIL: Gold records are different!")


if __name__ == "__main__":
    verify_rerun()
