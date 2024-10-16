import os
from typing import Any, Dict, Iterator, List, Optional, Type

import jsonpatch
from langchain.schema.runnable import RunnableGenerator
from langchain_core.runnables.base import Runnable
from langchain_core.runnables.config import RunnableConfig
from langchain_core.runnables.utils import Input, Output
from pydantic import BaseModel


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
