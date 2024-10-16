from fastapi.testclient import TestClient
import sys
import os
from fastapi.testclient import TestClient

# Add the project root to the PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from chat_api.src.main import app

client = TestClient(app)


def test_chat_endpoint():
    response = client.post("/chat", json={"message": "Hello, how are you?"})
    assert response.status_code == 200
    # Further assertions can be made based on the expected response content
