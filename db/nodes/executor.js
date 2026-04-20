// nodes/executor.js
import sqlite3 from 'sqlite3';

export async function sqlExecutorNode(state) {
  // Use the seeded database at the workspace root
  const db = new sqlite3.Database('../db/company.sqlite');

  return new Promise((resolve) => {
    db.all(state.sqlQuery, [], (err, rows) => {
      db.close(); // Always close connection
      if (err) {
        resolve({ ...state, error: err.message, results: null });
      } else {
        resolve({ ...state, results: rows, error: null });
      }
    });
  });
}