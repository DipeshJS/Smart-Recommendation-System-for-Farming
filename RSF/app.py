from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask import render_template
import numpy as np
import pickle
import warnings
from flask_cors import CORS
# import flask-cors
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the pickled model and scaler
with open('rsf-model.pkl', 'rb') as file:
    model = pickle.load(file)
with open('label_encoder.pkl', 'rb') as file:
    scaler = pickle.load(file)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    print("in def predict")
    if request.method == 'POST':
        try:
            # data = request.json
            # print(data)
            # N = data['Nitrogen']
            # P = data['Phosporus']
            # K = data['Potassium']
            # temp = data['Temperature']
            # humidity = data['Humidity']
            # ph = data['Ph']
            # rainfall = data['Rainfall']

            data = request.json
            # Extracting data from JSON
            print(data)
            
            N = data.get('Nitrogen', 0)
            P = data.get('Phosporus', 0)
            K = data.get('Potassium', 0)
            temp = data.get('Temperature', 0)
            humidity = data.get('Humidity', 0)
            ph = data.get('Ph', 0)
            rainfall = data.get('Rainfall', 0)
            
            # Validation checks
            if not all(isinstance(val, (int, float)) and val > 0 for val in [N, P, K, temp, humidity, ph, rainfall]):
                return jsonify({'error': 'All values must be positive numbers.'}), 400
            if not (0 <= ph <= 14):
                return jsonify({'error': 'pH must be between 0 and 14.'}), 400

           
            # Prepare input data for prediction
            feature_list = [N, P, K, temp, humidity, ph, rainfall]
            single_pred = np.array(feature_list).reshape(1, -1)
            print(feature_list)
            # Make the prediction using the loaded model
            prediction = model.predict(single_pred)
            outputs = scaler.inverse_transform(prediction)
            print("output predicted")
            # outputs = prediction.tolist()
            return render_template('output_page.html', prediction= outputs[0].upper())
        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        return jsonify({'error': 'Method is Not Allowed'}), 405


if __name__ == '__main__':
    app.run(debug=True)
