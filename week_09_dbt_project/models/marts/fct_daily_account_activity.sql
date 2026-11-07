select
    transaction_date,
    account_id,
    count(transaction_id) as transaction_count,

    sum(
        case
            when transaction_type = 'DEPOSIT' then amount
            else 0
        end
    ) as total_deposits,

    sum(
        case
            when transaction_type in ('PURCHASE', 'WITHDRAWAL') then amount
            else 0
        end
    ) as total_outflows,

    sum(signed_amount) as net_amount

from {{ ref('int_transaction_enriched') }}

group by
    transaction_date,
    account_id