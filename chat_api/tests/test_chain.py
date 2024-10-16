"""Tests for the outer chat chain"""

from api.chain_setup import StreamParser, ChatCoT


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
