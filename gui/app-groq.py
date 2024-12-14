import os
import chainlit as cl
from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv()

client = AsyncGroq(
    api_key=os.environ.get("GROQ_API"),
)


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
        [
            {
                "role": "system",
                "content": "You are an advanced virtual assistant specializing in URScript programming and Universal Robots operations. Your expertise spans robot programming, debugging, and optimization within industrial automation. Your mission is to provide precise, actionable, and context-aware solutions.",
            }
        ],
    )


@cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")

    stream = await client.chat.completions.create(
        messages=message_history,
        stream=True,
        model="llama3-8b-8192",
    )

    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)

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
