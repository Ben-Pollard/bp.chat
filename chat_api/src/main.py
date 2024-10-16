import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from chat_api.src.models.message import StreamRequest
from chat_api.src.chains.chat_assistant import ChatAssistant

app = FastAPI()

chat_assistant = ChatAssistant()


@app.post("/chat")
async def chat(request: StreamRequest):
    """Respond to a message with an async streaming chat response"""
    user_input = await request.model_dump_json()  # Get user input from the request
    config = {"configurable": {"session_id": "your_session_id"}}  # Set your session ID

    async def event_stream():
        async for chunk in chat_assistant.chain.astream({"input": user_input}, config):
            yield chunk  # Stream each chunk of response

    return StreamingResponse(event_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000, app=app)
