"""Tests for the outer chat chain"""

from chat.chain_setup import StreamParser, ChatCoT
from chat.app import ChatApp


def test_json_patch_streaming():
    """Test to extract utterance as text stream from jsonpatch stream"""

    fake_json_patches = [
        [{"op": "add", "path": "/utterance", "value": ""}],
        [{"op": "replace", "path": "/utterance", "value": "Hello"}],
        [{"op": "replace", "path": "/utterance", "value": "Hello, how "}],
        [{"op": "replace", "path": "/utterance", "value": "Hello, how are "}],
        [{"op": "replace", "path": "/utterance", "value": "Hello, how are you?"}],
    ]

    parser = StreamParser(ChatCoT)
    messages = parser.json_diff_extractor(fake_json_patches)

    # Collect the streamed utterance
    collected_stream = "".join([i["utterance"] for i in messages])

    # Assert the final streamed utterance is as expected
    assert collected_stream == "Hello, how are you?"


def test_response_display():
    """Test displaying response messages"""

    fake_messages = [
        {"strategy": "greet "},
        {"strategy": "user"},
        {"utterance": "Hello "},
        {"utterance": "there"},
    ]

    app = ChatApp(session_id=1)

    app.display_response(fake_messages)

    # Collect the streamed utterance
    last_msg = app.session_state.chat_history[-1]

    # Assert the final streamed utterance is as expected
    assert last_msg.content == "Hello there"
