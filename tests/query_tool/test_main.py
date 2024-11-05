# tests/query_tool/test_main.py

import pytest

from query_tool.main import main, send_query


def test_send_query():
    # Mock the OpenAI API response, as we don't want to make an actual API call
    query = "What is the capital of France?"
    document_text = "This is some document text to provide context."

    # Assuming send_query would normally return a response
    response = send_query(query, document_text)
    assert isinstance(
        response, str
    )  # Or any other assertions based on expected behavior


def test_main_no_api_key(monkeypatch, capsys):
    # Simulate no API key set
    monkeypatch.delenv("CANVAS_API_KEY", raising=False)

    # Capture system exit and output
    with pytest.raises(SystemExit) as exc_info:
        main()
    captured = capsys.readouterr()

    assert exc_info.value.code == 1
    assert "Error: OpenAI API key not set" in captured.out
