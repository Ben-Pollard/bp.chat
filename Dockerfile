# Use the official Python image as a parent image
FROM python:3.12-slim

# Set environment variables
ENV POETRY_VERSION=1.5.1
ENV PIPX_HOME=/root/.local
ENV PATH="$PIPX_HOME/bin:$PATH"

# Install pipx and use it to install Poetry
RUN pip install --no-cache pipx && \
    pipx install poetry==$POETRY_VERSION

# Set the working directory
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock /app/

# Install the dependencies
RUN poetry install --no-root

# Copy the rest of the application code
COPY . /app

# Expose the port the app runs on
EXPOSE 8501

# Run the application
CMD ["poetry", "run", "streamlit", "run", "app.py"]
