import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # Suppress TensorFlow warnings

import numpy as np
from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from PIL import Image
import gdown

print("1. Checking for model...")

# DOWNLOAD MODEL BEFORE LOADING IT
MODEL_PATH = 'pepper_disease_model.h5'
if not os.path.exists(MODEL_PATH):
    print("Downloading model from Google Drive...")
    url = 'https://drive.google.com/uc?id=1juWQmz7ln3kSPH5bJfxyk2fR1ukEtCxk'
    gdown.download(url, MODEL_PATH, quiet=False)
    print("Model downloaded successfully!")
else:
    print("Model already exists.")

print("2. Loading Keras model...")
app = Flask(__name__)

model = tf.keras.models.load_model(MODEL_PATH, compile=False)
print("3. Model loaded successfully!")

class_names = ['bacterial_spot', 'healthy']
os.makedirs('static', exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            img = Image.open(file).convert('RGB').resize((224, 224))
            img_array = np.expand_dims(np.array(img) / 255.0, axis=0).astype('float32')
            preds = model.predict(img_array, verbose=0)
            idx = np.argmax(preds[0])
            conf = float(np.max(preds[0]) * 100)
            disease = 'Bacterial Spot' if idx == 0 else 'Healthy'
            return jsonify({
                'disease': disease,
                'confidence': round(conf, 2),
                'severity': 'High' if conf > 90 else 'Medium' if conf > 75 else 'Low',
                'cause': 'Bacteria Xanthomonas campestris.' if idx == 0 else 'No disease detected.',
                'organic_cure': 'Copper-based bactericide spray.' if idx == 0 else 'No treatment needed.',
                'chemical_cure': 'Mancozeb 2g/L.' if idx == 0 else 'No treatment needed.',
                'prevention': 'Avoid overhead watering.' if idx == 0 else 'Continue monitoring.'
            })
    return render_template('index.html')

if __name__ == '__main__':
    print("4. Starting Flask server...")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)