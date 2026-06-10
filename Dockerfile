# Root Dockerfile: builds the Python app only to avoid platform auto-detection running `npm ci`
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# install system deps required by some Python packages
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy app sources
COPY . /app/

EXPOSE 8000

# Use the ASGI adapter that mounts the Flask app and exposes /metrics
CMD ["uvicorn", "app_asgi:app", "--host", "0.0.0.0", "--port", "8000"]
