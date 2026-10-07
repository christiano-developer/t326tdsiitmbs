# Final — q-dbt-operations-dashboard

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga0/q-dbt-operations-dashboard](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga0/q-dbt-operations-dashboard)

## How to solve (for a teammate)

> Values are seeded from your email, but any SQL meeting the checks passes.

1. Copy [src/int_returns_daily.sql](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga0/q-dbt-operations-dashboard/src/int_returns_daily.sql) and paste it into the answer box.
2. If your business or metric differs, paste the prompt under "Final prompt" into any LLM with your names. The SQL must have:
   - `{{ config(` and `{{ ref('...') }}`
   - a `with` CTE, `coalesce`, and `date_trunc('day', ...)`
   - the 14-day filter on one line, for example `where cast(returned_at as date) >= dateadd('day', -14, current_date)`
3. Click Check, then Save.

## Final prompt

```text
Write a dbt intermediate model (Snowflake SQL + Jinja) for Orbit Ops returns: daily percent refunded over the
last 14 days, built on {{ ref('stg_returns') }}.
Requirements (an auto-grader regex-checks the text):
- Start with {{ config(materialized='table', meta={...freshness...}) }}.
- Use CTEs (WITH) and {{ ref('stg_returns') }}.
- Coalesce amounts and flags (coalesce).
- The 14-day filter must be ONE line containing the standalone word "date" and ">=", exactly like:
  where cast(returned_at as date) >= dateadd('day', -14, current_date)
- Aggregate with date_trunc('day', ...); compute sums of return_amount and refund_amount and
  percent_refunded = 100 * refund / nullif(return, 0), coalesced to 0, rounded to 2.
- Select BI-ready columns and order by the date column.
Output only the SQL.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps

1. Write the model to [`src/int_returns_daily.sql`](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga0/q-dbt-operations-dashboard/src/int_returns_daily.sql).
2. Validate: `python3 src/check.py src/int_returns_daily.sql` (all PASS).
3. Copy **from the file**: `pbcopy < src/int_returns_daily.sql`, then paste, Check and Save.

## Expected output

```
PASS non-empty
PASS uses Jinja {{ }}
PASS intermediate: {{ ref(
PASS intermediate: CTE (with)
PASS daily: date_trunc('day' or ::date
PASS percent_refunded logic: sum|refund|amount
PASS business term 'return'
PASS 14-day filter: where ... \bdate\b ... >=|between (single line)
PASS SELECT and FROM
PASS NULL handling: coalesce|ifnull|0)
PASS {{ config(
```

## Answer submitted (✅ passed, attempt 1)

[src/int_returns_daily.sql](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga0/q-dbt-operations-dashboard/src/int_returns_daily.sql), copied with `pbcopy`.
