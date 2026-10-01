FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    MODEL_DIR=/app/models \
    MODEL_PATH=/app/models/plant_disease_model_1_latest.pt

WORKDIR /app

COPY requirements-docker.txt ./
RUN pip install --upgrade pip && pip install -r requirements-docker.txt && pip install gdown==5.2.0

COPY ["Flask Deployed App", "./Flask-Deployed-App"]
COPY docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh && mkdir -p /app/models

EXPOSE 7860
ENTRYPOINT ["/app/docker-entrypoint.sh"]