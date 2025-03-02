import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

DAILY_REQUEST_LIMIT = int(os.getenv("DAILY_REQUEST_LIMIT", "100"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BACKEND_TYPE = os.getenv("BACKEND_TYPE", "openai")
