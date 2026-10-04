{#
    Passing "no failing rows" checks on an empty table proves nothing, so
    every layer also asserts it actually has rows.
#}
{% test not_empty(model) %}
    select 1 as failure
    where not exists (select 1 from {{ model }})
{% endtest %}
