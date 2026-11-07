select
    cast(trim(customer_id) as varchar) as customer_id,
    cast(trim(customer_name) as varchar) as customer_name,
    cast(trim(city) as varchar) as city,
    cast(trim(customer_segment) as varchar) as customer_segment
from {{ ref('customers') }}
