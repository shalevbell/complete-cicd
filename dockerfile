FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY app/. .
RUN pip install --no-cache-dir -r requirements.txt && mkdir -p /app/static/history

EXPOSE 9090
ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "wsgi:weather_app"]