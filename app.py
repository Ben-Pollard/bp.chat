"""Streamlit app for interacting with an LLM"""
import streamlit as st
from chain_module import chain  # Import the chain from the new module

def main():
    st.title("LLM Chain Invocation App")

    # Input text box for user messages
    user_input = st.text_area("Enter your message:", "")

    if st.button("Invoke Chain"):
        # Invoke the chain with user input
        result = chain.invoke({"messages": user_input})

        # Display the result
        st.write("Response:", result)

if __name__ == "__main__":
    main()
