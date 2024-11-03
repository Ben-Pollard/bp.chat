from typing import Dict, Iterable

import pytest
from web.src.app import ChatApp
from web.src.api_client import ApiClient


@pytest.fixture
def chat_app():
    """Fixture to initialize the ChatApp."""
    return ChatApp(session_id=1)


@pytest.fixture
def mock_get_response() -> Iterable[Dict]:
    """Fixture to mock the get_response method."""
    return iter(
        [
            {"target_info": "target "},
            {"target_info": "info"},
            {"strategy": "strategy"},
            {"utterance": "bot "},
            {"utterance": "utterance"},
        ]
    )


@pytest.fixture
def api_client():
    base_url = "http://localhost:8000"
    return ApiClient(base_url)
