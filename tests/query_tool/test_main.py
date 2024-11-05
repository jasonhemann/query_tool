# tests/query_tool/test_main.py

import pytest

from query_tool.main import (
    check_api_key,
    check_file_exists,
    create_client,
    main,
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
    # Create a mock for the message content
    mock_message = mocker.Mock()
    mock_message.content = "Paris"  # Setting the content attribute directly

    # Create a mock for the choice that includes the message
    mock_choice = mocker.Mock()
    mock_choice.message = mock_message  # Assign mock_message to the message attribute

    # Create the mock response to have a list of choices
    mock_response = mocker.Mock()
    mock_response.choices = [mock_choice]  # Assign mock_choice to choices list

    # Mock the OpenAI client's `chat.completions.create` method
    mock_client = mocker.Mock()
    mock_client.chat.completions.create.return_value = mock_response

    # Define inputs
    query = "What is the capital of France?"
    document_text = "Some document content here."

    # Call `send_query` with the mock client and check the returned value
    response = send_query(mock_client, query, document_text)
    assert response == "Paris", "Expected response to be 'Paris'"


# def test_send_query(mocker):
#     # Define the expected response structure from OpenAI
#     expected_response = {"choices": [{"message": {"content": "Paris"}}]}

#     # Patch the `create` method on the client's `chat.completions`
#     mock_create = mocker.patch(
#         "query_tool.main.client.chat.completions.create", return_value=expected_response
#     )

#     # Run `send_query` with the patched client
#     client = create_client()
#     query = "What is the capital of France?"
#     document_text = "This is some document text to provide context."

#     # Execute `send_query` and capture the response
#     response = send_query(client, query, document_text)
#     assert response == "Paris"

#     # Verify `create` was called with the correct parameters
#     mock_create.assert_called_once_with(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "Use the provided document for context."},
#             {"role": "user", "content": f"Document: {document_text}"},
#             {"role": "user", "content": f"Query: {query}"},
#         ],
#         max_tokens=200,
#     )
