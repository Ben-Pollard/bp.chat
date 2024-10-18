"""LLM Chat Server"""

import json

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from chat_api.src.chains.chat_assistant import ChatAssistant
from chat_api.src.models.message import StreamRequest

app = FastAPI()

chat_assistant = ChatAssistant()


@app.post("/chat")
async def chat(request: StreamRequest):
    """Respond to a message with an async streaming chat response"""
    user_input = request.model_dump_json()  # Get user input from the request
    config = {"configurable": {"session_id": "your_session_id"}}  # Set your session ID

    def event_stream():
        for chunk in chat_assistant.chain.stream({"input": user_input}, config):
            yield json.dumps(chunk)  # Stream each chunk of response

    return StreamingResponse(event_stream(), media_type="application/json")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(host="0.0.0.0", port=8000, app=app)
