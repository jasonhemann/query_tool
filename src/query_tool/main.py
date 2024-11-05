import os
import sys

import openai


def create_client():
    check_api_key()
    api_key = os.getenv("OPENAI_API_KEY")
    return openai.OpenAI(api_key=api_key)


def send_query(client, query, document_text):
    """Send the query and document to OpenAI API and return the response."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "Use the provided document for context."},
                {"role": "user", "content": f"Document: {document_text}"},
                {"role": "user", "content": f"Query: {query}"},
            ],
            max_tokens=200,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error communicating with OpenAI API: {e}")
        sys.exit(1)


def check_api_key():
    if not os.getenv("OPENAI_API_KEY"):
        print(
            "Error: OpenAI API key not set. Set the OPENAI_API_KEY environment variable."
        )
        sys.exit(1)


def validate_args():
    if len(sys.argv) < 3:
        print("Usage: python query_tool/main.py '<query>' <document_path>")
        sys.exit(1)


def check_file_exists(filepath):
    if not os.path.isfile(filepath):
        print(f"Error: Document file '{filepath}' not found.")
        sys.exit(1)


def main():
    validate_args()
    client = create_client()

    query = sys.argv[1]
    document_path = sys.argv[2]

    check_file_exists(document_path)

    with open(document_path, "r") as file:
        document_text = file.read()

    # Send query and document to OpenAI API
    result = send_query(client, query, document_text)
    print("LLM Response:", result)


if __name__ == "__main__":
    main()
