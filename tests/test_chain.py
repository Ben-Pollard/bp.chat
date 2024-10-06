"""Tests for the outer chat chain"""

from unittest.mock import patch
from chain_setup import StreamParser, chain


def test_json_patch_streaming():
    """Unittest for streaming json parser"""

    fake_json_patches = [
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

def test_chain_call_with_mocked_response():
    """Test to mock the chain call and receive fake patches"""

    fake_patches = [
        [{"op": "add", "path": "/utterance", "value": ""}],
        [{"op": "replace", "path": "/utterance", "value": "Hello "}],
        [{"op": "replace", "path": "/utterance", "value": "Hello, how "}],
        [{"op": "replace", "path": "/utterance", "value": "Hello, how are "}],
        [{"op": "replace", "path": "/utterance", "value": "Hello, how are you?"}],
    ]

    with patch.object(chain, 'invoke', return_value=fake_patches) as mock_invoke:
        response = list(chain.invoke({"input": "Hi"}))
        mock_invoke.assert_called_once_with({"input": "Hi"})
        assert response == fake_patches

    parser = StreamParser("utterance")
    utterance_stream = parser.json_diff_extractor(patches)

    # Collect the streamed utterance
    collected_stream = "".join([i for i in utterance_stream])

    # Assert the final streamed utterance is as expected
    assert collected_stream == "How can I help you today?"
