from fastapi.testclient import TestClient

from server.src.main import app
from server.src.v1.debate import get_debate_service


class FakeDebateService:
    async def run(self, topic: str, groq_api_key: str):
        return {
            "topic": topic,
            "conversation_history": [
                {"agent": "pro", "message": "A concise pro argument."},
                {"agent": "against", "message": "A concise against argument."},
            ],
            "verdict": {
                "winner": "pro",
                "reasoning": "The pro side used clearer evidence.",
                "pro_score": 8.0,
                "against_score": 7.0,
            },
            "supporting_evidence": {
                "argument": "The strongest argument.",
                "evidence": [
                    {
                        "text": "A factual claim.",
                        "url": "https://example.com/source",
                    }
                ],
                "confidence": 0.8,
            },
        }


def test_run_debate_route_returns_success_response():
    app.dependency_overrides[get_debate_service] = lambda: FakeDebateService()

    try:
        client = TestClient(app)
        response = client.post(
            "/api/v1/debate",
            json={
                "topic": "Should AI replace software engineers?",
                "groq_api_key": "test-key",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["topic"] == "Should AI replace software engineers?"
    assert body["data"]["transcript"][1]["agent"] == "against"
    assert body["data"]["supporting_evidence"]["confidence"] == 0.8
