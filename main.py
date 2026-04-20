# import os
# from dotenv import load_dotenv

# load_dotenv()

# # Verify Mistral Key
# if not os.getenv("MISTRAL_API_KEY"):
#     print("❌ ERROR: MISTRAL_API_KEY not found in .env")
# else:
#     print("✅ Mistral API Key loaded.")
#     from src.agent import app

#     def run_formatter(bad_text):
#         inputs = {
#             "raw_input": bad_text,
#             "json_output": None,
#             "errors": [],
#             "iterations": 0
#         }
#         final_state = app.invoke(inputs)
#         print("\n--- FINAL CLEAN JSON ---")
#         print(final_state["json_output"])

#     if __name__ == "__main__":
#         # Testing with a very broken string
#         dirty_data = "name: Ahmad, city: Okara, degree: BSCS missing braces"
#         run_formatter(dirty_data)



import os
import subprocess
import json
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("MISTRAL_API_KEY"):
    print("❌ ERROR: MISTRAL_API_KEY not found in .env")
else:
    print("✅ Mistral API Key loaded.")
    # Your existing formatter import
    # from src.agent import app 

    def run_sql_agent(question):
        """Calls the Node.js SQL Agent and returns the data"""
        try:
            # We run the node command and pass the question as an argument
            result = subprocess.run(
                ['node', 'index.js', question],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(__file__)
            )

            # Prefer stdout (normal output). If empty, attempt to surface stderr for debugging.
            stdout = (result.stdout or "").strip()
            stderr = (result.stderr or "").strip()

            if stdout:
                try:
                    return json.loads(stdout)
                except Exception as e:
                    return {"error": "Failed to parse JSON from SQL Agent stdout", "parseError": str(e), "stdout": stdout}

            if stderr:
                # Sometimes Node prints errors to stderr; try to parse JSON there too.
                try:
                    return json.loads(stderr)
                except Exception:
                    return {"error": "No stdout from SQL Agent", "stderr": stderr, "returncode": result.returncode}

            return {"error": "No output from SQL Agent", "returncode": result.returncode}
        except Exception as e:
            return {"error": str(e)}

    def run_formatter(bad_text):
        # ... your existing logic for the formatter ...
        print(f"Formatting: {bad_text}")

    if __name__ == "__main__":
        # Example 1: Run Formatter
        run_formatter("name: Ahmad, city: Okara")

        # Example 2: Run SQL Agent
        print("\n--- RUNNING SQL AGENT ---")
        user_query = "Who are the employees with salary > 45000?"
        data = run_sql_agent(user_query)
        
        print("Final Database Result:")
        print(json.dumps(data, indent=2))
