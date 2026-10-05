{#
    The source quotes every currency against the base, but not the base
    against itself. Adding that row (rate 1) lets downstream models treat
    all currencies the same way.
#}
with quoted as (
    select
        rate_date,
        base_currency,
        quote_currency,
        rate
    from {{ ref('stg_frankfurter__exchange_rates') }}
),

base_rows as (
    select distinct
        rate_date,
        base_currency,
        base_currency as quote_currency,
        1.0 as rate
    from quoted
)

select
    rate_date || '-' || base_currency || '-' || quote_currency as rate_key,
    rate_date,
    base_currency,
    quote_currency,
    rate
from (
    select * from quoted
    union all
    select * from base_rows
) as rates
