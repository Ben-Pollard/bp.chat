"""Streamlit app for interacting with an LLM.

This app allows users to input messages and receive responses from a language model chain.
The responses are streamed in real-time to the display.
"""

from typing import Dict, Iterable

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from chat.chain_setup import ChatAssistant


class ChatApp:
    def __init__(self, session_id) -> None:
        self.session_id = session_id
        self.session_state = st.session_state
        self.chat_assistant = ChatAssistant()
        self.initialise_session_state()
        self.column_chat, self.column_metachat = st.columns([3, 1])

    def initialise_session_state(self):
        st.title("LLM Chain Invocation App")
        st.session_state.chat_history = []

    def display_chat_history(self):
        for message in st.session_state.chat_history:
            if isinstance(message, HumanMessage):
                self.display_message("Human", message.content)
            elif isinstance(message, AIMessage):
                self.display_message("AI", message.content)

    def get_user_input(self):
        return st.chat_input("Your message:")

    def handle_user_input(self, user_input):
        st.session_state.chat_history.append(HumanMessage(content=user_input))
        self.display_message("Human", user_input)
        response = self.get_response(user_input)
        self.display_response(response)

    def get_response(self, user_input):
        config = {"configurable": {"session_id": self.session_id}}
        return self.chat_assistant.chain.stream({"input": user_input}, config)

    def display_ai_response(self, text):
        with self.column_chat:
            with st.chat_message("AI"):
                st.write(text)

    def display_message(self, sender, content):
        with st.chat_message(sender):
            st.markdown(content)

    def display_response_meta(self, text):
        with self.column_metachat:
            st.markdown(text)

    def display_response(self, response: Iterable[Dict]):
        utterance = ""
        response = list(response)
        for msg in response:
            if "utterance" in msg:
                utterance += msg["utterance"]
                self.display_ai_response(msg["utterance"])
            else:
                self.display_response_meta(msg)

        self.session_state.chat_history.append(AIMessage(content=utterance))

    def run(self):
        self.display_chat_history()
        user_input = self.get_user_input()
        if user_input:
            self.handle_user_input(user_input)


if __name__ == "__main__":
    app = ChatApp(session_id=1)
    app.run()
