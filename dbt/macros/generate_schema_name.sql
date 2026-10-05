{#
    Layer schemas (stage, curate, product) are used as-is, so models land in
    the same schema in every environment. Setting DBT_SCHEMA_PREFIX, e.g. to
    the branch or PR number, isolates a build: pr_12_product, pr_12_curate.
#}
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set schema = custom_schema_name or target.schema -%}
    {%- set prefix = env_var('DBT_SCHEMA_PREFIX', '') -%}
    {{ prefix ~ '_' ~ schema if prefix else schema }}
{%- endmacro %}
