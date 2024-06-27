from flask import Flask,request,jsonify
import pandas as pd
import numpy as np
import pickle



with open('pipe.pkl','rb') as model_file:
    pipe = pickle.load(model_file)


app = Flask(__name__)

columns = ['Age', 'Gender', 'Cholesterol', 'Blood Pressure', 'Heart Rate', 'Smoking', 'Alcohol Intake',
           'Exercise Hours', 'Family History', 'Diabetes', 'Obesity', 'Stress Level',
           'Blood Sugar', 'Exercise Induced Angina', 'Chest Pain Type']
@app.route('/')
def start():
    return "welcome to heartAI api"


@app.route('/predict', methods=['POST'])
def predict():
    print('coming to route')
    data = request.json

    #converting data to pd dataFrame

    try:
        new_data = pd.DataFrame([data],columns=columns)
    except Exception as e:  
        return jsonify({'error' : str(e)}), 400

    # making prediction

    try: 
        prediction = pipe.predict(new_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    print(f'heres the prediction {prediction}')
    prediction_result = prediction[0].item() if hasattr(prediction[0], 'item') else prediction[0]

    
    return jsonify({'result' : prediction_result})
