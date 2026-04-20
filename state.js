// state.js
export const AgentState = {
  question: "",      // User input
  sqlQuery: "",      // Current SQL draft
  results: null,     // DB Output
  error: null,       // Any SQL errors
  iterations: 0      // To prevent infinite loops
};