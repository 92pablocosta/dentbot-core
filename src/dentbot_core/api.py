from fastapi import FastAPI
from pydantic import BaseModel

from dentbot_core.decision import make_decision


class DecisionRequest(BaseModel):
    message: str


app = FastAPI()


@app.post("/decisions")
def create_decision(request: DecisionRequest):
    decision = make_decision(request.message)

    return {
        "intent": decision.intent,
        "action": decision.action,
        "message": decision.message,
    }

