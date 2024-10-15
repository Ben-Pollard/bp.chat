import pytest

@pytest.fixture
def mock_get_response():
    """Fixture to mock the get_response method."""
    return iter([
        {"target_info": "partial target info"},
        {"strategy": "partial strategy"},
        {"utterance": "partial utterance"}
    ])
