"""Tests for the outer chat chain"""

from chain_setup import ChatAssistant


def test_chain_invocation():
    """Test if the chain returns a non-empty string for a given input."""
    # Example input to test the chain
    user_input = "Hello, how are you?"

    # Invoke the chain and check the result
    result = ChatAssistant().chain.invoke(
        {"input": user_input}, {"configurable": {"session_id": "unused"}}
    )

    # Assert that the result is a non-empty string
    assert isinstance(result, dict)
    assert len(result) > 0
