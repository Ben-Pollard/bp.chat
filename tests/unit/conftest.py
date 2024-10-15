import pytest
from unittest.mock import Mock
from streamlit.testing.v1 import AppTest
from chat.app import ChatApp


@pytest.fixture()
def at():
    """Fixture that prepares the Streamlit app tests"""
    yield AppTest.from_function(lambda x: ChatApp(session_id=1).run())
