# Final — q-sql-average-salary

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga0/q-sql-average-salary](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga0/q-sql-average-salary)

## How to solve (for a teammate)

> Values are seeded from your email, but this query works for everyone.

1. Paste this query into the answer box:
   ```sql
   SELECT department, ROUND(AVG(salary)) AS avg_salary
   FROM employees
   GROUP BY department
   ORDER BY department;
   ```
2. Click Check, then Save.

## Final prompt

```text
Write a SQLite query on employees(employee_id, name, department, salary) that returns department and the average
salary rounded to a whole number, one row per department, ordered by department. Department must be the first column.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps

```bash
node src/gen_employees.mjs <exam-email> > data/employees.json   # optional: regenerate the table
python3 src/check.py                                             # runs src/average_salary.sql, applies grader check
pbcopy < src/average_salary.sql
```

## Expected output

```
('Engineering', 78523.0)
('Finance', 79265.0)
('HR', 83208.0)
('Marketing', 79582.0)
('Sales', 79313.0)
PASS
```

## Answer submitted (✅ passed, attempt 1)

[src/average_salary.sql](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga0/q-sql-average-salary/src/average_salary.sql).
