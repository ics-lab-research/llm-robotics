import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from the .env file
load_dotenv()


genai.configure(api_key=os.environ["GEMINI_API"])

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    # "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=genai.GenerationConfig(**generation_config),
)

# chat_session = model.start_chat(history=[])
# response = chat_session.send_message("Who are you", stream=True)

# for chunk in response:
#     print(chunk.text)
#     print("_" * 80)

response = model.generate_content(["how to be get better in programming?"])
print(response.text)
