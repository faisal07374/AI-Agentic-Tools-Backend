import json
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage

# Use your key directly here to ensure the 500 error goes away
llm = ChatMistralAI(
    model="mistral-large-latest", 
    temperature=0,
    mistral_api_key="C12z7oDjTI2ZrG8tQ7ELkkv7G9V7JSnc" # Hardcoded for now
)

def format_json_node(state):
    print(f"--- MISTRAL ATTEMPT {state['iterations'] + 1} ---")
    
    error_feedback = f"\nPrevious JSON Error: {state['errors'][-1]}" if state['errors'] else ""
    
    prompt = [
        SystemMessage(content="You are a JSON repair expert. Output ONLY valid raw JSON. No markdown, no backticks, no explanations."),
        HumanMessage(content=f"Fix this text into valid JSON:\n{state['raw_input']}{error_feedback}")
    ]
    
    # Try-Except block to see the actual error in the console
    try:
        response = llm.invoke(prompt)
        return {
            "json_output": response.content.strip(),
            "iterations": state['iterations'] + 1
        }
    except Exception as e:
        print(f"Mistral API Error: {e}")
        raise e

def validate_json_node(state):
    try:
        # Mistral sometimes adds markdown blocks like ```json
        clean_content = state['json_output'].replace("```json", "").replace("```", "").strip()
        json.loads(clean_content)
        return {"errors": [], "json_output": clean_content} 
    except Exception as e:
        return {"errors": [str(e)]}