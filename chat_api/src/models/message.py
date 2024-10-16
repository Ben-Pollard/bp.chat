from pydantic import BaseModel
from typing import Dict


class Message(BaseModel):
    content: Dict[str, str]


class StreamRequest(BaseModel):
    """Request body for streaming."""

    message: str
