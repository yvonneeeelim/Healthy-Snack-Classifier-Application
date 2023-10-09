# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

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
        font-size: 46px;
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
st.markdown(
    """
    <p class="subheader">Scan, Snack, Stay Healthy!</p>
    <p class="subheader">Scan your snack, uncover its nutrients, and receive instant health insights! Make mindful snacking a breeze</p>
    """,
    unsafe_allow_html=True
)

st.divider()

# Get user input for nutrients
sugar = st.number_input("Enter Sugar (g):", min_value=0, step=1)
fats = st.number_input("Enter Fats (g):", min_value=0, step=1)
sodium = st.number_input("Enter Sodium (mg):", min_value=0, step=1)

# Display the user input
st.write("### Nutrient Values:")
st.write(f"Sugar: {sugar} g")
st.write(f"Fats: {fats} g")
st.write(f"Sodium: {sodium} mg")

# Logic to recommend snacks based on user input (this is just a sample recommendation logic)
recommended_snacks = []
if sugar < 200 and fats > 10:
    recommended_snacks.append("Greek Yogurt")
if sodium < 20 and fats < 10:
    recommended_snacks.append("Almonds")
if sugar < 150:
    recommended_snacks.append("Apple")

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
    

if st.button('Snack-o-meter it!'):
    with st.spinner('Looking hard for nutrients...'):
        
        user = answer_1 + " " + answer_2
        user_series = pd.Series(user)
        user_record = vectorizer.transform(user_series)
        prediction = model.predict(user_record)
        
        partner = partner_1 + " " + partner_2
        partner_series = pd.Series(partner)
        partner_record = vectorizer.transform(partner_series)
        partner_prediction = model.predict(partner_record)
        
        
    st.success('Done!')
    
    if prediction ==1  and partner_prediction ==1 :
       st.divider() 
       st.write("You and your partner have the same attachment style which is ***Anxious***.")
       st.write("Anxious attachment styles are less likely to communicate their needs directly (i.e. make inferences from the narratives in their head rather than from reality). When a couple are both of anxious types, they should try to invite each other to communicate directly like frequently asking them what they think or feel about something.")
       st.write("View the video below to understand more.")
       st.divider()

       st.video("https://www.youtube.com/watch?v=EdpaCMW1PHw&ab_channel=HeidiPriebe", format="video/mp4", start_time=0)
       
       st.write("Below are some recommendations for you :wink:")
       col1, col2, col3 = st.columns(3, gap="medium")
       with col1:
           
           st.image("https://img1.od-cdn.com/ImageType-100/1523-1/%7BF2891E67-123A-4785-AFD2-862D4DE36200%7DImg100.jpg", width = 150, use_column_width="always")
           st.link_button("Click to read more","https://nlb.overdrive.com/media/6889424", use_container_width=True)

       with col2:
           
           st.image("https://img1.od-cdn.com/ImageType-100/1219-1/%7B502BBD28-C4A1-4C12-BEC6-CD66C797430E%7DImg100.jpg", width = 150, use_column_width="always")
           st.link_button("Click to read more","https://nlb.overdrive.com/media/5901249", use_container_width=True)

       with col3:
           
           st.image("https://img1.od-cdn.com/ImageType-100/1523-1/%7B73A45BAA-C1B6-4DE1-A907-97F1DEBCE31E%7DImg100.jpg", width = 150,use_column_width="always")
           st.link_button("Click to read more","https://nlb.overdrive.com/media/5168313", use_container_width=True)
           

       st.write(" ")
       with st.chat_message("user"):
           st.write("Hello👋 We hope that the above resources have been helpful.")
           st.write("If you need more support and would like to chat with someone:") 
           st.link_button("Click for more assistance", "https://familyassist.msf.gov.sg/content/resources/programmes/online-counselling/")
       

      
       
    elif prediction == 0 and partner_prediction == 0:
        st.divider()
        st.write("You and your partner have the same attachment style which is ***Avoidant***.")
        st.write("Avoidant attachment styles do not feel comfortable sharing their emotions openly (i.e. they prefer to keep their thoughts to themselves). When couples are both avoidant, they should commit to expressing themselves more to each other,  so that misunderstandings can be avoided.")
        st.write("View the video below to understand more.")
        st.divider()

        st.video("https://www.youtube.com/watch?v=zv7ROoYCi6s&ab_channel=HeidiPriebe", format="video/mp4", start_time=0)
        
        st.write("Below are some book recommendations for you :wink:")
        col1, col2, col3 = st.columns(3, gap="medium")
        with col1:
            
            st.image('https://img1.od-cdn.com/ImageType-100/1430-1/%7BC70BEA75-D280-43F2-AEFF-1E5EEB5CD8F6%7DImg100.jpg', width = 150, use_column_width="always")
            st.link_button("Click to read more","https://nlb.overdrive.com/media/319596", use_container_width=True)

        with col2:
            
            st.image("https://img1.od-cdn.com/ImageType-100/0044-1/%7BED3699EC-C269-4B4E-AA44-9BC0970FB606%7DImg100.jpg", width = 150, use_column_width="always")
            st.link_button("Click to read more","https://nlb.overdrive.com/media/3682131", use_container_width=True)

        with col3:
            
            st.image("https://img1.od-cdn.com/ImageType-100/1430-1/%7BEC8D5943-429E-4F9C-B446-5D6600E3AB57%7DImg100.jpg", width = 150,use_column_width="always")
            st.link_button("Click to read more","https://nlb.overdrive.com/media/322424", use_container_width=True)

        
        st.write(" ")
        with st.chat_message("user"):
            st.write("Hello👋 We hope that the above resources have been helpful.")
            st.write("If you need more support and would like to chat with someone:") 
            st.link_button("Click for more assistance", "https://familyassist.msf.gov.sg/content/resources/programmes/online-counselling/")


    elif prediction == 0 and partner_prediction == 1:
        st.divider()
        st.write("Your attachment style is ***Avoidant*** whereas your partner's attachment style is ***Anxious***.")
        st.write("Avoidant attachment styles do not feel comfortable sharing their emotions openly (i.e. keep their thoughts to themselves). Anxious attachment styles on the other hand are less likely to communicate their needs directly (i.e. make inferences from the narratives in their head rather than from reality). Opening up to your partner and reciprocating their emotions will be the key in having successful communication.")
        st.write("View the video below to understand more.")
        st.divider()

        st.video("https://www.youtube.com/watch?v=yMQ-cO-Jqmg", format="video/mp4", start_time=0)
        
        st.write("Below are some book recommendations for you :wink:")
        col1, col2, col3 = st.columns(3, gap="medium")
        with col1:
            
            st.image("https://img1.od-cdn.com/ImageType-100/12293-1/%7B054D9E58-B7ED-45E4-9C97-CCEE8BFD6433%7DIMG100.JPG", width = 150, use_column_width="always")
            st.link_button("Click to read more","https://nlb.overdrive.com/media/5054551", use_container_width=True)

        with col2:
            
            st.image("https://img1.od-cdn.com/ImageType-100/1219-1/%7B502BBD28-C4A1-4C12-BEC6-CD66C797430E%7DImg100.jpg", width = 150, use_column_width="always")
            st.link_button("Click to read more","https://nlb.overdrive.com/media/5901249", use_container_width=True)

        with col3:
            
            st.image("https://img1.od-cdn.com/ImageType-100/1523-1/%7B73A45BAA-C1B6-4DE1-A907-97F1DEBCE31E%7DImg100.jpg", width = 150,use_column_width="always")
            st.link_button("Click to read more","https://nlb.overdrive.com/media/5168313", use_container_width=True)
        
        st.write(" ")
        with st.chat_message("user"):
            st.write("Hello👋 We hope that the above resources have been helpful.")
            st.write("If you need more support and would like to chat with someone:") 
            st.link_button("Click for more assistance", "https://familyassist.msf.gov.sg/content/resources/programmes/online-counselling/")


    else: #prediction == 1 and partner_prediction == 0:
        st.divider()
        st.write("Your attachment style is ***Anxious*** whereas your partner's attachment style is ***Avoidant***.")
        st.write("Anxious attachment styles are less likely to communicate their needs directly (i.e. make inferences from the narratives in their head rather than from reality). Avoidant attachment styles on the other hand do not feel comfortable sharing their emotions openly (i.e. keep their thoughts to themselves). Trusting your partner and getting your partner to open up to you will be the key in having successful communication.")
        st.write("View the video below to understand more.")
        st.divider()

        st.video("https://www.youtube.com/watch?v=l8vcCPakbds", format="video/mp4", start_time=0)
        
        st.write("Below are some book recommendations for you :wink:")
        col1, col2, col3 = st.columns(3, gap="medium")
        with col1:
            
            st.image('https://img1.od-cdn.com/ImageType-100/1523-1/%7BD7320176-CE10-4830-9F86-2142B5F595B3%7DImg100.jpg', width = 150, use_column_width="always")
            st.link_button("Click to read more","https://nlb.overdrive.com/media/204069", use_container_width=True)

        with col2:
    
            st.image('https://img1.od-cdn.com/ImageType-100/1430-1/%7BC70BEA75-D280-43F2-AEFF-1E5EEB5CD8F6%7DImg100.jpg', width = 150, use_column_width="always")
            st.link_button("Click to read more","https://nlb.overdrive.com/media/319596", use_container_width=True)

        with col3:
    
            st.image("https://img1.od-cdn.com/ImageType-100/0044-1/%7BED3699EC-C269-4B4E-AA44-9BC0970FB606%7DImg100.jpg", width = 150, use_column_width="always")
            st.link_button("Click to read more","https://nlb.overdrive.com/media/3682131", use_container_width=True)

        st.write(" ")
        with st.chat_message("user"):
            st.write("Hello👋 We hope that the above resources have been helpful.")
            st.write("If you need more support and would like to chat with someone:") 
            st.link_button("Click for more assistance", "https://familyassist.msf.gov.sg/content/resources/programmes/online-counselling/")

