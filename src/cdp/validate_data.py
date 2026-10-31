
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "database" / "cdp.db"


def validate_data():
    connection = sqlite3.connect(DB_PATH)

    try:
        checks = {
            "Duplicate customer IDs": """
                SELECT customer_id
                FROM customers
                GROUP BY customer_id
                HAVING COUNT(*) > 1
            """,
            "Duplicate account IDs": """
                SELECT account_id
                FROM accounts
                GROUP BY account_id
                HAVING COUNT(*) > 1
            """,
            "Unknown customer references": """
                SELECT a.account_id
                FROM accounts a
                LEFT JOIN customers c
                    ON a.customer_id = c.customer_id
                WHERE c.customer_id IS NULL
            """,
            "Unknown account references": """
                SELECT t.transaction_id
                FROM transactions t
                LEFT JOIN accounts a
                    ON t.account_id = a.account_id
                WHERE a.account_id IS NULL
            """,
            "Missing customer IDs": """
                SELECT rowid
                FROM customers
                WHERE customer_id IS NULL OR TRIM(customer_id) = ''
            """,
            "Missing account fields": """
                SELECT account_id
                FROM accounts
                WHERE account_id IS NULL
                   OR TRIM(account_id) = ''
                   OR customer_id IS NULL
                   OR TRIM(customer_id) = ''
            """,
            "Missing transaction fields": """
                SELECT transaction_id
                FROM transactions
                WHERE transaction_id IS NULL
                   OR TRIM(transaction_id) = ''
                   OR account_id IS NULL
                   OR TRIM(account_id) = ''
                   OR amount IS NULL
                   OR transaction_date IS NULL
                   OR TRIM(transaction_date) = ''
                   OR transaction_type IS NULL
                   OR TRIM(transaction_type) = ''
            """
        }

        for name, query in checks.items():
            results = connection.execute(query).fetchall()

            print(f"{name}: {len(results)}")
            if results:
                print(results)

    finally:
        connection.close()


if __name__ == "__main__":
    validate_data()
