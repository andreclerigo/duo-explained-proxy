from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from services.usage_logger_sqlite import UsageLoggerSQLite
from services.ai_backend import AIBackend
from config import DAILY_REQUEST_LIMIT, BACKEND_TYPE
import logging
import os

# Ensure the data directory exists (important for Docker volume mounting)
os.makedirs("data", exist_ok=True)

# FastAPI app instance
app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Allow all origins (unsafe, but good for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all domains (change this to specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Initialize the logger and backend
usage_logger = UsageLoggerSQLite("data/usage_logs.db")
ai_backend = AIBackend(backend_type=BACKEND_TYPE)

# Request body model (replaces Flask `request.json`)
class ProxyRequest(BaseModel):
    source: Optional[str] = "unknown_source"
    prompt: str

@app.post("/proxy")
def proxy_request(req: ProxyRequest):
    if not usage_logger.is_within_limit(DAILY_REQUEST_LIMIT):
        raise HTTPException(status_code=429, detail="Daily request limit exceeded")

    usage_logger.log_request(req.source, req.prompt)

    response_text = ai_backend.get_response(req.prompt)

    return {
        "source": req.source,
        "prompt": req.prompt,
        "response": response_text
    }

@app.get("/usage")
def get_usage():
    return {
        "total_usage_today": usage_logger.get_daily_count(),
        "recent_logs": usage_logger.get_logs()
    }
