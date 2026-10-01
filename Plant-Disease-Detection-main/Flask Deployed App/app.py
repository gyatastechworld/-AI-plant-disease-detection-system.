import os
from pathlib import Path
from flask import Flask, jsonify, redirect, render_template, request
from werkzeug.utils import secure_filename
from PIL import Image
import CNN
import numpy as np
import torch
import pandas as pd


APP_DIR = Path(__file__).resolve().parent
MODEL_PATH = Path(os.getenv('MODEL_PATH', APP_DIR / 'plant_disease_model_1_latest.pt'))
UPLOAD_DIR = APP_DIR / 'static' / 'uploads'

disease_info = pd.read_csv(APP_DIR / 'disease_info.csv', encoding='cp1252')
supplement_info = pd.read_csv(APP_DIR / 'supplement_info.csv', encoding='cp1252')

model = CNN.CNN(39)    
if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f'Model checkpoint not found: {MODEL_PATH}. '
        'Download plant_disease_model_1_latest.pt or set MODEL_PATH.'
    )
model.load_state_dict(torch.load(MODEL_PATH, map_location='cpu'))
model.eval()

def prediction(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))
    input_data = torch.from_numpy(np.asarray(image.convert('RGB'), dtype=np.float32) / 255.0)
    input_data = input_data.permute(2, 0, 1)
    input_data = input_data.view((-1, 3, 224, 224))
    with torch.no_grad():
        output = model(input_data)
    probabilities = torch.softmax(output, dim=1)[0]
    index = int(torch.argmax(probabilities).item())
    confidence = float(probabilities[index].item())
    return index, confidence


def prediction_details(file_path):
    pred, confidence = prediction(file_path)
    healthy_indexes = {3, 5, 7, 11, 15, 18, 20, 23, 24, 25, 28, 38}
    return {
        'disease': str(disease_info['disease_name'][pred]),
        'description': str(disease_info['description'][pred]),
        'recommendation': str(disease_info['Possible Steps'][pred]),
        'image_url': str(disease_info['image_url'][pred]),
        'supplement_name': str(supplement_info['supplement name'][pred]),
        'supplement_image': str(supplement_info['supplement image'][pred]),
        'buy_link': str(supplement_info['buy link'][pred]),
        'confidence': round(confidence * 100, 1),
        'healthy': pred in healthy_indexes,
    }


app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact-us.html')

@app.route('/index')
def ai_engine_page():
    return render_template('index.html')


@app.route('/api/predict', methods=['POST'])
def api_predict():
    image = request.files.get('image')
    filename = secure_filename(image.filename) if image else ''
    if not filename:
        return jsonify({'error': 'Please choose a plant image first.'}), 400
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_path = UPLOAD_DIR / filename
    image.save(file_path)
    return jsonify(prediction_details(file_path))

@app.route('/mobile-device')
def mobile_device_detected_page():
    return render_template('mobile-device.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        image = request.files['image']
        filename = secure_filename(image.filename)
        if not filename:
            return 'Please select an image.', 400
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        file_path = UPLOAD_DIR / filename
        image.save(file_path)
        print(file_path)
        details = prediction_details(file_path)
        return render_template('submit.html', title=details['disease'], desc=details['description'],
                       prevent=details['recommendation'], image_url=details['image_url'],
                       pred=details['disease'], sname=details['supplement_name'],
                       simage=details['supplement_image'], buy_link=details['buy_link'],
                       confidence=details['confidence'], healthy=details['healthy'],
                       disease=details['disease'])

@app.route('/market', methods=['GET', 'POST'])
def market():
    return render_template('market.html', supplement_image = list(supplement_info['supplement image']),
                           supplement_name = list(supplement_info['supplement name']), disease = list(disease_info['disease_name']), buy = list(supplement_info['buy link']))

if __name__ == '__main__':
    app.run(debug=True)
