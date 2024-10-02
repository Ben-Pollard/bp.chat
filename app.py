"""Streamlit app for interacting with an LLM"""
import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Base templates for vector store prompts
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability.",
        ),
        ("placeholder", "{messages}"),
    ]
)

model = ChatOpenAI(
    temperature=0,
    model_name="gpt-3.5-turbo",
    openai_api_key=os.environ["OPENAI_KEY"],
)

parser = StrOutputParser()

chain = prompt | model | parser
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
