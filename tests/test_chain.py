"""Tests for the outer chat chain"""
import unittest
from chain_setup import chain, jsonpatch_extractor

class TestChainInvocation(unittest.TestCase):
    """Unit test for chain invocation."""
    def test_chain_invocation(self):
        """Test if the chain returns a non-empty string for a given input."""
        # Example input to test the chain
        user_input = "Hello, how are you?"

        # Invoke the chain and check the result
        result = chain.invoke({"input": user_input}, {"configurable": {"session_id": "unused"}})

        # Assert that the result is a non-empty string
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_json_patch_streaming(self):
        """Unittest for streaming json parser"""

        patches = [
            {"op": "add", "path": "/reasoning", "value": ""}, 
            {"op": "replace", "path": "/reasoning", "value": "The "},
            {"op": "replace", "path": "/reasoning", "value": "The chatbot "},
            {"op": "replace", "path": "/reasoning", "value": "The chatbot evaluates "},
            {"op": "replace", "path": "/reasoning", "value": "The chatbot evaluates user inputs."},
            {"op": "add", "path": "/utterance", "value": ""},
            {"op": "replace", "path": "/utterance", "value": "How "},
            {"op": "replace", "path": "/utterance", "value": "How can "},
            {"op": "replace", "path": "/utterance", "value": "How can I "},
            {"op": "replace", "path": "/utterance", "value": "How can I help "},
            {"op": "replace", "path": "/utterance", "value": "How can I help you today?"}
        ]

        # Use the jsonpatch_extractor to simulate streaming
        utterance_stream = jsonpatch_extractor(patches, "utterance")

        # Collect the streamed utterance
        streamed_utterance = ""
        for part in utterance_stream:
            streamed_utterance = part

        # Assert the final streamed utterance is as expected
        self.assertEqual(streamed_utterance, "How can I help you today?")

if __name__ == "__main__":
    unittest.main()
