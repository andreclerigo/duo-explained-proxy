# duo-explained-proxy

## Project Overview

This project implements a **modular AI Proxy Server** that acts as an intermediary between end-users and backend AI models (like OpenAI's ChatGPT).

The primary goal is to allow users to send requests to this proxy server without needing their own API key for the AI provider, centralizing API management and usage tracking.

This project was created to provide users of the [Duo Explained](https://github.com/digas99/duo-explained) app with a way to interact with AI models without needing to manage their own API keys.

The server logs requests, tracks usage, and enforces a **daily request limit** to control how many queries the proxy can handle per day. Once the limit is reached, the proxy responds with a `429 Too Many Requests` error. The usage data is stored in a **SQLite database**, and a simple **SQLite Admin Web Interface** (using `sqlite-web`) is used to inspect the logs visually.

---

## Project Objectives

- Centralize AI API calls, so end users do not need API keys.
- Log all requests with timestamps and sources for auditing and monitoring.
- Enforce daily rate limits to manage costs and control abuse.
- Support modular backends (easily swap GPT, custom LLMs, or other services).
- Provide a web-based interface to browse logs for quick inspection.

---

## Setup Instructions

### Step 1: Environment Variables

Create a file called `.env` inside the `proxy` folder. This file defines the proxy behavior, including the daily request limit and the AI provider’s API key.

Example `.env` file:

```
DAILY_REQUEST_LIMIT=daily-request-limit-here
OPENAI_API_KEY=your-openai-api-key-here
BACKEND_TYPE=openai or custom
```

---

### Step 2: Build and Start the Project (Docker Compose)

Once the `.env` file is ready, launch the system with:

```bash
docker compose up --build
```

This will:

- Start the proxy server (on port 5001).
- Start the SQLite web interface (on port 5002) to view the logs.
- Bind-mount the `data/usage_logs.db` so logs persist across restarts.

---

## Proxy API Documentation

### Base URL

```
http://localhost:5001
```

### Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/proxy` | Forward request to AI backend |
| GET | `/usage` | Show today’s usage and recent logs |

---

### Example `/proxy` Request


```json
{
    "source": "test_user",
    "prompt": "What is the capital of France?"
}
```

Sample response:

```json
{
    "source": "test_user",
    "prompt": "What is the capital of France?",
    "response": "The capital of France is Paris."
}
```

---

### Example `/usage` Response

```json
{
    "total_usage_today": 5,
    "recent_logs": [
        {
            "timestamp": "2025-03-02 10:00:00",
            "source": "test_user",
            "prompt": "What is the capital of France?"
        }
    ]
}
```

---

### Step 3: Testing the Proxy Server

Once the system is running, you can test your proxy directly.

- Open the FastAPI documentation at:
    ```
    http://localhost:5001/docs
    ```
- Or send a direct request using `curl`:
    ```bash
    curl -X POST http://localhost:5001/proxy \
        -H "Content-Type: application/json" \
        -d '{"source":"test_user","prompt":"What is the capital of Germany?"}'
    ```

---

### Step 4: Viewing Usage Logs (SQLite Admin)

To inspect usage logs directly via a web UI, visit:

```
http://localhost:5002
```

This exposes the `usage_logs.db` database in a simple web interface.

---

## Troubleshooting

### Proxy server not reachable?

- Check if another service is already using port `5001`.
- Verify that the `.env` file exists inside the `proxy` folder.
- Check the container logs:
    ```bash
    docker compose logs proxy_server
    ```

---

## License

Duo Explained Proxy is licensed under the [MIT License](LICENSE).

---
