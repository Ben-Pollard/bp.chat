"""LLM Chat Server"""

import json

from fastapi import FastAPI
from sse_starlette.sse import ServerSentEvent, EventSourceResponse

from src.chains.chat_assistant import ChatAssistant
from src.models.message import StreamRequest

app = FastAPI()

chat_assistant = ChatAssistant()


@app.post("/test")
async def test(request: StreamRequest):
    """Streams a canned response"""
    request.model_dump_json()  # Get user input from the request

    async def event_stream():
        for chunk in iter([{"utterance": "hello "}, {"utterance": "there"}]):
            yield ServerSentEvent(json.dumps(chunk))  # Stream each chunk of response
        yield ServerSentEvent("[DONE]")

    return EventSourceResponse(event_stream(), media_type="text/event-stream")


@app.post("/chat")
async def chat(request: StreamRequest):
    """Respond to a message with an async streaming chat response"""
    user_input = request.model_dump_json()  # Get user input from the request
    config = {"configurable": {"session_id": "your_session_id"}}  # Set your session ID

    async def event_stream():
        for chunk in chat_assistant.chain.stream({"input": user_input}, config):
            yield ServerSentEvent(json.dumps(chunk))  # Stream each chunk of response
        yield ServerSentEvent("[DONE]")

    return EventSourceResponse(event_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(host="0.0.0.0", port=8000, app=app)
