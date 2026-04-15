from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from src.agent import app as agent_app  # Importing your agent
import os
from dotenv import load_dotenv

load_dotenv()

api = FastAPI()

# --- IMPORTANT FOR REACT ---
# This allows your React app (usually on localhost:3000) to talk to FastAPI
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define what the request should look like
class JSONRequest(BaseModel):
    text: str

@api.post("/format-json")
async def format_json_endpoint(request: JSONRequest):
    try:
        # Prepare the input for your LangGraph agent
        inputs = {
            "raw_input": request.text,
            "json_output": None,
            "errors": [],
            "iterations": 0
        }
        
        # Run the agent
        result = agent_app.invoke(inputs)
        
        return {
            "status": "success",
            "original": request.text,
            "formatted_json": result["json_output"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8000)