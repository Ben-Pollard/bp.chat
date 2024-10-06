# LLM Experiments

This project is designed to experiment with language models using a Streamlit app interface. It allows users to interact with a language model chain to generate responses based on input messages.

## Setup

To set up the project, ensure you have Python 3.12 installed. Use Poetry to manage dependencies.

1. Install dependencies:
   ```bash
   poetry install
   ```

2. Set your OpenAI API key as an environment variable:
   ```bash
   set OPENAI_API_KEY=your_openai_api_key
   ```

## Building and Running the Docker Image

To build the Docker image, use the following command:
```bash
docker build -t your-image-name .
```

To run the Docker container, ensuring your OpenAI API key is passed as an environment variable, use:
```bash
docker run --env OPENAI_API_KEY=$OPENAI_API_KEY -p 8501:8501 your-image-name
```

Replace `your-image-name` with the desired name for your Docker image.

To run the Streamlit app, execute the following command:
```bash
streamlit run app.py
```

This will start a local server, and you can interact with the app through your web browser.

## Testing

## Testing

To run the tests, use `pytest`:
```bash
pytest tests/
```

This will execute the test suite to ensure the chain invocation works as expected.
