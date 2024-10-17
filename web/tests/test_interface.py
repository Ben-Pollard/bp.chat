from unittest.mock import patch

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage


def test_human_message_input(chat_app, mock_get_response):
    """Test entering a human chat message and receiving a response."""
    with patch.object(
        chat_app.api_client, "get_response", return_value=mock_get_response
    ):
        # Simulate user input
        user_input = "Hi"
        chat_app.handle_user_input(user_input)

        # Check if the human message is added to chat history
        assert any(
            isinstance(msg, HumanMessage) and msg.content == "Hi"
            for msg in st.session_state.chat_history
        )

        # Check if the AI response is added to chat history
        assert any(
            isinstance(msg, AIMessage) and "bot utterance" in msg.content
            for msg in st.session_state.chat_history
        )
