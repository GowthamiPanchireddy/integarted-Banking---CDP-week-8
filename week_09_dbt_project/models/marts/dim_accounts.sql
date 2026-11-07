select
    a.account_id,
    a.customer_id,
    c.customer_name,
    c.city,
    c.customer_segment,
    a.account_type,
    a.opened_date,
    a.account_status
from {{ ref('stg_accounts') }} a
left join {{ ref('stg_customers') }} c
    on a.customer_id = c.customer_id