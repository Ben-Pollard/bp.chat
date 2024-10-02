"""Streamlit app for interacting with an LLM"""
import streamlit as st
from chain_setup import chain  # Import the chain from the new module
from langchain_core.messages import AIMessage, HumanMessage

def main():
    st.title("LLM Chain Invocation App")

    # session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    
    # Input for user messages
    user_input = st.chat_input("Your message:")
    if user_input is not None and user_input != "":
        st.session_state.chat_history.append(HumanMessage(content=user_input))

        with st.chat_message("Human"):
            st.markdown(user_input)

        with st.chat_message("AI"):
            stream = chain.stream({"input": user_input}, {"configurable": {"session_id": "unused"}})
            response = st.write_stream(stream)

        st.session_state.chat_history.append(AIMessage(content=response))


if __name__ == "__main__":
    main()
