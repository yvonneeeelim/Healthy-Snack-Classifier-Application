
import streamlit as st
import numpy as np
import time
from PIL import Image
import pickle
import pandas as pd

import streamlit as st

#opening the image
image = Image.open('snacks.jpg')

#displaying the image on streamlit app
st.image(image, use_column_width=True)


# Custom CSS to style the title and subheader
st.markdown(
    """
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 10px;
    }
    .subheader {
        font-size: 18px;
        font-style: italic;
        color: #777;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and subheader with custom styles
st.markdown('<p class="title">Snack-O-Meter</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Scan, Snack, Stay Healthy! Scan your snack, uncover its nutrients, and receive instant health insights! Make mindful snacking a breeze</p>', unsafe_allow_html=True)


st.divider()

# Get user input for nutrients
sugar = st.number_input("Enter Sugar (g):", min_value=0, step=1)
fats = st.number_input("Enter Fats (g):", min_value=0, step=1)
sodium = st.number_input("Enter Sodium (mg):", min_value=0, step=1)

with open("classifier.pkl", 'rb') as our_model:
    model = pickle.load(our_model)

if st.button('Get my snack deets!'):
    with st.spinner('Searching for your snacks details...'):
        
        sugars_g_per_gram_of_serving = sugar
        total_fat_g_per_gram_of_serving = fats
        sodium_mg_per_gram_of_serving = sodium
        user_series = pd.Series(user)
        prediction = model.predict(user_record)
        
    st.success('Done!')
