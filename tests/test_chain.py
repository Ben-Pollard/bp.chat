"""Tests for the outer chat chain"""
import unittest
from chain_setup import chain

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

if __name__ == "__main__":
    unittest.main()
