
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

tab1, tab2, tab3 = st.tabs(["Enter Your Nutrients", "Upload an image", "Search Keywords"])

with tab1:
   st.header("Enter Your Nutrients")
    
   # Get user input for nutrients
   sugar = float(st.number_input("Enter Sugar (g):", value=1))
   fats = float(st.number_input("Enter Fats (g):", value=1))
   sodium = float(st.number_input("Enter Sodium (g):", value=1))
   serving_size = float(st.number_input("Enter Serving Size (g):", value=1))

   # calculate the nutrition value for prediction
   fats_per_gram = fats/serving_size
   sugars_per_gram = sugar/serving_size
   sodium_per_gram = sodium/serving_size

   with open("classifier.pkl", 'rb') as our_model:
        model = pickle.load(our_model)

   data = {'total_fat_g_per_gram_of_serving': [fats_per_gram],
            'sugars_g_per_gram_of_serving': [sugars_per_gram],
            'sodium_g_per_gram_of_serving': [sodium_per_gram]}
   test = pd.DataFrame(data)

   button = st.button("Get my snack details!", key="button")  
   # if button is pressed
   if button:
       with st.spinner("Wait for it..."):
            ans=model.predict(test)
    
            if ans==0:
                st.write("Your snack is unfortunately unhealthy. Try to pick another snack unless you're too stressed and in need of this snack as comfort food!")
            else:
                st.write("Good Job! Your snack is healthy! Keep snacking.")
    
       st.success("Done!")


st.divider()

with tab2:
   st.header("Upload an image")

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

        # save the values into its respective dataframes
        sodium = df.iloc[df.loc[(df['Text'] == 'Sodium')].index+1,1:2]
        fats = df.iloc[df.loc[(df['Text'] == 'Total Fat')].index+1,1:2]
        sugar = df.iloc[df.loc[(df['Text'] == 'Total Sugar')].index+1,1:2]
        serving = df.iloc[df.loc[(df['Text'] == "Servings Size")].index+1,1:2]

        # storing the values of the extracted text
        sodium_value = sodium['Text'].iloc[0]
        fats_value = fats['Text'].iloc[0]
        sugars_value = sugar['Text'].iloc[0]
        serving_value = serving['Text'].iloc[0]

        # extract out the serving size in grams
        serving_size = float(serving_value[:2])

        fats_actual_value = float(fats_value[:-1])

        sugars_actual_value = float(sugars_value[:-1])

        sodium_actual_value = float(sodium_value[:-2])/1000

        # calculate the nutrition value for prediction
        fats_per_gram = fats_actual_value/serving_size
        sugars_per_gram = sugars_actual_value/serving_size
        sodium_per_gram = sodium_actual_value/serving_size


        with open("classifier.pkl", 'rb') as our_model:
            model = pickle.load(our_model)

        data = {'total_fat_g_per_gram_of_serving': [fats_per_gram],
                'sugars_g_per_gram_of_serving': [sugars_per_gram],
                'sodium_g_per_gram_of_serving': [sodium_per_gram]}
        test = pd.DataFrame(data)

        button2 = st.button("Get my snack details!", key="button2")
        # if button is pressed
        if button2:
            with st.spinner("Wait for it..."):
                ans=model.predict(test)
    
                if ans==0:
                    st.write("Your snack is unfortunately unhealthy. Try to pick another snack unless you're too stressed and in need of this snack as comfort food!")
                else:
                    st.write("Good Job! Your snack is healthy! Keep snacking.")
    
        st.success("Done!")

with tab3:
   st.header("Search Keywords")
   # Load product data from CSV file
   product_data = pd.read_csv('final_data.csv')

   # Get user input for product lookup
   query = st.text_input("Enter the name of the snack")
   
   button3 = st.button('Find snacks!',key="button3")
   
   # if button is pressed
   if button3:
        st.spinner("Finding snack...")
   
        subset_data = product_data[product_data['product'].str.contains(query,case=False, regex=True)==True].reset_index()
        
        if len(subset_data) != 0:
   
            subset_data_X = subset_data[['total_fat_g_per_gram_of_serving','sugars_g_per_gram_of_serving','sodium_g_per_gram_of_serving']]
   
            with open("classifier.pkl", 'rb') as our_model:
                model = pickle.load(our_model)
       
            prediction_array = model.predict(subset_data_X)
   
            pred_df = pd.DataFrame(prediction_array).rename(columns = {0:"class"})

            pred_df['outcome'] = pred_df['class'].replace({0:"Not healthy, refrain from consuming",1:"Eat in moderation"})
            
            merged_subset = pd.merge(subset_data,pred_df,left_index = True, right_index = True)
            merged_subset_answer = merged_subset[['product','outcome']].sort_values('outcome')
            
            merged_outcome = merged_subset_answer.reset_index().drop("index",axis=1)
            
            st.success("Complete!")
            
            st.write("Below is the result of relevant snacks that you have queried! :blush:")
            
            st.dataframe(merged_outcome) 
            
   else:
            st.write("Thank you for your patience, it appears that we do not have the relevant snacks that you have queried!")
      
