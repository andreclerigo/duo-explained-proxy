from flask import Flask, request, jsonify
from services.usage_logger_sqlite import UsageLoggerSQLite
from services.ai_backend import AIBackend
from config import DAILY_REQUEST_LIMIT, OPENAI_API_KEY
import os

app = Flask(__name__)

# Ensure the database path is set inside /app/data (shared volume)
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'usage_logs.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

usage_logger = UsageLoggerSQLite(DB_PATH)
ai_backend = AIBackend(backend_type="openai", api_key=OPENAI_API_KEY)

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

@app.route("/usage", methods=["GET"])
def get_usage():
    logs = usage_logger.get_logs()
    return jsonify({
        "total_usage_today": usage_logger.get_daily_count(),
        "recent_logs": logs
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
