FROM python:3.12-slim

WORKDIR /app

# Install sqlite-web
RUN pip install sqlite-web

# Copy start script
COPY start_sqlite_web.py .

# Expose SQLite Web UI port
EXPOSE 5002

# Run SQLite Web Admin
CMD ["python", "start_sqlite_web.py"]
