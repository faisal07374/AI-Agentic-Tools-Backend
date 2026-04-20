// nodes/generator.js
import { Mistral } from '@mistralai/mistralai';
const client = new Mistral({ apiKey: process.env.MISTRAL_API_KEY });

export async function sqlGeneratorNode(state) {
  const prompt = `You are a SQLite expert. 
  Schema: employees (id, name, role, salary)
  Question: ${state.question}
  ${state.error ? `Previous error: ${state.error}. Fix the SQL.` : ""}
  Return ONLY the raw SQL query. No markdown, no backticks.`;

  const res = await client.chat.complete({
    model: "mistral-small-latest",
    messages: [{ role: "user", content: prompt }],
  });

  let sql = res.choices[0].message.content.trim();
  // Clean up backticks if Mistral adds them
  sql = sql.replace(/```sql|```/g, "").trim();

  return { ...state, sqlQuery: sql };
}