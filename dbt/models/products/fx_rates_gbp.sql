with rates as (
    select
        rate_date,
        quote_currency,
        rate
    from {{ ref('fct_exchange_rates') }}
),

gbp as (
    select
        rate_date,
        rate as gbp_rate
    from rates
    where quote_currency = 'GBP'
),

per_gbp as (
    select
        rates.rate_date,
        rates.quote_currency as currency_code,
        rates.rate / gbp.gbp_rate as rate_per_gbp
    from rates
    inner join gbp on rates.rate_date = gbp.rate_date
)

select
    per_gbp.rate_date || '-' || per_gbp.currency_code as rate_key,
    per_gbp.rate_date,
    per_gbp.currency_code,
    currencies.currency_name,
    per_gbp.rate_per_gbp,
    100 * (
        per_gbp.rate_per_gbp
        / lag(per_gbp.rate_per_gbp)
            over (
                partition by per_gbp.currency_code order by per_gbp.rate_date
            )
        - 1
    ) as change_1d_pct
from per_gbp
inner join {{ ref('dim_currencies') }} as currencies
    on per_gbp.currency_code = currencies.currency_code
