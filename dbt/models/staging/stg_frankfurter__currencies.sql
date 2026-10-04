select
    code as currency_code,
    name as currency_name
from {{ source('frankfurter', 'currencies') }}
