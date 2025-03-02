from flask import Flask, request, jsonify
from services.usage_logger_sqlite import UsageLoggerSQLite
from services.ai_backend import AIBackend
from config import DAILY_REQUEST_LIMIT, OPENAI_API_KEY, BACKEND_TYPE

app = Flask(__name__)

usage_logger = UsageLoggerSQLite("data/usage_logs.db")

# Initialize modular backend
ai_backend = AIBackend(backend_type=BACKEND_TYPE, api_key=OPENAI_API_KEY)

@app.route("/proxy", methods=["POST"])
def proxy_request():
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    source = data.get("source", "unknown_source")
    prompt = data.get("prompt", "")

    if not usage_logger.is_within_limit(DAILY_REQUEST_LIMIT):
        return jsonify({"error": "Daily request limit exceeded"}), 429

    usage_logger.log_request(source, prompt)

    response_text = ai_backend.get_response(prompt)

    return jsonify({
        "source": source,
        "prompt": prompt,
        "response": response_text
    }), 200
