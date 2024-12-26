from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Access environment variables
database_url = os.getenv("DATABASE_URL")
secret_key = os.getenv("SECRET_KEY")
debug = os.getenv("DEBUG")

print(f"Database URL: {database_url}")
print(f"Secret Key: {secret_key}")
print(f"Debug Mode: {debug}")
