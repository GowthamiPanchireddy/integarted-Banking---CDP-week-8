select
    t.transaction_id,
    t.account_id,
    a.customer_id,
    c.customer_name,
    c.city,
    c.customer_segment,
    t.transaction_date,
    t.amount,
    t.transaction_type,
    t.currency,
    case
        when t.transaction_type = 'DEPOSIT' then t.amount
        when t.transaction_type in ('PURCHASE', 'WITHDRAWAL') then -t.amount
        else 0
    end as signed_amount
from {{ ref('stg_transactions') }} t
left join {{ ref('stg_accounts') }} a
    on t.account_id = a.account_id
left join {{ ref('stg_customers') }} c
    on a.customer_id = c.customer_id
