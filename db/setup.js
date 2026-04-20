import sqlite3 from 'sqlite3';
import fs from 'fs';

// Ensure the db folder exists
if (!fs.existsSync('./db')) fs.mkdirSync('./db');

const db = new sqlite3.Database('./db/company.sqlite');

db.serialize(() => {
  db.run("CREATE TABLE employees (id INTEGER, name TEXT, role TEXT, salary INTEGER)");
  db.run("INSERT INTO employees VALUES (1, 'Ahmad', 'MERN Developer', 50000)");
  db.run("INSERT INTO employees VALUES (2, 'Sara', 'AI Engineer', 75000)");
  db.run("INSERT INTO employees VALUES (3, 'Zain', 'Designer', 40000)");
  
  console.log("Database created and seeded!");
  db.close();
});