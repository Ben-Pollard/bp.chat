"""Tests including calls to real LLM"""

from fastapi.testclient import TestClient
from chat_api.src.main import app


def test_chain_invocation(chat_assistant):
    """Test if the chain returns a non-empty string for a given input."""
    # Example input to test the chain
    user_input = "Hello, how are you?"

    # Invoke the chain and check the result
    result = chat_assistant.chain.invoke(
        {"input": user_input}, {"configurable": {"session_id": "unused"}}
    )

    # Assert that the result is a non-empty string
    assert isinstance(result, dict)
    assert len(result) > 0


def test_chat_endpoint():
    client = TestClient(app)
    response = client.post("/chat", json={"message": "Hello, how are you?"})
    assert response.status_code == 200
