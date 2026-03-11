from pathlib import Path

import pytest

from query_tool.main import (
    check_api_key,
    check_file_exists,
    create_client,
    send_query,
    validate_args,
)


def test_validate_args_usage_info(capsys):
    with pytest.raises(SystemExit) as exc_info:
        validate_args([])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Usage: python -m query_tool '<query>' <document_path>" in captured.out


def test_create_client_with_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test_key")
    client = create_client()
    assert client is not None
    assert client.api_key == "test_key"


def test_check_api_key_no_key(monkeypatch, capsys):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(SystemExit) as exc_info:
        check_api_key()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error: OpenAI API key not set" in captured.out


def test_check_file_exists_missing_file(capsys):
    with pytest.raises(SystemExit) as exc_info:
        check_file_exists(Path("non_existent_file.txt"))
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error: Document file 'non_existent_file.txt' not found." in captured.out


def test_check_file_exists(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Sample text")
    check_file_exists(test_file)


def test_send_query_response_handling(mocker):
    mock_response = mocker.Mock(
        choices=[mocker.Mock(message=mocker.Mock(content="Paris"))]
    )
    mock_client = mocker.Mock()
    mock_client.chat.completions.create.return_value = mock_response

    response = send_query(mock_client, "What is the capital of France?", "Some text")
    assert response == "Paris"
