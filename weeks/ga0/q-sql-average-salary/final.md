# Final — q-sql-average-salary

> Goal: the answer can be reproduced from this file alone.

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

[src/average_salary.sql](src/average_salary.sql).
