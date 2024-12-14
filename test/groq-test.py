import os
import asyncio
from dotenv import load_dotenv
from groq import AsyncGroq

# Load environment variables from the .env file
load_dotenv()

client = AsyncGroq(
    api_key=os.environ.get("GROQ_API"),
)


async def main() -> None:
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "who are you?",
            }
        ],
        model="llama3-8b-8192",
    )
    print(chat_completion.choices[0].message.content)


asyncio.run(main())
