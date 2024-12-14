import os
from dotenv import load_dotenv

load_dotenv()

url = str(os.environ.get("NGROK_URL")) + "/generate"
print(url)
