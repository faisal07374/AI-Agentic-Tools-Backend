from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from src.agent import app as agent_app  # Importing your agent
import os
from dotenv import load_dotenv
import subprocess
import json

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


class SQLRequest(BaseModel):
    question: str

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


def run_sql_agent(question: str):
    """Run the Node.js SQL agent (index.js) and return parsed JSON result or error info."""
    try:
        result = subprocess.run(
            ['node', 'index.js', question],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(__file__)
        )

        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()

        if stdout:
            try:
                return json.loads(stdout)
            except Exception:
                return {"error": "Failed to parse SQL agent stdout", "stdout": stdout}

        if stderr:
            try:
                return json.loads(stderr)
            except Exception:
                return {"error": "SQL agent error", "stderr": stderr, "returncode": result.returncode}

        return {"error": "No output from SQL agent", "returncode": result.returncode}
    except Exception as e:
        return {"error": str(e)}


@api.post("/sql-query")
async def sql_query_endpoint(request: SQLRequest):
    try:
        result = run_sql_agent(request.question)
        return {"status": "success", "query": request.question, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8000)