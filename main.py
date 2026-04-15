import os
from dotenv import load_dotenv

load_dotenv()

# Verify Mistral Key
if not os.getenv("MISTRAL_API_KEY"):
    print("❌ ERROR: MISTRAL_API_KEY not found in .env")
else:
    print("✅ Mistral API Key loaded.")
    from src.agent import app

    def run_formatter(bad_text):
        inputs = {
            "raw_input": bad_text,
            "json_output": None,
            "errors": [],
            "iterations": 0
        }
        final_state = app.invoke(inputs)
        print("\n--- FINAL CLEAN JSON ---")
        print(final_state["json_output"])

    if __name__ == "__main__":
        # Testing with a very broken string
        dirty_data = "name: Ahmad, city: Okara, degree: BSCS missing braces"
        run_formatter(dirty_data)