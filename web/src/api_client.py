import requests
from typing import Dict, Iterable
import json


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_response(self, user_input: str, session_id: int) -> Iterable[Dict]:
        """Get the response stream from the chat API."""
        url = f"{self.base_url}/test"
        # payload = {"input": user_input, "session_id": session_id}
        payload = {"message": user_input}

        try:
            response = requests.post(url, json=payload, stream=True)
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    data = line.decode("utf-8").replace("data: ", "")
                    if data == "[DONE]":
                        break
                    else:
                        yield json.loads(data)
        except requests.RequestException as e:
            raise RuntimeError(f"Error in API request: {e}")
