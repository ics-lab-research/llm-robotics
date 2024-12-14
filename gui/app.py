import requests
import chainlit as cl
import json
import os
from dotenv import load_dotenv

# load from .env file
load_dotenv()


# template for getting start with llm
# NOTE: use `prompt professor ` to improve from instruct prompt
@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="How to control UR robot?",
            message="Explain the different methods for controlling a Universal Robots (UR) robotic arm. Include an overview of the UR teach pendant, URScript programming, and integration with external systems (e.g., ROS or PLCs). Provide examples where applicable and highlight key advantages of each method.",
        ),
        cl.Starter(
            label="Create an URscript example",
            message="Create an example of an URScript program that moves a robotic arm to pick up an object from a designated location and place it at a specified drop-off point. Include comments explaining each step in the code and ensure it demonstrates basic URScript functions such as defining positions, setting waypoints, and executing movements.",
        ),
        cl.Starter(
            label="What is movej() in URscript?",
            message="Explain the function movej() in URScript. Describe its purpose, syntax, and typical use cases in programming robotic movements. Provide an example code snippet with comments demonstrating how movej() is used to move a robotic arm to a specific position.",
        ),
        cl.Starter(
            label="How to deploy URscript?",
            message="Explain the process of deploying a URScript program to a Universal Robots robotic arm. Include the steps for transferring the script, methods of execution (e.g., through the teach pendant or remote interface), and troubleshooting common issues. Highlight any tools or software required during the deployment.",
            # icon="/public/write.svg",
        ),
    ]


@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [],
        # NOTE: role system note supported yet
        # [
        #     {
        #         "role": "system",
        #         "content": "You are an advanced virtual assistant specializing in URScript programming and Universal Robots operations. Your expertise spans robot programming, debugging, and optimization within industrial automation. Your mission is to provide precise, actionable, and context-aware solutions.",
        #     }
        # ],
    )


@cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")

    ###########################################################
    # Define the URL of the Flask application
    ngrok_url = os.environ.get("NGROK_URL")
    url = f"{ngrok_url}/generate" if ngrok_url else "http://localhost:5000/generate"

    # Define the payload
    payload = {
        "messages": message_history,
        "max_new_tokens": 10,
    }

    # Define the headers
    headers = {"Content-Type": "application/json"}

    try:
        print(payload)

        # Send the POST request
        response = requests.post(
            url, headers=headers, data=json.dumps(payload), stream=True
        )

        # NOTE: streaming word by word
        for chunk in response.iter_content(decode_unicode=True):
            # buffer += chunk
            # sys.stdout.write(chunk)
            # sys.stdout.flush()
            await msg.stream_token(chunk)

    except requests.RequestException as e:
        print(f"An error occurred: {e}")

    ###########################################################

    # async for part in stream:
    #     if token := part.choices[0].delta.content or "":
    #         await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()


# Authentication
@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None
