"""Tests including calls to real LLM"""

from fastapi.testclient import TestClient
import httpx


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
    url = "http://127.0.0.1:8000/chat"

    response = []

    with httpx.stream("POST", url, json={"message": "Hello, how are you?"}) as r:
        for chunk in r.iter_raw():
            response.append(chunk)

    assert response[0].status_code == 200
