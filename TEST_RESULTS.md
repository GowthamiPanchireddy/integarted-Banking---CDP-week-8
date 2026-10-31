# Customer 360 CDP – Test Results

## 1. Test Environment

- Language: Python 3.10
- Database: SQLite
- API: Python built-in `http.server`
- Test database: `database/cdp.db`
- Source data: Week 8 Silver transactions
- Customer reference records: 10
- Account reference records: 21
- Transaction records: 13

## 2. Customer 360 Gold Validation

| Test scenario | Expected result | Actual result | Status |
|---|---|---|---|
| Build Customer 360 Gold | 10 customer records | 10 records | PASS |
| C001 – Multiple accounts | 2 accounts, 2 transactions, 625.5 | Matched | PASS |
| C002 – Multiple accounts | 2 accounts, 2 transactions, 1000.0 | Matched | PASS |
| C003 – No transactions | 1 account, 0 transactions, 0 total, NULL date | Matched | PASS |
| C007 – No transactions | 2 accounts, 0 transactions, 0 total | Matched | PASS |

## 3. Independent SQL Verification

Independent SQL queries were executed against the customers, accounts and transactions tables.

All 10 customer records were independently checked.

| Customer | Accounts | Transactions | Total amount | Status |
|---|---:|---:|---:|---|
| C001 | 2 | 2 | 625.5 | PASS |
| C002 | 2 | 2 | 1000.0 | PASS |
| C003 | 1 | 0 | 0 | PASS |
| C004 | 2 | 2 | 1075.0 | PASS |
| C005 | 2 | 2 | 240.0 | PASS |
| C006 | 2 | 1 | 300.0 | PASS |
| C007 | 2 | 0 | 0 | PASS |
| C008 | 2 | 1 | 225.0 | PASS |
| C009 | 2 | 2 | 410.0 | PASS |
| C010 | 4 | 1 | 25.0 | PASS |

Final Gold record count: 10.

All independently calculated account counts, transaction counts and total amounts matched the Gold table.

## 4. API Testing

Endpoint:

`GET /customers/{customer_id}/summary`

| Test | Expected result | Actual result | Status |
|---|---|---|---|
| C001 | HTTP 200 with customer summary | HTTP 200, correct data | PASS |
| C002 | HTTP 200 with customer summary | HTTP 200, correct data | PASS |
| C003 | HTTP 200 with zero transaction values | HTTP 200, correct data | PASS |
| C999 | HTTP 404 with error JSON | HTTP 404, Customer not found | PASS |

Unknown customer response:

```json
{
    "error": "Customer not found"
}
```

## 5. Exception Validation

The invalid-record fixture was used to test exception handling.

| Record ID | Scenario | Expected rejection reason | Status |
|---|---|---|---|
| T1001 | Duplicate transaction ID | Duplicate transaction ID | PASS |
| T9999 | Unknown account reference | Unknown account ID | PASS |
| A9998 | Unknown customer reference | Unknown customer ID | PASS |
| T9998 | Missing transaction date | Missing essential transaction field: transaction_date | PASS |

Total exception records: 3.

### Exception Rerun Safety

The exception-recording script was executed again.

- Existing exception records: 3
- New exception records inserted: 0
- Total exception records after rerun: 3

Result: PASS – no duplicate exception records were inserted.

## 6. Gold Rerun Safety

The Customer 360 Gold table was read before and after rebuilding it from unchanged source tables.

| Check | Result |
|---|---:|
| Records before rebuild | 10 |
| Records after rebuild | 10 |
| All Gold values identical | Yes |
| Final status | PASS |

The verification script confirmed:

`PASS: Gold records are identical after rebuilding!`

## 7. Overall Test Summary

- Customer 360 Gold build: PASS
- Independent SQL verification: PASS
- API tests: 4 PASS
- Exception validation: 3 PASS
- Exception rerun safety: PASS
- Gold rerun safety: PASS
- Missing essential field validation: PASS
- Data quality validation: 7 checks, all passed
- Exception rerun safety after missing-field test: PASS

**Conclusion:** The Customer 360 data product was successfully built and validated using synthetic customer, account and transaction data. The read-only API returned correct customer summaries, including customers without transactions. Independent SQL checks matched Gold metrics, and rerunning the build did not change the results.