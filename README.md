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

## Running the Streamlit App

To run the Streamlit app, execute the following command:
```bash
streamlit run app.py
```

This will start a local server, and you can interact with the app through your web browser.

## Testing

To run the tests, use:
```bash
python -m unittest tests/test_chain.py
```

This will execute the test suite to ensure the chain invocation works as expected.
