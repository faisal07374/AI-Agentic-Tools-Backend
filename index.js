// index.js
import 'dotenv/config';
import { sqlGeneratorNode } from './db/nodes/generator.js';
import { sqlExecutorNode } from './db/nodes/executor.js';

async function main() {
  const userQuestion = process.argv[2] || "Show all employees";

  let state = {
    question: userQuestion,
    sqlQuery: "",
    results: null,
    error: null,
    iterations: 0
  };

  try {
    while (state.iterations < 3) {
      state = await sqlGeneratorNode(state);
      state = await sqlExecutorNode(state);

      if (!state.error) {
        // Output the result and the generated SQL as JSON for Python to read
        console.log(JSON.stringify({ sqlQuery: state.sqlQuery, results: state.results, error: null }));
        process.exit(0); // Exit successfully
      }
      
      state.iterations++;
    }
    // If we reach here, it means we failed after 3 tries
    console.log(JSON.stringify({ error: "Agent could not fix SQL", lastError: state.error, sqlQuery: state.sqlQuery }));
  } catch (globalError) {
    console.log(JSON.stringify({ error: "System Crash", details: globalError.message }));
  }
}

main();