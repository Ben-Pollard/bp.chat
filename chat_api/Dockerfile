################################
# BUILDER
# Used to build deps for this service
################################
FROM builder-base AS builder-web
RUN --mount=type=cache,target=/root/.cache \
    poetry install --extras "chat_api"

################################
# DEVELOPMENT
# Image used during development / testing
################################
FROM python-base AS web-development
ENV FASTAPI_ENV=development
WORKDIR $PYSETUP_PATH

# copy in our built poetry + venv
COPY --from=builder-web $POETRY_HOME $POETRY_HOME
COPY --from=builder-web $PYSETUP_PATH $PYSETUP_PATH

# quicker install as runtime deps are already installed
RUN --mount=type=cache,target=/root/.cache \
    poetry install --with=dev --extras "chat_api"

# copy tests
COPY ./src /app
COPY ./tests /app/tests

# ensure tests can find application code
ENV PYTHONPATH="/app"


# will become mountpoint of our code
WORKDIR /app
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]


################################
# PRODUCTION
# Final image used for runtime
################################
FROM python-base AS production
ENV FASTAPI_ENV=production
COPY --from=builder-web $PYSETUP_PATH $PYSETUP_PATH
COPY ./src /app
WORKDIR /app
CMD ["streamlit", "run", "app.py"]