import json
import os
from typing import Dict, Iterable

import requests
from dotenv import load_dotenv

load_dotenv()


class ApiClient:

    hostname = os.getenv("CHAT_API_HOSTNAME")
    port = os.getenv("CHAT_API_PORT")

    def __init__(self):
        pass

    @property
    def base_url(self):
        return f"http://{self.hostname}:{self.port}"

    def get_chat_response(self, user_input: str, session_id: int):
        return self.get_response("chat", user_input, session_id)

    def get_test_response(self):
        return self.get_response("test", "test", -1)

    def get_response(
        self, endpoint, user_input: str, session_id: int
    ) -> Iterable[Dict]:
        """Get the response stream from the chat API."""
        url = f"{self.base_url}/{endpoint}"
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
