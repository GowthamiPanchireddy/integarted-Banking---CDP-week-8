select
    cast(trim(account_id) as varchar) as account_id,
    cast(trim(customer_id) as varchar) as customer_id,
    cast(trim(account_type) as varchar) as account_type,
    cast(opened_date as date) as opened_date,
    cast(trim(account_status) as varchar) as account_status
from {{ ref('accounts') }}
