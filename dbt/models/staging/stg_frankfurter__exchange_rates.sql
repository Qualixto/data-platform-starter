select
    rate_date::date as rate_date,
    base_currency,
    quote_currency,
    rate::double as rate
from {{ source('frankfurter', 'exchange_rates') }}
