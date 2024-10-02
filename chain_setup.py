import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

ephemeral_chat_history = ChatMessageHistory()


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability.",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
    ]
)

model = ChatOpenAI(
    temperature=0,
    model_name="gpt-3.5-turbo",
    openai_api_key=os.environ["OPENAI_API_KEY"],
)

parser = StrOutputParser()

# Chain initialization
chain = RunnableWithMessageHistory(
    prompt | model | parser,
    lambda session_id: ephemeral_chat_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)