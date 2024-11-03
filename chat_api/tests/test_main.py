import json
from unittest.mock import patch

from fastapi.testclient import TestClient

from chat_api.src.main import app

# client = TestClient(app)


def test_chat_endpoint(client: TestClient, mock_chain_stream):

    # with patch(
    #     "chat_api.src.chains.chat_assistant.RunnableWithMessageHistory.stream",
    #     return_value=iter(mock_chain_stream),
    # ):

    request_data = {"message": "Hi!"}

    with client.stream("POST", "/chat", json=request_data) as response:

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

        streamed_responses = []
        for chunk in response.iter_text():
            if chunk:
                streamed_responses.extend(parse_sse(chunk))

        # Validate the streamed responses
        assert len(streamed_responses) == len(mock_chain_stream)
        for i, chunk in enumerate(streamed_responses):
            assert chunk == mock_chain_stream[i]


def parse_sse(response_text):
    events = []
    for event_text in response_text.strip().split("\r\n\r\n"):
        if event_text.startswith("data:"):
            json_data = event_text.split("data: ", 1)[1]
            if not json_data == "[DONE]":
                events.append(json.loads(json_data))
    return events
