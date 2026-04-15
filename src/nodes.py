import os
import json
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

# 1. Load the .env file (this works for your local laptop)
load_dotenv()

# 2. Get the key from the environment (Render OR .env)
# This prevents your app from crashing if the key isn't hardcoded
api_key = os.getenv("MISTRAL_API_KEY")

llm = ChatMistralAI(
    model="mistral-large-latest", 
    temperature=0,
    mistral_api_key=api_key 
)

def format_json_node(state):
    print(f"--- MISTRAL ATTEMPT {state['iterations'] + 1} ---")
    
    # Check if we have an error from a previous loop
    error_feedback = ""
    if state['errors']:
        error_feedback = f"\n\nIMPORTANT: Your last attempt failed with this error: {state['errors'][-1]}. Please fix it."
    
    prompt = [
        SystemMessage(content="You are a JSON repair expert. Output ONLY valid raw JSON. No markdown backticks, no text before or after."),
        HumanMessage(content=f"Fix this text into valid JSON:\n{state['raw_input']}{error_feedback}")
    ]
    
    try:
        response = llm.invoke(prompt)
        # We strip backticks just in case the LLM ignores the SystemMessage
        content = response.content.strip().replace("```json", "").replace("```", "")
        
        return {
            "json_output": content,
            "iterations": state['iterations'] + 1
        }
    except Exception as e:
        print(f"Mistral API Error: {e}")
        # In production, we don't want the server to crash, we want to return the error to the state
        return {
            "errors": [f"API Error: {str(e)}"],
            "iterations": state['iterations'] + 1
        }

def validate_json_node(state):
    # If the formatter already reported an API error, skip validation
    if state['errors'] and "API Error" in state['errors'][-1]:
        return {"errors": state['errors']}

    try:
        # Final safety check on the string
        json_str = state['json_output']
        json.loads(json_str)
        return {"errors": [], "json_output": json_str} 
    except Exception as e:
        return {"errors": [str(e)]}