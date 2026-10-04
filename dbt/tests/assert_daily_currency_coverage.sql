{{ config(severity='warn') }}
-- A partial load shows up as a day with far fewer currencies than usual.
-- It warns rather than blocks: the ECB does occasionally drop a currency.
with daily as (
    select
        rate_date,
        count(*) as currencies
    from {{ ref('fx_rates_gbp') }}
    group by rate_date
),

usual as (
    select max(currencies) as currencies
    from daily
)

select
    daily.rate_date,
    daily.currencies
from daily
cross join usual
where daily.currencies < 0.9 * usual.currencies
