# Integrated Banking - CDP Week 8

## Project Overview

This project extends the Week 8 banking data pipeline work by adding automated integration tests and reusable database schema-checking functions.

The tests use a temporary SQLite database, so the original Week 8 database is not modified.

## Technologies Used

- Python 3.10
- SQLite
- Pytest
- Git and GitHub

## Project Structure


integrated-banking-capstone-week9/
|-- src/
|   |-- integration/
|       |-- __init__.py
|       |-- schema_checks.py
|-- tests/
|   |-- test_schema_integration.py
|-- data/
|-- evidence/
|   |-- integration-test-results.xml
|-- .gitignore
|-- requirements.txt
|-- README.md


## Integration Tests

The project currently includes six automated tests:

1. Verify that all required pipeline tables are created.
2. Verify that non-positive transaction amounts are rejected.
3. Verify that duplicate transaction IDs are rejected.
4. Verify that unknown pipeline run IDs are rejected.
5. Verify that the table-name function returns the expected tables.
6. Verify that the required-table check returns `True`.

## Reusable Functions

The `src/integration/schema_checks.py` module contains:

- `get_table_names(connection)`: Returns the names of database tables.
- `check_required_tables(connection, expected_tables)`: Checks whether all required tables exist.

## How to Run the Tests

Activate the project's virtual environment, then run:

```powershell
python -m pytest tests\test_schema_integration.py -v
```

To save the test results as an XML report:

```powershell
python -m pytest tests\test_schema_integration.py -v --junitxml=evidence\integration-test-results.xml
```

## Current Test Results

- Total tests: 6
- Passed: 6
- Failed: 0

The test report is saved at `evidence/integration-test-results.xml`.

## Learning Outcomes

- Writing automated integration tests with Pytest.
- Testing SQLite database constraints.
- Creating reusable Python functions.
- Identifying and fixing import errors.
- Saving test results in JUnit XML format.

---

# CDP Readiness Extension – Customer 360

## Project Overview

This extension builds a Customer 360 Gold data product using customer, account, and transaction data from the Week 8 banking pipeline.

It also provides a local read-only API to retrieve customer summary information.

The project uses a separate SQLite database. The original Week 8 database is not modified.

## Technologies Used

- Python 3.10
- SQLite
- SQL
- Python built-in `http.server`
- Pytest

## Data Model

The project includes the following tables:

- `customers` – one row per customer.
- `accounts` – one row per account.
- `transactions` – one row per transaction.
- `exceptions` – stores invalid records and rejection reasons.
- `customer_360` – one row per customer summary.

Customer identity matching uses `customer_id`. Customer names are used only for display.

## Customer 360 Gold

The Gold table contains:

- Customer ID and name.
- Account count.
- Transaction count.
- Total transaction amount.
- Last transaction date.

Customers without transactions are also included, with zero transaction count, zero total amount, and a NULL last transaction date.

## Data Quality and Validation

The project checks:

- Duplicate customer, account, and transaction IDs.
- Unknown customer references.
- Unknown account references.
- Missing essential fields in test records.

Invalid records are stored in the Exceptions table with their rejection reasons.

## API

A local read-only API is implemented using Python's built-in `http.server`.

Endpoint:

`GET /customers/<customer_id>/summary`

- Returns customer summary JSON for a known customer.
- Returns HTTP 404 for an unknown customer.
- Uses parameterized SQL.
- Runs on localhost.

## Rerun Safety

The Gold table can be rebuilt from the same source data.

A verification script compares the Gold records before and after rebuilding to confirm that the results remain identical.

## Documentation and Evidence

- `ARCHITECTURE.md` – project architecture and data flow.
- `PRIVACY_AND_DESIGN.md` – data grain, identity matching, privacy considerations, freshness, and production controls.
- `TEST_RESULTS.md` – validation and testing evidence.
- `database/schema.sql` – database schema.
- `output/customer_360.csv` – exported Customer 360 Gold data.

## How to Run

Activate the virtual environment and run the scripts from the project root.

Initialize the database:

```powershell
python database\init_db.py
```

Load reference data:

```powershell
python src\cdp\load_reference_data.py
```

Load Silver transactions:

```powershell
python src\cdp\load_transactions.py
```

Build Customer 360 Gold:

```powershell
python src\cdp\build_customer360.py
```

Export Gold data:

```powershell
python src\cdp\export_customer360.py
```

Run validation:

```powershell
python src\cdp\validate_data.py
```

Run the local API:

```powershell
python src\cdp\api_server.py
```

## Project Limitations

This is an educational project using synthetic data. The API is intended for local demonstration. Production authentication, authorization, audit logging, consent management, encryption, and rate limiting are documented as future requirements, not implemented features.
