PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS accounts (
    account_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount > 0),
    transaction_date TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    FOREIGN KEY (account_id)
        REFERENCES accounts(account_id)
);

CREATE TABLE IF NOT EXISTS exceptions (
    exception_id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id TEXT,
    record_type TEXT NOT NULL,
    rejection_reason TEXT NOT NULL,
    raw_record TEXT
);

CREATE TABLE IF NOT EXISTS customer_360 (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    account_count INTEGER NOT NULL,
    transaction_count INTEGER NOT NULL,
    total_transaction_amount REAL NOT NULL,
    last_transaction_date TEXT,
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);