#!/bin/sh
set -eu

MODEL_DIR="${MODEL_DIR:-/app/models}"
MODEL_PATH="${MODEL_PATH:-$MODEL_DIR/plant_disease_model_1_latest.pt}"
MODEL_URL="${MODEL_URL:-https://drive.google.com/drive/folders/1ewJWAiduGuld_9oGSrTuLumg9y62qS6A?usp=share_link}"

mkdir -p "$MODEL_DIR"
if [ ! -f "$MODEL_PATH" ]; then
    echo "Model checkpoint is missing; downloading it to $MODEL_DIR ..."
    gdown --folder "$MODEL_URL" --output "$MODEL_DIR"
    downloaded_model="$(find "$MODEL_DIR" -type f \( -name '*.pt' -o -name '*.pth' \) | head -n 1)"
    if [ -z "$downloaded_model" ]; then
        echo "No .pt or .pth checkpoint was found after the download." >&2
        exit 1
    fi
    if [ "$downloaded_model" != "$MODEL_PATH" ]; then
        cp "$downloaded_model" "$MODEL_PATH"
    fi
fi

cd /app/Flask-Deployed-App
exec gunicorn --bind 0.0.0.0:7860 --workers 1 --timeout 120 app:app