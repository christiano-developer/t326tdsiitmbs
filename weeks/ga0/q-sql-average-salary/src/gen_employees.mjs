// Regenerates the seeded employees table exactly as the GA0 grader does and writes it as JSON.
// Usage: node src/gen_employees.mjs <exam-email> > data/employees.json   (npm i seedrandom@3)
import seedrandom from "seedrandom";
const n = seedrandom(`${process.argv[2]}#q-sql-average-salary`);
const l = ["Engineering", "Sales", "Marketing", "HR", "Finance"];
const s = Array.from({ length: 500 }, () => ({ employee_id: Math.floor(n() * 1e4) + 1e3, name: `Employee_${Math.floor(n() * 1e3)}`,
  department: l[Math.floor(n() * l.length)], salary: Math.floor(n() * 8e4) + 4e4 }));
const expected = {}; for (const d of l) { const h = s.filter(g => g.department === d); expected[d] = Math.round(h.reduce((f, y) => f + y.salary, 0) / h.length); }
console.log(JSON.stringify({ expected, rows: s }));
