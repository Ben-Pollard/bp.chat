"""Streamlit app for interacting with an LLM.

This app allows users to input messages and receive responses from a language model chain.
The responses are streamed in real-time to the display.
"""

from typing import Dict, Iterable

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from chat.chain_setup import ChatAssistant


class ChatApp:
    def __init__(self, session_id: int) -> None:
        """Initialize the ChatApp with a ChatAssistant and session state."""
        self.session_id = session_id
        self.chat_assistant = ChatAssistant()
        self.initialise_session_state()

        # layout
        self.column_chat, self.column_metachat = st.columns([3, 1])

    def initialise_session_state(self) -> None:
        """Initialize the session state for chat history."""
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

    def display_chat_history(self) -> None:
        """Display the chat history from the session state."""
        for message in st.session_state.chat_history:
            if isinstance(message, HumanMessage):
                self.display_message("Human", message.content)
            elif isinstance(message, AIMessage):
                self.display_message("AI", message.content)

    def display_message(self, sender: str, content: str) -> None:
        """Display a message in the chat.

        Args:
            sender (str): The sender of the message, either 'Human' or 'AI'.
            content (str): The content of the message to display.
        """
        with self.column_chat:
            with st.chat_message(sender):
                st.write(content)

    def display_meta_message(self, text: str) -> None:
        """Display metadata in the designated meta column."""
        with self.column_metachat:
            with st.chat_message:
                st.write(text)

    def get_user_input(self) -> str:
        """Get user input from the chat input field.

        Returns:
            str: The user's input message.
        """
        return st.chat_input("Your message:")

    def handle_user_input(self, user_input: str) -> None:
        """Handle the user's input by updating chat history and streaming responses.

        Args:
            user_input (str): The input message from the user.
        """
        self.display_message("Human", user_input)
        st.session_state.chat_history.append(HumanMessage(content=user_input))

        response = self.get_response(user_input)
        self.display_response(response)

    def get_response(self, user_input: str) -> Iterable[Dict]:
        """Get the response stream from the backend"""
        config = {"configurable": {"session_id": self.session_id}}

        try:
            return self.chat_assistant.chain.stream({"input": user_input}, config)
        except Exception as e:
            st.error(f"Error in response stream {e}")
            return []

    def display_response(self, response: Iterable[Dict]) -> None:
        """Display the response from the chat assistant.

        Args:
            response (Iterable[Dict]): The response data to display.
        """

        # Create a placeholder at the END of the chat for AI's response
        with self.column_chat:
            with st.chat_message("AI"):
                message_placeholder = st.empty()

        # Create a placeholder for metadata in the metachat column (outside the AI container)
        with self.column_metachat:
            meta_placeholder = st.empty()

        utterance = ""

        for msg in response:
            if "utterance" in msg:
                utterance += msg["utterance"]
                message_placeholder.markdown(utterance)
            else:
                meta_placeholder.markdown(msg)

        # Append the complete AI message to the chat history
        st.session_state.chat_history.append(AIMessage(content=utterance))

    def run(self) -> None:
        """Run the chat application, displaying chat history and handling user input."""
        user_input = self.get_user_input()
        self.display_chat_history()

        if user_input:
            self.handle_user_input(user_input)


if __name__ == "__main__":
    app = ChatApp(session_id=1)
    app.run()
