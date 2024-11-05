Here’s a sample `README.md` for your project. This README includes an overview of the project’s purpose, setup instructions, usage, and testing guidelines.

```markdown
# Query Tool

A Python-based query tool for interacting with the OpenAI API. This tool allows users to send custom queries to the API, along with document text, to receive AI-generated responses. 

## Project Structure

The project is organized as follows:
- `query_tool/`: The main package directory containing the following files:
  - `main.py`: Contains the primary functionality and can be run directly to send queries.
  - `__main__.py`: Enables the package to be executed with `python -m query_tool`.
- `tests/`: Directory for unit tests, which cover the main functionality.

## Setup and Installation

This project uses [PDM](https://pdm.fming.dev/) for dependency management and virtual environment handling. Follow these steps to set up the project:

1. **Install PDM** (if you haven’t already):
   ```bash
   pip install pdm
   ```

2. **Install Project Dependencies**:
   Navigate to the project root directory and install dependencies:
   ```bash
   pdm install
   ```

## Environment Variables

To use this tool, you’ll need to set an environment variable for your OpenAI API key.

1. **Set the OpenAI API Key**:
   ```bash
   export CANVAS_API_KEY="your_openai_api_key"
   ```

Alternatively, you can create a `.env` file with the following line and use a package like `python-dotenv` to load it automatically:
   ```dotenv
   CANVAS_API_KEY=your_openai_api_key
   ```

## Usage

To send a query using the tool, provide a query string and a path to the document text file. The tool will send the query and the document to OpenAI and print the AI’s response.

### Running as a Package

Run the tool as a package:
```bash
python -m query_tool "<query>" <document_path>
```

### Running `main.py` Directly

Alternatively, you can run `main.py` directly if needed:
```bash
python query_tool/main.py "<query>" <document_path>
```

## Testing

The project uses `pytest` for testing, along with `coverage` for test coverage reporting.

### Running Tests

To run tests, use the following command:
```bash
pdm run pytest
```

### Checking Coverage

To measure test coverage for the project, use:
```bash
pdm run pytest --cov=query_tool --cov-report=term-missing
```

To enforce a minimum coverage threshold (e.g., 100%), run:
```bash
pdm run pytest --cov=query_tool --cov-fail-under=100
```

### Pre-Commit Hooks (Optional)

If you have set up `pre-commit` hooks, they will automatically run `black`, `isort`, `flake8`, and `mypy` on staged files to enforce code quality before each commit.

To manually run the pre-commit hooks, use:
```bash
pdm run pre-commit run --all-files
```

If you need to bypass these hooks during a commit, add the `--no-verify` flag:
```bash
git commit --no-verify
```

## License

This project is licensed under the MIT License.
```

This `README.md` provides a concise overview, setup instructions, usage examples, and testing guidelines tailored to your PDM-based setup.
