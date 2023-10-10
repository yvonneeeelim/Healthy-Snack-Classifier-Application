
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

# Logic to recommend snacks based on user input (this is just a sample recommendation logic)
recommended_snacks = []
if sugar < 200 and fats > 10:
    recommended_snacks.append("Greek Yogurt", "https://www.fairprice.com.sg/product/farmers-union-greek-style-yoghurt-natural-1kg-155863")
if sodium < 20 and fats < 10:
    recommended_snacks.append("Almond Nuts", "https://www.fairprice.com.sg/product/natures-wonders-baked-almond-nuts-70g-11720126")
if sugar < 150:
    recommended_snacks.append("Granola", "https://www.fairprice.com.sg/product/sweet-home-farm-granola-blueberry-with-flax-454g-13217933")

# Display recommended snacks
st.write("### Recommended Snacks:")
if recommended_snacks:
    for snack in recommended_snacks:
        st.write(f"- {snack}")
else:
    st.write("Uh-oh, no recommended snacks. Let us stock up first!")

with open("our_model.pkl", 'rb') as our_model:
    model = pickle.load(our_model)

with open('our_vectorizer.pkl', 'rb') as vect:
    vectorizer = pickle.load(vect)
    
   
st.write(" ")
with st.chat_message("user"):
    st.write("Hello👋 We hope that the above resources have been helpful.")
    st.write("If you need more support and would like to chat with someone:") 
    st.link_button("Click for more assistance", "https://familyassist.msf.gov.sg/content/resources/programmes/online-counselling/")

