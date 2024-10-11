"""The outer chat chain"""

import os
from typing import Any, Iterator, Optional, Type, Dict, List
import jsonpatch
from langchain.schema.runnable import RunnableGenerator
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.globals import set_debug
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import Runnable
from langchain_core.runnables.config import RunnableConfig
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.utils import Input, Output
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

set_debug(True)


class StreamParser(Runnable):
    """Runnable to apply a jsonpatch parser when streaming and yield field diffs."""

    def __init__(self, model_class: Type[BaseModel]):
        self.model_fields = model_class.model_fields

    def invoke(
        self,
        input: Input,  # pylint: disable=W0622
        config: Optional[RunnableConfig] = None,
    ) -> Output:
        return input

    def stream(
        self,
        input: Iterator[List[Dict[str, Any]]],  # pylint: disable=W0622
        config: Optional[RunnableConfig] = None,
        **kwargs: Optional[Any]
    ) -> Iterator[Dict[str, str]]:
        generator = RunnableGenerator(self.json_diff_extractor)
        return generator.stream(input)

    def json_diff_extractor(self, input: Input):  # pylint: disable=W0622
        """Extract diff of chosen fields from jsonpatch stream."""
        current_json = {}
        previous_str = {field: "" for field in self.model_fields}
        for op in input:
            json_patch = jsonpatch.JsonPatch(op)
            current_json = json_patch.apply(current_json)
            for field in self.model_fields:
                if field in current_json:
                    new_str = current_json[field]
                    diff = new_str[len(previous_str[field]) :]
                    previous_str[field] = new_str
                    yield {field: diff}


class ChatCoT(BaseModel):
    """Chain of thought for the chat response"""

    target_info: str = Field(description="The information you are seeking")
    strategy: str = Field(description="Your strategy for engaging the user")
    utterance: str = Field(description="Your response to the user")


class ChatAssistant:
    """Chat chain for user interaction"""

    def __init__(self) -> None:

        user_chat_history = ChatMessageHistory()

        system_prompt = "Your task is to carry out a mental health diagnostic conversation. You can ask questions and should direct the conversation toward reaching your goal of generating information that can be reviewed by a human mental health professional. As a bot you may not suggest or propose a diagnosis to the user. Your questions and responses must be very simple and short."  # pylint: disable=C0301

        prompt_template = system_prompt + "\n\n{format_instructions}" ""

        pydantic_parser = PydanticOutputParser(pydantic_object=ChatCoT)
        json_diff_parser = JsonOutputParser(diff=True, pydantic_object=ChatCoT)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt_template),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
            ]
        ).partial(format_instructions=pydantic_parser.get_format_instructions())

        model = ChatOpenAI(
            temperature=0,
            model_name="gpt-3.5-turbo",
            openai_api_key=os.environ["OPENAI_API_KEY"],
            streaming=True,
        )

        # Chain initialization
        chain_with_message_history = RunnableWithMessageHistory(
            prompt | model | json_diff_parser | StreamParser(ChatCoT),
            lambda session_id: user_chat_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

        self.chain = chain_with_message_history
