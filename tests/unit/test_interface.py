from unittest.mock import patch
import pytest
import streamlit as st
from tests.unit.conftest import at, mock_get_response


def test_human_message_input(at, mock_get_response):
    """Test entering a human chat message and receiving a response."""
    with patch('chat.app.ChatApp.get_response', return_value=mock_get_response):
        # Simulate user input
        st.session_state.chat_history = []
        at.run()
        st.session_state.chat_history.append("Hello, AI!")

        # Check if the human message is added to chat history
        assert any(isinstance(msg, str) and msg == "Hello, AI!" for msg in st.session_state.chat_history)

        # Check if the AI response is added to chat history
        assert any(isinstance(msg, str) and "bot utterance" in msg for msg in st.session_state.chat_history)


def test_app_starts(at):
    """Verify the app starts without errors"""
    assert not at.exception
