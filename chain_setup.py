"""The outer chat chain"""
import os
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.schema.runnable import RunnableGenerator

ephemeral_chat_history = ChatMessageHistory()

SYSTEM_PROMPT = """Your task is to carry out a mental health diagnostic conversation. You can ask questions and should direct the conversation toward reaching your goal of generating information that can be reviewed by a human mental health professional. As a bot you may not suggest or propose a diagnosis to the user. Your questions and responses must be very simple and short.

{format_instructions}"""

class ChatCoT(BaseModel):
    """Chain of thought for the chat response"""
    target_info: str = Field(description="The information you are seeking")
    strategy: str = Field(description="Your strategy for engaging the user")
    utterance: str = Field(description="Your response to the user")

parser = PydanticOutputParser(pydantic_object=ChatCoT)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

model = ChatOpenAI(
    temperature=0,
    model_name="gpt-3.5-turbo",
    openai_api_key=os.environ["OPENAI_API_KEY"],
)

# Chain initialization
chain_with_message_history = RunnableWithMessageHistory(
    prompt | model,
    lambda session_id: ephemeral_chat_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

def _transform(input_stream):
    for chunk in input_stream:
        yield chunk['output']

chain = chain_with_message_history | RunnableGenerator(_transform)
