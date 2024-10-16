from fastapi.testclient import TestClient
from chat_api.src.main import app

client = TestClient(app)


def test_chat_endpoint():
    response = client.post("/chat", json={"message": "Hello, how are you?"})
    assert response.status_code == 200
    # Further assertions can be made based on the expected response content
