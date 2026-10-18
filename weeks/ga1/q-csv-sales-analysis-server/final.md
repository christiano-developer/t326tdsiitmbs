# Final — q-csv-sales-analysis-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga1/q-csv-sales-analysis-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga1/q-csv-sales-analysis-server)

## How to solve (for a teammate)

> Seeded per email: your CSV, **city and month** differ. Read them off your question
> ("Calculate total revenue for transactions in <City> during <Month> 2025").

1. On the exam page click **Download Sales Data (ZIP)** and unzip it. You get `sales_data.csv`
   (`date,city,product,quantity,price`; dates look like `2025-May-8`).
2. Save the script below as `revenue.mjs` next to the CSV (Node 18+, no packages).
3. Run it with your city and month, e.g. `node revenue.mjs sales_data.csv Bangalore May`.
   It prints the matching rows and the exact total, then the rounded integer on the last line.
4. Enter that integer, then Check and Save. The grader accepts ±2.

<details><summary>revenue.mjs (click to expand)</summary>

```js
import { readFileSync } from "node:fs";

const [file = "sales_data.csv", city = "Bangalore", month = "May"] = process.argv.slice(2);
const rows = readFileSync(file, "utf8").trim().split(/\r?\n/).slice(1).map((l) => l.split(","));
const match = rows.filter(
  ([date, c]) => c.trim().toLowerCase() === city.toLowerCase() && date.split("-")[1].toLowerCase() === month.toLowerCase().slice(0, 3),
);
const total = match.reduce((s, r) => s + Number(r[3]) * Number(r[4]), 0);
console.error(match.map((r) => r.join(",")).join("\n"));
console.error(`rows: ${match.length}  exact: ${total.toFixed(2)}`);
console.log(Math.round(total));
```

</details>

## Final prompt

```text
sales_data.csv has columns date,city,product,quantity,price with dates like 2025-May-8 (month name, day not
zero-padded). Write a Node script that takes the file, a city and a month name, filters rows by city
(case-insensitive) and month, prints the matching rows, and prints SUM(quantity*price) rounded to an integer.
```

- **Tool / model used:** Claude (Claude Opus 5.5) via Claude in Chrome.

## Reproduction steps (needs a clone of this repo)

```bash
cd weeks/ga1/q-csv-sales-analysis-server/src
node revenue.mjs ../data/sales_data.csv Bangalore May
```

## Expected output

```
2025-May-8,Bangalore,Keyboard,4,475.99
2025-May-22,Bangalore,Monitor,7,573.82
2025-May-16,Bangalore,Mouse,10,472.45
2025-May-12,Bangalore,Phone,7,195.04
rows: 4  exact: 12010.48
12010
```

## Answer submitted (✅ Check passed)

```
12010
```
