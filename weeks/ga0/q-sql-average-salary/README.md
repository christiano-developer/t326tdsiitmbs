# q-sql-average-salary

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-06 |
| Closed    | 2026-10-06 (passed on attempt 1) |

## Question

**SQL: Average salary by department**: background: *Database: SQLite* (core SQL, Python integration, CLI ops,
indexes, window functions, tools).

> HR Analytics for GlobalTech Corporation. There is an `employees` table in a SQLite database with columns
> `employee_id`, `name`, `department`, and `salary`.
>
> What is the average salary for each department? Write SQL to calculate it. Round the results to the nearest whole
> number. Order the results by department name alphabetically.

Preview ([data/table-preview.png](data/table-preview.png)): `8207 Employee_740 Marketing 105238`, `5787 Employee_840 Sales 69830`, …

Per-user variant: 500 rows seeded from the student email.

## Inputs / given data

- [data/employees.json](data/employees.json): regenerated seeded table (first 5 rows match the page preview) + grader's expected averages.

## Final answer

✅ Passed on the first submission (grader check PASS locally). Paste [src/average_salary.sql](src/average_salary.sql):

```sql
SELECT
  department,
  ROUND(AVG(salary)) AS avg_salary
FROM employees
GROUP BY department
ORDER BY department;
```

Result: Engineering 78523 · Finance 79265 · HR 83208 · Marketing 79582 · Sales 79313.

## Status notes

- Exam Check ✅ **passed**.

## Files

- [prompts.md](prompts.md) · [approaches.md](approaches.md) · [final.md](final.md)
- [src/average_salary.sql](src/average_salary.sql) — submission
- [src/gen_employees.mjs](src/gen_employees.mjs) — regenerates the seeded table
- [src/check.py](src/check.py) — runs the SQL in SQLite and applies the grader's check
