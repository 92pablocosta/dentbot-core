from fastapi.testclient import TestClient

from dentbot_core.api import app


client = TestClient(app)


def test_creates_pricing_decision():
    response = client.post(
        "/decisions",
        json={"message": "Qual é o valor da consulta?"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "intent": "pricing_question",
        "action": "pricing_response",
        "message": "A consulta custa R$ 250. Os demais serviços são avaliados durante a consulta.",
    }
