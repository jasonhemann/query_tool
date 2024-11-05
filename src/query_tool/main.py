# main.py

import os
import sys

import openai

# Set your OpenAI API key
openai.api_key = os.getenv("CANVAS_API_KEY")


def send_query(query, document_text):
    """Send the query and document to OpenAI API and return the response."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # or "gpt-4" if you have access
            prompt=f"Document: {document_text}\n\nQuery: {query}",
            max_tokens=200,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error communicating with OpenAI API: {e}")
        sys.exit(1)


def main():
    if not openai.api_key:
        print(
            "Error: OpenAI API key not set. Set the CANVAS_API_KEY environment variable."
        )
        sys.exit(1)

    if len(sys.argv) < 3:
        print("Usage: python query_tool/main.py '<query>' <document_path>")
        sys.exit(1)

    query = sys.argv[1]
    document_path = sys.argv[2]

    # Read the document file
    try:
        with open(document_path, "r") as file:
            document_text = file.read()
    except FileNotFoundError:
        print(f"Error: Document file '{document_path}' not found.")
        sys.exit(1)

    # Send query and document to OpenAI API
    result = send_query(query, document_text)
    print("LLM Response:", result)


if __name__ == "__main__":
    main()
