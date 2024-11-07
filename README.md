# LLM Experiments

This project is designed to experiment with language models using a Streamlit app interface. It allows users to interact with a language model chain to generate responses based on input messages.

## Setup

To set up the project, ensure you have Python 3.12 installed. Use Poetry to manage dependencies.

1. Install dependencies:
   ```powershell
   poetry install --all-extras
   ```

2. Set OPENAI_API_KEY as an environment variable:

## Running
To run the chat server:
```powershell
uvicorn --app-dir=chat_api src.main:app --reload --env-file .env
```

To run the Streamlit app, execute the following command:
```powershell
cd web/src
streamlit run app.py
```

This will start a local server, and you can interact with the app through your web browser.

## Testing

To run the tests, use `pytest`:
```powershell
pytest tests/
```

This will execute the test suite to ensure the chain invocation works as expected.

## Building and Running the Docker Image

To build and run the Docker images, use the following commands:
```powershell
docker build --target builder-base -f Dockerfile.base .
docker-compose up --build
```

Or to run the unit tests in the container, use:
```powershell
docker run chat-dev pytest /app/tests/unit
```

