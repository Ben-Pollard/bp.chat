"""Tests for the outer chat chain"""

from chain_setup import StreamParser


def test_json_patch_streaming():
    """Unittest for streaming json parser"""

    patches = [
        [{"op": "add", "path": "/reasoning", "value": ""}],
        [{"op": "replace", "path": "/reasoning", "value": "The "}],
        [{"op": "replace", "path": "/reasoning", "value": "The chatbot "}],
        [{"op": "replace", "path": "/reasoning", "value": "The chatbot evaluates "}],
        [
            {
                "op": "replace",
                "path": "/reasoning",
                "value": "The chatbot evaluates user inputs.",
            }
        ],  # pylint: disable=C0301
        [{"op": "add", "path": "/utterance", "value": ""}],
        [{"op": "replace", "path": "/utterance", "value": "How "}],
        [{"op": "replace", "path": "/utterance", "value": "How can "}],
        [{"op": "replace", "path": "/utterance", "value": "How can I "}],
        [{"op": "replace", "path": "/utterance", "value": "How can I help "}],
        [{"op": "replace", "path": "/utterance", "value": "How can I help you today?"}],
    ]

    # Use the jsonpatch_extractor to simulate streaming
    parser = StreamParser("utterance")
    utterance_stream = parser.json_diff_extractor(patches)

    # Collect the streamed utterance
    collected_stream = "".join([i for i in utterance_stream])

    # Assert the final streamed utterance is as expected
    assert collected_stream == "How can I help you today?"
