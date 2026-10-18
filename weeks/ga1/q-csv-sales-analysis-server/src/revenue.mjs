// Total revenue = SUM(quantity * price) for one city and month, rounded to an integer.
// Usage: node revenue.mjs ../data/sales_data.csv Bangalore May
// Dates look like 2025-May-8 (YYYY-MMM-D), so the month is the middle part.
import { readFileSync } from "node:fs";

const [file = "../data/sales_data.csv", city = "Bangalore", month = "May"] = process.argv.slice(2);
const rows = readFileSync(file, "utf8").trim().split(/\r?\n/).slice(1).map((l) => l.split(","));
const match = rows.filter(
  ([date, c]) => c.trim().toLowerCase() === city.toLowerCase() && date.split("-")[1].toLowerCase() === month.toLowerCase().slice(0, 3),
);
const total = match.reduce((s, r) => s + Number(r[3]) * Number(r[4]), 0);
console.error(match.map((r) => r.join(",")).join("\n"));
console.error(`rows: ${match.length}  exact: ${total.toFixed(2)}`);
console.log(Math.round(total));
