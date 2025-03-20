import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

DAILY_REQUEST_LIMIT = int(os.getenv("DAILY_REQUEST_LIMIT", "100"))

# Load API keys into a list
OPENAI_API_KEYS = os.getenv("OPENAI_API_KEYS", "")
API_KEYS_LIST = [key.strip() for key in OPENAI_API_KEYS.split(",") if key.strip()]

# Load CORS ALLOWED ORIGINS
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "")
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in CORS_ALLOWED_ORIGINS.split(",") if origin.strip()]

# Load BLOCKED USER AGENTS
BLOCKED_USER_AGENTS = os.getenv("BLOCKED_USER_AGENTS", "")
BLOCKED_USER_AGENTS = [agent.strip() for agent in BLOCKED_USER_AGENTS.split(",") if agent.strip()]

BACKEND_TYPE = os.getenv("BACKEND_TYPE", "openai")

if not API_KEYS_LIST:
    raise ValueError("No API keys provided in OPENAI_API_KEYS")

# This will be the shared rotating index (you could also make it thread-safe if needed)
CURRENT_KEY_INDEX = 0

def get_next_api_key():
    global CURRENT_KEY_INDEX
    key = API_KEYS_LIST[CURRENT_KEY_INDEX]
    CURRENT_KEY_INDEX = (CURRENT_KEY_INDEX + 1) % len(API_KEYS_LIST)
    return key
