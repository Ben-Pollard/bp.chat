from fastapi.testclient import TestClient


def test_chat_endpoint(client: TestClient):
    response = client.get("/chat", params={"message": "Hello, how are you?"})
    assert response.status_code == 200
