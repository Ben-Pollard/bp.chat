from fastapi.testclient import TestClient


def test_chat_endpoint(client: TestClient):
    response = client.post("/chat", json={"message": "Hello, how are you?"})
    assert response.status_code == 200
