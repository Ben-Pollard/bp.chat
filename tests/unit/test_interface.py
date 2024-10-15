import unittest
from unittest.mock import patch
import streamlit as st
from streamlit.testing import TestRunner
from chat.app import ChatApp

class TestChatInterface(unittest.TestCase):
    @patch('chat.app.ChatAssistant')
    def test_chat_display_order(self, MockChatAssistant):
        # Mock the ChatAssistant to control responses
        mock_assistant = MockChatAssistant.return_value
        mock_assistant.get_response.side_effect = [
            [{"utterance": "Hello, how can I help you?"}],
            [{"utterance": "Sure, I can do that!"}]
        ]

        # Create a ChatApp instance
        chat_app = ChatApp(session_id=1)

        # Simulate user inputs
        user_inputs = ["Hi", "Can you help me?"]
        expected_display = [
            ("Human", "Hi"),
            ("AI", "Hello, how can I help you?"),
            ("Human", "Can you help me?"),
            ("AI", "Sure, I can do that!")
        ]

        # Use Streamlit's TestRunner to simulate the app
        with TestRunner(chat_app.run) as runner:
            for user_input in user_inputs:
                runner.input(user_input)
                runner.run()

            # Verify the chat history
            chat_history = st.session_state.chat_history
            actual_display = [(msg.sender, msg.content) for msg in chat_history]

            self.assertEqual(actual_display, expected_display)

if __name__ == '__main__':
    unittest.main()
