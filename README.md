# Calculation Challenge Microservice

This service may be run in Docker Compose or in non-Docker environment.

## Run in non-Docker Environment

Install Python 3.10

Install Python dependencies:

    make venv

Run tests:

    make test

Run tests with coverage:

    make test-coverage

Run service:

    make run

## Run in Docker Compose

Install Docker Compose.

Build Docker image:

    docker compose build

Run tests:

    docker compose run --rm app pytest tests

Run service:

    docker compose up


## Service Environment Variables

`BACKEND_URL`
: Backend api url.

`LOGGING_LEVEL`
: Logging level (One of: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
Default: `DEBUG`.

`NO_DOT_ENV`
: Disable reading of `.env` file (set to any non-empty string). Recommend to
set this in production environment or when using Docker Compose.

`STREAMLIT_SERVER_ADDRESS`
: Web app streamlit server address.

`STREAMLIT_PORT`
: Web app streamlit port.

## Uvicorn Environment Variables

`UVICORN_HOST`
: Bind socket to this host. Default: `127.0.0.1`.

`UVICORN_PORT`
: Bind socket to this port. Default: `8000`.

See full list of settings: https://www.uvicorn.org/settings/

## Usage Example

Run service. Then run:

```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/calculate/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "expression": "3+4.25"
}'
```


## Pre-commit

Install pre-commit hooks:

    make pre-commit-install
