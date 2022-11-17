#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import boto3
import yaml
from Interface import Interface
import streamlit as st
st.set_page_config(layout="wide")

st.title("Last Exercise Activity System")

s3_client = boto3.client('s3')
s3 = boto3.resource('s3', aws_access_key_id = st.secrets['aws_access_key_id'], aws_secret_access_key = st.secrets['aws_secret_access_key'])

@st.experimental_singleton
def load_data():
    print('Object Initialised')
    content_object = s3.Object('forgefait', 'new_data.json')
    file_content = content_object.get()['Body'].read().decode('utf-8')
    print('File Read')

    data = yaml.safe_load(file_content)
    print('File Converted to JSON')
    return data

data = load_data()

name_fields_array = []
date_fields_array = []

for idx, elem in enumerate(data):
    name_fields_array.append(elem['name'])

# st.title("Last Users Activity System")
user_name = st.selectbox('Enter the ID you want to check Last Activity for?',name_fields_array,key="user_name")

curr_elem_idx = 0
flag = False
for idx, elem in enumerate(data):
    if elem['name'] == user_name:
        curr_elem_idx = idx
        flag = True

date_fields_array = list(data[curr_elem_idx]['exercises'].keys())
exercise_date = st.selectbox('Enter the Last Activity Date?',date_fields_array,key="date")

last_exercise_activity = []
for act_elem in data[curr_elem_idx]['exercises']:
    if act_elem == exercise_date:
        for exercise_elem in data[curr_elem_idx]['exercises'][act_elem]:
            last_exercise_activity.append(exercise_elem)

exercise_list = [elem['exerciseName'] for elem in last_exercise_activity]
exercise_name = st.selectbox('Enter the Last Activity Exercise Name?',exercise_list,key="exer_name")

curr_exercise_idx = 0
for idx, act_elem in enumerate(last_exercise_activity):
    if act_elem['exerciseName'] == exercise_name:
        curr_exercise_idx = idx


# In[54]:


exercise = last_exercise_activity[curr_exercise_idx]


# In[ ]:


if flag == True:
    st.header("Exercise Details")
    exercise_name = exercise['exerciseName']
    date = exercise['id']
    dailypower = int(exercise['dailyPower'])
    x = exercise['workoutData']
    workoutData = list(map(int, x))
    peakforce = int(exercise['peakForce'])
    bps = int(exercise['bestPowerSet'])
    # Exercise Details
    st.subheader("Exercise Info")
    st.write("Client's Name: " + str(user_name))
    st.write("Exercise Name: " + str(exercise_name))
    st.write("Date: " + str(date))
    st.subheader("Exercise Plot")
    chart_data = pd.DataFrame(
    np.array(workoutData),
    columns=['workout'])
    st.line_chart(chart_data)
    st.subheader("Exercise Scores")
    st.write("Daily Power: " + str(dailypower))
    st.write("Peak Force: " + str(peakforce))
    st.write("Best Power Set: " + str(bps))
    
    h_params = {'user_id': 'Test', 
     'desc': 'Test', 'bwt': 65, 
     'gender': "men's", 'exercise_mode': 'Equipped Powerlifting', 
     'rep_id': 'chest-01', 
     'signal': workoutData, 
     'global_score': 40, 'l0': 0, 'l1': 1, 'l2': 2, 'l3': 3, 
     'discount': 0.1, 
     'peaks': {'sz': 12, 'max_win': 100}, 
     'sudden_release': {'max_to_fall_ratio': 0.4, 'fall_time': 4}, 
     'mode': {'sz': 12}, 
     'jitter': {'window_size': 4, 'delta': 2, 't0': 2, 'x_dist_rel': 0.2}, 
     'smooth_blips': {'sm': 2}, 'print': 0, 'plot': 0, "log_dir":r"C:\Users\Lenovo\OneDrive\Documents\Forge\User Metric Integration\MVP_cordova_ios_android-feedback_integration\Scores/"}
    # h_params
    Interface(h_params,workoutData)


