# app.py
from flask import Flask, request, jsonify
# from sklearn.ensemble import RandomForestClassifier
import pandas as pd
# import pickle
import joblib

app = Flask(__name__)

def preprocess(data):
    return pd.DataFrame.from_dict({
    'English': 12,
    'Kiswahili': 12,
    'Mathematics': 12,
    'Physics': 12,
    'Biology': 11,
    'Chemistry': 10,
    'Overall Grade': 83,
    'Cluster Points': 42.453,
    'languages' : 12,
    'science' : 12,
    'Weighted_points' : 32.75,
    'Job_satisfaction' : 4.5,
    'Interest_Laboratories' : 0,
    'Interest_Medical Research' : 0,
    'Interest_Nursing' : 0,
    'Interest_Pharmacy' : 0,
    'Interest_Public Health' : 1,
    'Interest_Surgery' : 0,
    'Interest_Therapy' : 0,
}, orient="index")

@app.route('/recommendations', methods=['POST'])
def predict():
    # Get input data from the request
    input_data = request.get_json()

    # processed_input = preprocess(input_data)
    processed_input = preprocess(input_data)
    print('Gotten data')
    # Use the model to predict and recommend courses
    # with open("model/model_v2.pkl", "rb") as f:
    #     ml_model = pickle.load(f)
    # ml_model = joblib.load('model/model_v2.pkl')
    print('Loading...')
    ml_model = joblib.load('model/best_model.pkl')
    print('Loaded')
    # ml_model = RandomForestClassifier()
    # ml_model.load('model/model_v2.pkl')

    # f = open('model/best_model.pkl', 'rb')
    # ml_model = pickle.load(f)
    print('Predicting...')  
    predictions = ml_model.predict(processed_input)
    print('Predicted')
    print(predictions)

    # Return cluster points and recommended courses
    return jsonify({'cluster_points': 'cluster_points', 'recommended_courses': 'recommended_courses'})

if __name__ == '__main__':
    app.run()
    predict()