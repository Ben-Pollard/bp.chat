import unittest
from chain_setup import chain

class TestChainInvocation(unittest.TestCase):
    def test_chain_invocation(self):
        # Example input
        user_input = "Hello, how are you?"

        # Invoke the chain
        result = chain.invoke({"input": user_input}, {"configurable": {"session_id": "unused"}})

        # Check if the result is a non-empty string
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

if __name__ == "__main__":
    unittest.main()
