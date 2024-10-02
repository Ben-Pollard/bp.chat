"""Streamlit app for interacting with an LLM"""
import streamlit as st
from chain_setup import chain  # Import the chain from the new module

def main():
    st.title("LLM Chain Invocation App")

    # Input text box for user messages
    user_input = st.text_area("Enter your message:", "")

    if st.button("Invoke Chain"):
        # Stream the chain with user input
        response_stream = chain.stream({"input": user_input}, {"configurable": {"session_id": "unused"}})

        # Display the streamed result
        result = ""
        for chunk in response_stream:
            result += chunk
            st.write("Response:", result)

if __name__ == "__main__":
    main()
