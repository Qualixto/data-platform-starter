-- By definition, 1 GBP buys exactly 1 GBP; anything else means the cross-rate maths broke.
select
    rate_date,
    rate_per_gbp
from {{ ref('fx_rates_gbp') }}
where currency_code = 'GBP' and abs(rate_per_gbp - 1) > 1e-9
