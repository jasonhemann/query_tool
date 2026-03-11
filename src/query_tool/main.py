"""Query tool runtime and CLI wiring."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

from openai import OpenAI


@dataclass(frozen=True)
class CliArgs:
    """CLI arguments for query execution."""

    query: str
    document_path: Path


def check_api_key() -> str:
    """Return OPENAI_API_KEY or exit with an error."""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key

    print("Error: OpenAI API key not set. Set OPENAI_API_KEY.")
    raise SystemExit(1)


def create_client() -> OpenAI:
    """Create an OpenAI API client using the configured key."""
    return OpenAI(api_key=check_api_key())


def validate_args(argv: list[str] | None = None) -> CliArgs:
    """Validate CLI args and return typed values."""
    args = list(argv) if argv is not None else list(sys.argv[1:])
    if len(args) < 2:
        print("Usage: python -m query_tool '<query>' <document_path>")
        raise SystemExit(1)

    return CliArgs(query=args[0], document_path=Path(args[1]))


def check_file_exists(filepath: Path) -> None:
    """Exit if the input document is missing."""
    if not filepath.is_file():
        print(f"Error: Document file '{filepath}' not found.")
        raise SystemExit(1)


def send_query(client: OpenAI, query: str, document_text: str) -> str:
    """Send a query and document text to the OpenAI API."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Use the provided document for context."},
                {"role": "user", "content": f"Document: {document_text}"},
                {"role": "user", "content": f"Query: {query}"},
            ],
            max_tokens=200,
        )
    except Exception as exc:
        print(f"Error communicating with OpenAI API: {exc}")
        raise SystemExit(1) from exc

    if not response.choices:
        print("Error: OpenAI API returned no choices.")
        raise SystemExit(1)

    return (response.choices[0].message.content or "").strip()


def main(argv: list[str] | None = None) -> int:
    """Run CLI and return process exit code."""
    args = validate_args(argv)
    check_file_exists(args.document_path)

    document_text = args.document_path.read_text(encoding="utf-8")
    result = send_query(create_client(), args.query, document_text)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
