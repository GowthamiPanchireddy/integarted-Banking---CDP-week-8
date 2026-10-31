# Customer 360 CDP – Privacy and Design

## 1. Customer Identity Rule

The project uses `customer_id` as the unique customer identity key.

- Each customer has a unique customer ID.
- Each account is linked to a customer using `customer_id`.
- Each transaction is linked to an account using `account_id`.
- Customer names are used for display only.
- Customers are not merged based only on matching names.

This approach helps prevent incorrect customer identity matching.

## 2. Data Model and Grain

Grain describes what one row represents in a database table.

| Table | Grain | Primary Key |
|---|---|---|
| customers | One row per customer | customer_id |
| accounts | One row per account | account_id |
| transactions | One row per transaction | transaction_id |
| customer_360 | One row per customer summary | customer_id |
| exceptions | One row per recorded exception | exception_id |

### Relationships

- One customer can have multiple accounts.
- One account can have multiple transactions.
- Each transaction belongs to one account.
- Each account belongs to one customer.

## 3. Customer 360 Design

The Customer 360 Gold table combines customer, account and transaction information.

It provides:

- Customer name
- Number of accounts
- Number of transactions
- Total transaction amount
- Last transaction date

Customers without transactions are retained in the Gold output.

For these customers:

- Transaction count = 0
- Total transaction amount = 0
- Last transaction date = NULL

SQL LEFT JOIN operations are used to retain customers without transactions.

## 4. Data Quality Controls

The project includes checks for:

- Duplicate customer IDs.
- Duplicate account IDs.
- Duplicate transaction IDs.
- Unknown customer references.
- Unknown account references.
- Invalid test records.

Invalid records are stored in the Exceptions table with their rejection reasons.

The exception-recording process checks existing exceptions before inserting new ones to avoid duplicate exception entries on reruns.

## 5. Privacy Considerations

- Only synthetic customer names and IDs are used.
- No real customer personal information is included.
- No production banking account identifiers are used.
- The API returns customer summary information only.
- Full transaction histories are not exposed through the API.
- The API is configured to run on localhost for demonstration.

## 6. Production Controls Not Implemented

This project is an educational demonstration, not a production banking system.

A real banking CDP would require additional controls, including:

- Authentication to verify users.
- Authorization to control access to customer data.
- Audit logging to track data access.
- Customer consent and privacy management.
- Data encryption in transit and at rest.
- API rate limiting.
- Secure credential and secret management.
- Monitoring and alerting.
- Data retention and deletion policies.

These controls are documented as future production requirements and are not implemented in this project.

## 7. Data Freshness and Provenance

The transaction data is loaded from the Week 8 Silver table into a separate CDP database.

The Customer 360 Gold table is a snapshot based on the data available when the build script runs.

New Silver transactions will not automatically appear in Customer 360. The loading and Gold-building processes must be run again to refresh the output.

The original Week 8 database remains unchanged.

## 8. Project Limitations

- Synthetic data is used for testing.
- Customer identity matching uses predefined customer IDs.
- This project does not implement advanced identity resolution.
- The API is read-only and intended for local demonstration.
- Enterprise security and governance controls are documented but not implemented.