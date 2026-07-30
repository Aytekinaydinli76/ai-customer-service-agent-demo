from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def classify(message: str) -> dict:
    response = client.post("/agent/respond", json={"message": message})
    assert response.status_code == 200
    return response.json()


def test_routes_booking_request() -> None:
    result = classify("I would like to book an appointment. What is available?")
    assert result["intent"] == "create_appointment"
    assert result["requires_human"] is False
    assert result["next_action"] == "collect_service_and_date"


def test_prioritizes_cancellation_over_generic_appointment_word() -> None:
    result = classify("Please cancel my appointment because I cannot come.")
    assert result["intent"] == "cancel_appointment"
    assert result["next_action"] == "request_appointment_reference"


def test_routes_explicit_human_request() -> None:
    result = classify("This is urgent. I need to speak with a human manager.")
    assert result["intent"] == "human_handoff"
    assert result["requires_human"] is True


def test_unknown_intent_fails_safely() -> None:
    result = classify("The blue sky is interesting today.")
    assert result["intent"] == "unknown"
    assert result["requires_human"] is True
    assert result["confidence"] < 0.5


def test_rejects_empty_messages() -> None:
    response = client.post("/agent/respond", json={"message": ""})
    assert response.status_code == 422
