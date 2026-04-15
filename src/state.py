from typing import TypedDict, Annotated, List

class AgentState(TypedDict):
    raw_input: str
    json_output: str
    errors: List[str]
    iterations: int