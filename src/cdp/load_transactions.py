import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

CDP_DB = BASE_DIR / "database" / "cdp.db"

WEEK8_DB = (
    Path.home()
    / "OneDrive"
    / "Desktop"
    / "integrated-banking-capstone week 8"
    / "database"
    / "banking.db"
)


def load_transactions():
    source = sqlite3.connect(
        f"file:{WEEK8_DB.as_posix()}?mode=ro",
        uri=True
    )

    target = sqlite3.connect(CDP_DB)

    try:
        rows = source.execute(
            """
            SELECT
                transaction_id,
                account_id,
                amount,
                transaction_date,
                transaction_type
            FROM silver_transactions
            ORDER BY transaction_id
            """
        ).fetchall()

        target.executemany(
            """
            INSERT INTO transactions (
                transaction_id,
                account_id,
                amount,
                transaction_date,
                transaction_type
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            rows
        )

        target.commit()

        print("Transactions loaded successfully!")
        print(f"Transactions loaded: {len(rows)}")

    except Exception:
        target.rollback()
        raise

    finally:
        source.close()
        target.close()


if __name__ == "__main__":
    load_transactions()