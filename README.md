# Feminist Quote Generator

An API built with FastAPI and GraphQL to generate feminist quotes.

## Setup/Instructions

Setup the virtual environment and install dependencies:

- `python3 --version` to ensure you have Python 3.6+ installed
- `virtualenv --version`
- `python -m venv virtualenv`
- `source virtualenv/bin/activate`
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`

Start the server for the first time: `uvicorn main:app --reload`

## Endpoints

Make POST requests to `http://localhost:8000/graphql`

Get a list of quotes:

```graphql
{
  getQuote {
    id
    quote
    author
  }
}
```

Fetch a quote by id:

```graphql
{
  getQuote(id: 2) {
    id
    quote
    author
  }
}
```
