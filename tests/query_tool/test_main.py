# tests/query_tool/test_main.py

import pytest

from query_tool.main import (
    check_api_key,
    check_file_exists,
    create_client,
    send_query,
    validate_args,
)


def test_validate_args_usage_info(capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["query_tool/main.py"])  # No arguments
    with pytest.raises(SystemExit) as exc_info:
        validate_args()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Usage: python query_tool/main.py '<query>' <document_path>" in captured.out


def test_create_client_with_key(monkeypatch):
    # Set the environment variable for the API key and create a client
    monkeypatch.setenv("OPENAI_API_KEY", "test_key")
    client = create_client()

    # Confirm that the client is configured with the correct API key
    assert client is not None, "Expected a valid client instance"
    assert client.api_key == "test_key", "Expected the API key to be set correctly"


def test_check_api_key_no_key(monkeypatch, capsys):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(SystemExit) as exc_info:
        check_api_key()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error: OpenAI API key not set" in captured.out


def test_check_file_exists_missing_file(capsys):
    with pytest.raises(SystemExit) as exc_info:
        check_file_exists("non_existent_file.txt")
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error: Document file 'non_existent_file.txt' not found." in captured.out


def test_check_file_exists(monkeypatch, tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Sample text")
    try:
        check_file_exists(str(test_file))  # Should not raise SystemExit
    except SystemExit:
        pytest.fail("SystemExit raised unexpectedly!")


def test_send_query_response_handling(mocker):
    # Create a mock response directly with the necessary nested structure
    mock_response = mocker.Mock(
        choices=[mocker.Mock(message=mocker.Mock(content="Paris"))]
    )

    # Mock OpenAI client's `chat.completions.create` method to return `mock_response`
    mock_client = mocker.Mock()
    mock_client.chat.completions.create.return_value = mock_response

    # Define inputs
    query = "What is the capital of France?"
    document_text = "Some document content here."

    # Call `send_query` with the mock client and check the returned value
    response = send_query(mock_client, query, document_text)
    assert response == "Paris", "Expected response to be 'Paris'"
