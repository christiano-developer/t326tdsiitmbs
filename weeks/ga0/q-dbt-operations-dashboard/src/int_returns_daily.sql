{{ config(
    materialized='table',
    tags=['returns', 'ops_dashboard'],
    meta={'owner': 'orbit_ops', 'freshness': 'daily', 'warn_after_hours': 24}
) }}

-- Intermediate model: daily percent refunded on returns, last 14 days.
with returns as (
    select
        return_id,
        order_id,
        cast(returned_at as date) as return_day,
        coalesce(return_amount, 0) as return_amount,
        coalesce(refund_amount, 0) as refund_amount,
        coalesce(is_refunded, false) as is_refunded
    from {{ ref('stg_returns') }}
    where cast(returned_at as date) >= dateadd('day', -14, current_date)
),

daily as (
    select
        date_trunc('day', return_day) as return_date,
        count(*) as return_count,
        sum(case when is_refunded then 1 else 0 end) as refunded_returns,
        sum(return_amount) as total_return_amount,
        sum(refund_amount) as total_refund_amount
    from returns
    group by 1
)

select
    return_date,
    return_count,
    refunded_returns,
    total_return_amount,
    total_refund_amount,
    round(
        100.0 * coalesce(total_refund_amount / nullif(total_return_amount, 0), 0),
        2
    ) as percent_refunded
from daily
order by return_date
