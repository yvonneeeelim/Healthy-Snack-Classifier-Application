
import streamlit as st
import numpy as np
import time
from PIL import Image
import pickle
import pandas as pd
import easyocr

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

data = {'total_fat_g_per_gram_of_serving': [fats],
        'sugars_g_per_gram_of_serving': [sugar],
        'sodium_g_per_gram_of_serving': [sodium]}
test = pd.DataFrame(data)

button = st.button('Get my snack details!')
# if button is pressed
if button:
    ans=model.predict(test)
    
    if ans==0:
        st.write("Your snack is unfortunately unhealthy. Try to pick another snack unless you're too stressed and in need of this snack as comfort food!")
    else:
        st.write("Good Job! Your snack is healthy! Keep snacking.")
    
    st.success("Done!")


st.divider()

# Get user input for image upload
uploaded_file = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])

# Process the uploaded image if it exists
if uploaded_file is not None:
    # Open and display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    reader = easyocr.Reader(['en'])
    result = reader.readtext(np.array(image))
    
    df = pd.DataFrame(result)
    df.columns = ['1', 'Text', '2']

    # Extract Total Fat value
    total_fat_row = df.loc[df['Text'] == 'Total Fat']
    if not total_fat_row.empty:
        total_fat_index = total_fat_row.index[0]
        total_fat_value = df.iloc[total_fat_index + 1, 1]  # Extracting the value after 'Total Fat'
        print('Total Fat: ' + total_fat_value)
    else:
        print('Total Fat information not found in the image.')


    with open("classifier.pkl", 'rb') as our_model:
    model = pickle.load(our_model)

    data = {'total_fat_g_per_gram_of_serving': [fats],
            'sugars_g_per_gram_of_serving': [sugar],
            'sodium_g_per_gram_of_serving': [sodium]}
    test = pd.DataFrame(data)

    button = st.button('Get my snack details!')
    # if button is pressed
    if button:
        ans=model.predict(test)
    
        if ans==0:
            st.write("Your snack is unfortunately unhealthy. Try to pick another snack unless you're too stressed and in need of this snack as comfort food!")
        else:
            st.write("Good Job! Your snack is healthy! Keep snacking.")
    
        st.success("Done!")
