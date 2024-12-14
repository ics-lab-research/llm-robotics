import os
from dotenv import load_dotenv
from literalai import LiteralClient

load_dotenv()

literalai_client = LiteralClient(api_key=os.getenv("LITERAL_API_KEY"))


def main():
    thread_id = None  # Optional: Provide a thread_id to continue an existing thread
    with literalai_client.thread(name="Thread Example", thread_id=thread_id) as thread:
        user_query = "Hello World"
        literalai_client.message(content=user_query, type="user_message", name="User")

        # Add more steps here


main()

# Wait for all steps to be sent. This is NOT needed in production code.
literalai_client.flush_and_stop()
