FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY app/requirements.txt ./

# Install dependencies and curl for container health check
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/static/history

COPY app/. .

EXPOSE 9090
ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "wsgi:weather_app"]
