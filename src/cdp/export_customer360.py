import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "database" / "cdp.db"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "customer_360.csv"


def export_customer360():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    try:
        rows = connection.execute("""
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

        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "customer_id",
                "customer_name",
                "account_count",
                "transaction_count",
                "total_transaction_amount",
                "last_transaction_date"
            ])

            writer.writerows(rows)

        print("Customer 360 CSV exported successfully!")
        print(f"Records exported: {len(rows)}")
        print(f"File location: {OUTPUT_FILE}")

    finally:
        connection.close()


if __name__ == "__main__":
    export_customer360()