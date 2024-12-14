import requests
import json
import sys


def fetch_llm():
    # Define the URL of the Flask application
    url = "http://localhost:5000/generate"

    # Define the payload
    payload = {
        "messages": [
            {
                "role": "user",
                "content": "Continue the Fibonacci sequence! Your input is 1, 1, 2, 3, 5, 8,",
            }
        ],
        "max_new_tokens": 10,
    }

    # Define the headers
    headers = {"Content-Type": "application/json"}

    try:
        # Send the POST request
        response = requests.post(
            url, headers=headers, data=json.dumps(payload), stream=True
        )

        # NOTE: streaming word by word
        for chunk in response.iter_content(decode_unicode=True):
            # buffer += chunk
            sys.stdout.write(chunk)
            sys.stdout.flush()

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
