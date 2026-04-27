import os
import numpy as np
from flask import Flask, render_template, request, jsonify
import keras
from PIL import Image

print("1. Loading Keras 3.14 model...")
app = Flask(__name__)

model = keras.models.load_model('pepper_disease_model.h5', compile=False)
print("2. Model loaded successfully!")

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
    print("3. Starting Flask server...")
    app.run(debug=True)