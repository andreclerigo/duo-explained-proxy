import os
from dotenv import load_dotenv

# Load .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Read environment variables
DAILY_REQUEST_LIMIT = int(os.getenv("DAILY_REQUEST_LIMIT", 100))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-fallback-api-key")
