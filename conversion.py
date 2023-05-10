
# def convert_json_to_csv(api_url, csv_filename):
#     # Make request to API endpoint
#     response = requests.get(api_url)
#     data = response.json()
    
#     # Convert JSON data to pandas DataFrame
#     df = pd.json_normalize(data)
    
#     # Save DataFrame to CSV file
#     df.to_csv(csv_filename, index=False)

import pandas as pd
import json
import math
from category_encoders import OrdinalEncoder
from flask import Flask, request, jsonify
from surprise import dump
from surprise import Reader, Dataset
import os

# Load 
def json_to_df(json_data):
    # load JSON data
    data = json.loads(json.dumps(json_data))
    # data['user_id'] = 'user_120'

    # convert to DataFrame
    # Define the rating scale for the data
    # reader = Reader(rating_scale=(4.0, 5.0))
    df = pd.json_normalize(data)
    # data  = Dataset.load_from_df(df[['user_id','Interest', 'Job_satisfaction']], reader)
    return df

def load_model(model_filename):
    file_name = os.path.expanduser(model_filename)
    loaded_model = dump.load(file_name)

    return loaded_model

def lang(df):
  if df['English'] >= df['Kiswahili']:
    return df['English']
  else:
    return df['Kiswahili']
    

def science(df):
  if df['Mathematics'] >= df['Physics']:
    return df['Mathematics']
  else:
    return df['Physics']
  
def cluster_points(df):
  mult = (df['points']/48)*(df['Overall_Grade']/84)
  cluster = 48 * math.sqrt(mult)
  return cluster

def generate_user_id(df):
    num_users = len(df) + 1
    return f'user_{num_users}'

def get_course_recommendations(user_id, df):
    KNNBaseline_pickle_model = load_model('model/KNNBaseline_pickled_model')

    # get the inner user id
    inner_user_id = df.to_inner_uid(user_id)

    # get the courses the user has already rated
    rated_courses = set([r[0] for r in df.ur[inner_user_id]])

    # get all courses
    course_ids = [iid for iid in df.all_items()]

    # Get the list of courses the user is interested in
    user_interests = df.loc[df['ID'] == user_id, 'Interest'].unique()
    print(f'User Interest: {user_interests} ')

    # # Create a list of tuples of (course, predicted rating) for each course
    course_ratings = []
    for course in df.loc[df['Interest'].isin(user_interests), 'Course'].unique():
      if course not in rated_courses:
        predicted_rating = KNNBaseline_pickle_model.predict(uid=user_id, iid=course).est
        course_ratings.append((course, predicted_rating))

    # Sort the list of course ratings by predicted rating
    course_ratings_sorted = sorted(course_ratings, key=lambda x: x[1], reverse=True)
    # Create a list of the top three recommended courses that match the user's interests
    recommended_courses = []
    for course_rating in course_ratings_sorted:
      if course_rating[0] not in user_interests:
        recommended_courses.append(course_rating[0])
        if len(recommended_courses) == 3:
            break
    return recommended_courses

app = Flask(__name__)

@app.route('/recommendations', methods=['POST'])
def predict():
    input_data = request.get_json()
    # input_data = {
    #    'English' : 12,
    #    'Kiswahili' : 12,
    #    'English' : 12,
    #    'English' : 12,
    #    'English' : 12,
    # }
    input_data['user_id'] = 'user_120'
    df = json_to_df(input_data)
    df['Interest'].unique()

    mapping = [{'col': 'Interest', 'mapping': {'Public Health': 1,  'Laboratories': 2,
                                            'Nursing': 3, 'Medical Research': 4,
                                            'Therapy': 5, 'Pharmacy': 5, 'Surgery': 6}}]
    # Create an OrdinalEncoder object and fit it to the DataFrame
    encoder = OrdinalEncoder(cols=['Interest'], mapping=mapping)
    encoder.fit(df)

    
    predictions = get_course_recommendations('user_120', df)

    print(predictions)

if __name__ == "__main__":
    app.run()