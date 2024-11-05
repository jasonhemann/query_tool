import os
import sys

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def send_query(query, document_text):
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


def main():
    if not client.api_key:  # Change this line to use 'client'
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
