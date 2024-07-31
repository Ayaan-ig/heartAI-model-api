from flask import Flask,request,jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import pickle
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()




with open('pipe.pkl','rb') as model_file:
    pipe = pickle.load(model_file)


app = Flask(__name__)

mongo_uri = os.getenv('MONGO_URI')
if not mongo_uri:
    raise ValueError("MONGO_URI environment variable not set")

client = MongoClient(mongo_uri,server_api=ServerApi('1'))
db = client.get_database()  # Use default database
collection = db['people-data']


CORS(app)

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
    print(data)

    #converting data to pd dataFrame

    try:
        new_data = pd.DataFrame([data],columns=columns)
        print(new_data['Chest Pain Type'])
        print(new_data)
    except Exception as e:  
        return jsonify({'error' : str(e)}), 400

    # making prediction

    try: 
        prediction = pipe.predict(new_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    print(f'heres the prediction {prediction}') 
    prediction_result = prediction[0].item() if hasattr(prediction[0], 'item') else prediction[0]

    
    return jsonify({'result' : prediction_result,'object':data})


@app.route('/add', methods = ['POST'])
def addData():
    print('coming to data adding route', flush=True)
    data = request.json
    collection.insert_one(data)
    return jsonify(message = 'data added'), 201

 
if __name__ == '__main__':
    app.run(debug=True)