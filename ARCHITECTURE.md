# Customer 360 CDP – Architecture

## 1. Project Overview

This project extends the Week 8 Banking Data Pipeline by creating a customer-level Gold data product called Customer 360.

It uses customer reference data, account reference data and validated Silver transaction data to generate a single summary record for each customer.

A read-only API provides access to customer summaries.

## 2. Architecture Flow

```text
             Week 8 Banking Pipeline
                       |
                       v
              Silver Transactions
                       |
                       v
              Load Transactions
                       |
                       |
Customer Reference --> Customers Table
                       |
Account Reference ----> Accounts Table
                       |
                       v
                Data Validation
                       |
              +--------+--------+
              |                 |
              v                 v
         Valid Records      Invalid Records
              |                 |
              v                 v
        Transactions       Exceptions Table
              |
              v
       Customer 360 Gold
              |
              v
        Customer 360 API
              |
              v
        JSON Customer Summary
```

## 3. Main Components

### Customer Reference Data

- Source: `data/reference/customers.csv`
- Contains synthetic customer IDs and names.
- Customer ID is the unique identity key.

### Account Reference Data

- Source: `data/reference/accounts.csv`
- Contains account IDs and their customer relationships.
- One customer can have multiple accounts.

### Silver Transactions

- Source: Week 8 `banking.db` Silver table.
- Loaded into the separate CDP database.
- The original Week 8 database is not modified.

### Data Validation

Validation checks include:

- Duplicate customer IDs.
- Duplicate account IDs.
- Unknown customer references.
- Unknown account references.
- Duplicate transaction IDs.

Invalid test records are stored in the Exceptions table with rejection reasons.

### Customer 360 Gold

The Gold table contains one row per customer.

It includes:

- Customer ID
- Customer name
- Account count
- Transaction count
- Total transaction amount
- Last transaction date

Customers without transactions are retained with zero counts and totals and a NULL last transaction date.

### Customer 360 API

- Implemented using Python's built-in `http.server`.
- Runs locally on `127.0.0.1:8000`.
- Supports a read-only GET endpoint.
- Returns customer summary data in JSON format.
- Returns HTTP 404 for unknown customers.

## 4. Database

Database file:

`database/cdp.db`

Main tables:

- customers
- accounts
- transactions
- exceptions
- customer_360

## 5. Data Lineage

Week 8 Silver transactions and synthetic customer/account reference CSV files are loaded into the separate CDP database.

The validation process checks references and records invalid test cases in the Exceptions table.

Validated data is aggregated into Customer 360 Gold using SQL.

The API reads the Gold table and returns the requested customer summary.

## 6. Rerun Safety

The Gold build process deletes and rebuilds the Gold records from unchanged source tables.

The verification script compares all Gold records before and after rebuilding.

The exception-recording script checks existing exception records before inserting new ones.

Both rerun-safety checks passed.

## 7. Limitations

- This is a synthetic learning project.
- It is not a production banking CDP.
- The API is a local demonstration.
- Authentication, authorization, production monitoring and enterprise privacy controls are not implemented.