# q-dbt-operations-dashboard

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-06 |
| Closed    | 2026-10-06 (passed on attempt 1) |

## Question

**Data Transformation with dbt**: *dbt: Operations performance mart* (background: dbt fundamentals, models,
materialization, tests, Jinja, `ref`/`source`, seeds, macros, incremental models, orchestration).

> **Operations performance mart for Orbit Ops.** Orbit Ops uses dbt to publish dashboards for operational leaders.
> Build an **intermediate model** that powers the **returns** dashboards. The team focuses on **percent refunded**
> at a **daily** grain covering the **last 14 days**.
>
> Upstream models expose staging tables (e.g. `stg_shipments`, `stg_returns`). Build on them with `{{ ref() }}` and Jinja.
>
> The model must:
> - Use `{{ config(...) }}` to declare materialization and freshness metadata.
> - Reference upstream models via `{{ ref() }}` (and `{{ source() }}` if needed).
> - Filter rows to the last 14 days relative to `current_date`.
> - Aggregate at daily grain (`date_trunc` or similar).
> - Compute business-ready metrics for percent refunded; include logic referencing "return" and other domain terms.
> - Handle NULLs with `coalesce` / `ifnull`.
> - Return columns ready for BI consumption, ordered by date.
>
> Assume a Snowflake/BigQuery-compatible dialect. Paste your dbt model.

Per-user variant (seeded): domain *returns*, metric *percent_refunded*, grain *daily*, window *14 days*,
model type *intermediate*, required term *return*.

## Inputs / given data

None (free-form SQL).

## Final answer

✅ Passed on the first submission. Copy **from the file**: `pbcopy < src/int_returns_daily.sql`.

## Status notes

- Local grader replica `src/check.py`: 11/11 PASS. Exam Check ✅ **passed**.

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer
- [src/int_returns_daily.sql](src/int_returns_daily.sql) — the dbt model (submission)
- [src/check.py](src/check.py) — local replica of the grader's regex checks
