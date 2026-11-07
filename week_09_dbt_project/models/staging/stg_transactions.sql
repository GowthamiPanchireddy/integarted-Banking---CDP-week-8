select
    cast(trim(transaction_id) as varchar) as transaction_id,
    cast(trim(account_id) as varchar) as account_id,
    cast(transaction_date as date) as transaction_date,
    cast(amount as decimal(12, 2)) as amount,
    upper(trim(transaction_type)) as transaction_type,
    upper(trim(currency)) as currency
from {{ ref('transactions') }}
