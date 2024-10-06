"""Tests for the outer chat chain"""

from chat.chain_setup import StreamParser


def test_json_patch_streaming():
    """Test to extract utterance as text stream from jsonpatch stream"""

    fake_json_patches = [
        [{"op": "add", "path": "/utterance", "value": ""}],
        [{"op": "replace", "path": "/utterance", "value": "Hello"}],
        [{"op": "replace", "path": "/utterance", "value": "Hello, how "}],
        [{"op": "replace", "path": "/utterance", "value": "Hello, how are "}],
        [{"op": "replace", "path": "/utterance", "value": "Hello, how are you?"}],
    ]

    parser = StreamParser("utterance")
    utterance_stream = parser.json_diff_extractor(fake_json_patches)

    # Collect the streamed utterance
    collected_stream = "".join([i for i in utterance_stream])

    # Assert the final streamed utterance is as expected
    assert collected_stream == "Hello, how are you?"
