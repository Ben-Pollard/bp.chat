from typing import Dict


class Message:
    def __init__(
        self,
        content: str,
        additional_kwargs: Dict = None,
        response_metadata: Dict = None,
    ) -> None:
        self.content = content
        self.additional_kwargs = additional_kwargs
        self.response_metadata = response_metadata


class HumanMessage(Message):
    pass


class AIMessage(Message):
    pass
