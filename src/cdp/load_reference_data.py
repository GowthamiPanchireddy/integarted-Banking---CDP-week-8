import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "database" / "cdp.db"
CUSTOMERS_FILE = BASE_DIR / "data" / "reference" / "customers.csv"
ACCOUNTS_FILE = BASE_DIR / "data" / "reference" / "accounts.csv"


def load_reference_data():
    connection = sqlite3.connect(DB_PATH)

    try:
        with open(CUSTOMERS_FILE, newline="", encoding="utf-8") as file:
            customers = list(csv.DictReader(file))

        with open(ACCOUNTS_FILE, newline="", encoding="utf-8") as file:
            accounts = list(csv.DictReader(file))

        connection.executemany(
            """
            INSERT INTO customers (customer_id, customer_name)
            VALUES (?, ?)
            """,
            [
                (row["customer_id"], row["customer_name"])
                for row in customers
            ],
        )

        connection.executemany(
            """
            INSERT INTO accounts (account_id, customer_id)
            VALUES (?, ?)
            """,
            [
                (row["account_id"], row["customer_id"])
                for row in accounts
            ],
        )

        connection.commit()

        print("Reference data loaded successfully!")
        print(f"Customers loaded: {len(customers)}")
        print(f"Accounts loaded: {len(accounts)}")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    load_reference_data()