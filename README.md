# Query Tool

This tool allows you to interact with the OpenAI API to send queries based on the contents of a document and receive responses. The program reads a local document, combines it with a user-defined query, and sends it to the OpenAI API to generate a response.

## Prerequisites

- **Python 3.13** or higher
- **OpenAI API key**

## Installation

1. **Install Dependencies**

   Since dependencies are defined in [`pyproject.toml`](./pyproject.toml), you can use any compatible tool for installation.

2. **API Key Setup**

   Ensure you have your OpenAI API key stored as an environment variable:

   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   ```

## Usage

Run the program by specifying the query and the path to the document:

```bash
python -m query_tool "<your_query>" <path_to_document>
```

For example:

```bash
python -m query_tool "Write a summary" /path/to/document.txt
```

## Project Files

- [`src/query_tool/main.py`](./src/query_tool/main.py): Core program logic for sending queries to the OpenAI API.
- [`tests/query_tool/test_main.py`](./tests/query_tool/test_main.py): Test cases for `main.py`.
- [`pyproject.toml`](./pyproject.toml): Project configurations for dependencies, linting, formatting, and testing.
- [`README.md`](./README.md): This file, providing usage instructions.

## Running Tests

This project includes a suite of tests to verify functionality. You can run the tests using any test runner compatible with `pytest`. The commands below assume a typical environment configuration:

1. **Run All Tests**:

   ```bash
   pytest
   ```

2. **Run All Tests with Coverage**:

   ```bash
   pytest --cov=src
   ```

These commands will run the tests and report coverage based on the configurations specified in `pyproject.toml`. 

For full linting, formatting, and type-checking, refer to the `pre-commit` configuration in the development section below.

## Development

The following commands are optional and primarily for development convenience.

### Environment Configuration

If you’re using `pdm`, you can activate your environment with:

```bash
eval $(pdm venv activate in-project)
```
and deactivate with

```bash
deactivate
```

### Building 

To build this project as a single stand-alone onefile executable python script, use

```bash
pyinstaller --onefile --name query_tool src/query_tool/__main__.py 
```

and the executable will be built in `dist`. 


### Running Tests and Checks with Pre-Commit

To run tests, linting, and other checks in a single command (recommended for development), you can use the `pre-commit` setup specified in `pyproject.toml`:

```bash
pdm run pre-commit run --all-files
```

This command will:
- Run `pytest` for testing.
- Enforce code formatting with `black` and `isort`.
- Perform linting with `flake8` and type checking with `mypy`.

> **Note**: If you’re not using `pdm`, consult `pyproject.toml` and `pre-commit` for dependency and configuration details.

## Notes

- **API Key**: The program checks for the `OPENAI_API_KEY` environment variable. If it’s not set, the program will exit with an error.

