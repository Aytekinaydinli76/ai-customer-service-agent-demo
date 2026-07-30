from fastapi import FastAPI

from .agent import classify
from .schemas import AgentRequest, AgentResponse

app = FastAPI(
    title="AI Customer Service Agent Demo",
    version="1.0.0",
    description=(
        "A safe, testable customer-service intent router for appointment and "
        "business workflows. It runs without external AI credentials."
    ),
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "mode": "local-mock"}


@app.post("/agent/respond", response_model=AgentResponse, tags=["agent"])
def respond(payload: AgentRequest) -> AgentResponse:
    return classify(payload.message)
