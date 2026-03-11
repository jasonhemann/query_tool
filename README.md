# Query Tool

This tool sends a query plus local document context to the OpenAI API and prints the response.

## Prerequisites

- Python 3.13+
- OpenAI API key in `OPENAI_API_KEY`

## Setup

```bash
make sync
source .venv/bin/activate
```

## Usage

```bash
uv run python -m query_tool "<your_query>" <path_to_document>
```

Example:

```bash
uv run python -m query_tool "Write a summary" /path/to/document.txt
```

## Quality checks

```bash
make check
```

Individual commands:

```bash
make format
make lint
make lint-fix
make typecheck
make test
make coverage
```

## Build standalone binary

```bash
make build
```

## Project files

- `src/query_tool/main.py`: core runtime and API call path.
- `src/query_tool/__main__.py`: module entrypoint.
- `tests/query_tool/test_main.py`: unit tests.
- `pyproject.toml`: dependency and tooling configuration.
