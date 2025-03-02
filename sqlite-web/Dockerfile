FROM python:3.12-slim

WORKDIR /app

RUN pip install sqlite-web

CMD ["sqlite_web", "data/usage_logs.db", "--host", "0.0.0.0", "--port", "5002"]
