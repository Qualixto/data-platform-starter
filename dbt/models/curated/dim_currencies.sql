select
    currency_code,
    currency_name
from {{ ref('stg_frankfurter__currencies') }}
