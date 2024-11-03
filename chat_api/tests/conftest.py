from typing import Iterator, Dict

import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from chat_api.src.chains.chat_assistant import ChatAssistant
from chat_api.src import main


@pytest.fixture
def mock_chain_stream() -> Iterator[Dict[str, str]]:
    """Mocking the result of calling chat.stream"""
    return [{"utterance": "hello"}, {"utterance": "there"}]


@pytest.fixture
def chat_assistant(mock_chain_stream):
    """Chat assistant class defining the primary chain"""
    with patch(
        "chat_api.src.chains.chat_assistant.RunnableWithMessageHistory.stream",
        return_value=mock_chain_stream,
    ):
        chat_assistant = ChatAssistant()
        return chat_assistant


@pytest.fixture
def app(chat_assistant):
    with patch.object(main, "chat_assistant", return_value=chat_assistant):
        return main.app


@pytest.fixture
def client(app):
    """Test client for the fastapi app"""
    return TestClient(app)
