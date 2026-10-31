import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "database" / "cdp.db"


def build_customer360():
    connection = sqlite3.connect(DB_PATH)

    try:
        connection.execute("DELETE FROM customer_360")

        connection.execute("""
            INSERT INTO customer_360 (
                customer_id,
                customer_name,
                account_count,
                transaction_count,
                total_transaction_amount,
                last_transaction_date
            )
            SELECT
                c.customer_id,
                c.customer_name,
                COUNT(DISTINCT a.account_id),
                COUNT(t.transaction_id),
                COALESCE(SUM(t.amount), 0),
                MAX(t.transaction_date)
            FROM customers c
            LEFT JOIN accounts a
                ON c.customer_id = a.customer_id
            LEFT JOIN transactions t
                ON a.account_id = t.account_id
            GROUP BY
                c.customer_id,
                c.customer_name
        """)

        connection.commit()

        count = connection.execute(
            "SELECT COUNT(*) FROM customer_360"
        ).fetchone()[0]

        print("Customer 360 Gold table built successfully!")
        print(f"Customer records: {count}")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    build_customer360()