
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
st.markdown('<p class="subheader">Snack & Stay Healthy! Look up your snack, uncover its nutrients, and receive instant health insights! Make mindful snacking a breeze</p>', unsafe_allow_html=True)


st.divider()

st.markdown("**Choose from below options:**")
tab1, tab2, tab3, tab4 = st.tabs(["Enter Your Nutrients", "Upload an image", "Search Keywords", "Find Healthy Snack"])
# Add a short liner above the tabs

with tab1:
   st.header("Enter Your Nutrients")
    
   # Get user input for nutrients
   sugar = float(st.number_input("Enter Sugar (g):", format="%.3f", value=1.000))
   fats = float(st.number_input("Enter Fats (g):", format="%.3f", value=1.000))
   sodium = float(st.number_input("Enter Sodium (g):", format="%.3f", value=1.000))
   serving_size = float(st.number_input("Enter Serving Size (g):", value=1.000))

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
       with st.spinner("Searching for snack details..."):
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
            with st.spinner("Searching for snack details..."):
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
    
   # Rename the product column
   product_data = product_data.rename(columns={"product": "Product"})

   # Get user input for product lookup
   query = st.text_input("Enter the name of the snack:")

   button3 = st.button('Find snacks!',key="button3")
   
   # if button is pressed
   if button3:
        st.spinner("Finding snack details...")
   
        subset_data = product_data[product_data['Product'].str.contains(query,case=False, regex=True)==True].reset_index()
        
        if len(subset_data) != 0:
   
            subset_data_X = subset_data[['total_fat_g_per_gram_of_serving','sugars_g_per_gram_of_serving','sodium_g_per_gram_of_serving']]
   
            with open("classifier.pkl", 'rb') as our_model:
                model = pickle.load(our_model)
       
            prediction_array = model.predict(subset_data_X)
   
            pred_df = pd.DataFrame(prediction_array).rename(columns = {0:"class"})

            pred_df['Recommendation'] = pred_df['class'].replace({0:"Unhealthy snack, please refrain from consuming",1:"Eat in moderation"})
            
            merged_subset = pd.merge(subset_data,pred_df,left_index = True, right_index = True)
            merged_subset_answer = merged_subset[['Product','Recommendation']].sort_values('Recommendation')
            
            merged_outcome = merged_subset_answer.reset_index().drop("index",axis=1)
            
            if st.success("Complete!"):
                st.write("Below shows the results of relevant snack that you have queried!")
            
                st.dataframe(merged_outcome) 
            
            else:
               st.write("Thank you for your patience, it appears that we do not have the relevant snack that you have queried!")
      

with tab4:
   st.header("Find Healthy Snack")
   # Load product data from CSV file
   product_data = pd.read_csv('final_data.csv')
   image_data = pd.read_csv("products-cookies-clean-images.csv")
   image_data.rename(columns= {'product':'product_url'},inplace=True)
   final = pd.merge(product_data, image_data,  how='left', left_on=['type','per_serving_g','total_fat_g','sugars_g','sodium_g','total_fat_g_per_gram_of_serving','sugars_g_per_gram_of_serving','sodium_g_per_gram_of_serving'], right_on = ['type','per_serving_g','total_fat_g','sugars_g','sodium_g','total_fat_g_per_gram_of_serving','sugars_g_per_gram_of_serving','sodium_g_per_gram_of_serving'])
   complete_data = final.drop(['Unnamed: 0'],axis=1)
   
   product_X = product_data[['total_fat_g_per_gram_of_serving','sugars_g_per_gram_of_serving','sodium_g_per_gram_of_serving']]
   
   with open("classifier.pkl", 'rb') as our_model:
       model = pickle.load(our_model)

   prediction_array = model.predict(product_X)

   pred_df = pd.DataFrame(prediction_array).rename(columns = {0:"class"})

   pred_df['outcome'] = pred_df['class'].replace({0:"Unhealthy snack, please refrain from consuming",1:"Eat in moderation"})


   merged_subset = pd.merge(complete_data,pred_df,left_index = True, right_index = True)
   merged_subset = merged_subset.dropna()
   merged_subset_answer = merged_subset[['type','product','imageLink','outcome','per_serving_g','total_fat_g','sugars_g','sodium_g','total_fat_g_per_gram_of_serving','sugars_g_per_gram_of_serving','sodium_g_per_gram_of_serving']].sort_values('outcome')

   good_cookie_data = merged_subset_answer[(merged_subset_answer['type']=="cookie") & (merged_subset_answer['outcome'] =="Eat in moderation")]
   good_cream_data = merged_subset_answer[(merged_subset_answer['type']=="cream") & (merged_subset_answer['outcome'] =="Eat in moderation")]
   good_wafer_data = merged_subset_answer[(merged_subset_answer['type']=="wafer") & (merged_subset_answer['outcome'] =="Eat in moderation")]
   good_cracker_data = merged_subset_answer[(merged_subset_answer['type']=="cracker") & (merged_subset_answer['outcome'] =="Eat in moderation")]
   
   category2 =  st.radio("Choose your category of snack:", ['cookie','cracker','cream','wafer'])
   
   nutri_option2 = st.radio("Choose the nutrient that you wish to reduce",['fat content','sugar content','sodium content'])
   
   if category2 == 'cookie' and nutri_option2 == 'fat content':
       answer = good_cookie_data.sort_values('total_fat_g_per_gram_of_serving').head(3).reset_index().drop(['index'],axis=1)
   elif category2 == 'cookie' and nutri_option2 == 'sugar content':
       answer = good_cookie_data.sort_values('sugars_g_per_gram_of_serving').head(3).reset_index().drop(['index'],axis=1)
   elif category2 == 'cookie' and nutri_option2 == 'sodium content':
       answer = good_cookie_data.sort_values('sodium_g_per_gram_of_serving').head(3).reset_index().drop(['index'],axis=1) 
       
   elif category2 == 'cream' and nutri_option2 == 'fat content':
       answer = good_cream_data.sort_values('total_fat_g_per_gram_of_serving').head(3).reset_index().drop(['index'],axis=1)
   elif category2 == 'cream' and nutri_option2 == 'sugar content':
       answer = good_cracker_data.sort_values('sugars_g_per_gram_of_serving').head(3).reset_index().drop(['index'],axis=1)
   elif category2 == 'cream' and nutri_option2 == 'sodium content':
       answer = good_cracker_data.sort_values('sodium_g_per_gram_of_serving').head(3).reset_index().drop(['index'],axis=1) 
       
   elif category2 == 'cracker' and nutri_option2 == 'fat content':
       answer = good_cracker_data.sort_values('total_fat_g_per_gram_of_serving').head(3).reset_index().drop(['index'],axis=1)
   elif category2 == 'cracker' and nutri_option2 == 'sugar content':
       answer = good_cracker_data.sort_values('sugars_g_per_gram_of_serving').head(3).reset_index().drop(['index'],axis=1)
   elif category2 == 'cracker' and nutri_option2 == 'sodium content':
       answer = good_cracker_data.sort_values('sodium_g_per_gram_of_serving').head(3).reset_index().drop(['index'],axis=1) 
   
   elif category2 == 'wafer' and nutri_option2 == 'fat content':
       answer = good_wafer_data.sort_values('total_fat_g_per_gram_of_serving').head(3).reset_index().drop(['index'],axis=1)
   elif category2 == 'wafer' and nutri_option2 == 'sugar content':
       answer = good_wafer_data.sort_values('sugars_g_per_gram_of_serving').head(3).reset_index().drop(['index'],axis=1)
   else:
       answer = good_wafer_data.sort_values('sodium_g_per_gram_of_serving').head(3).reset_index().drop(['index'],axis=1) 
       

   button4 = st.button('Find the healthiest snack!',key="button4")
   
   if button4:
       
       image_list = []
       product_list = []
       fat_list = []
       sugar_list = []
       sodium_list = []
       serving_list = []
       
       for i in range(len(answer)):
           image_link = answer['imageLink'].iloc[i]
           product_name = answer['product'].iloc[i]
           fat_content = answer['total_fat_g'].iloc[i]
           sugar_content = answer['sugars_g'].iloc[i]
           sodium_content = answer['sodium_g'].iloc[i]
           serving_content = answer['per_serving_g'].iloc[i]
           
           image_list.append(image_link)
           product_list.append(product_name)
           sugar_list.append(sugar_content)
           sodium_list.append(sodium_content)
           fat_list.append(fat_content)
           serving_list.append(serving_content)
           
       #image_link = answer['imageLink'].iloc[0]
       #product_name = answer['product'].iloc[0]
       #fat_content = answer['total_fat_g'].iloc[0]
       #sugar_content = answer['sugars_g'].iloc[0]
       #sodium_content = answer['sodium_g'].iloc[0]
       #serving_content = answer['per_serving_g'].iloc[0]
       
       
       st.write("Here's our recommendation! :blush:")
       st.write("")
       
       
       col1, col2, col3 = st.columns(3, gap="medium")
       with col1:
            st.image(image_list[0], caption=product_list[0],width = 150, use_column_width="always")
            st.write("For serving size of ", serving_list[0], " g:")
            st.write("The fat content is ", fat_list[0], " g")
            st.write("The sugar content is ",sugar_list[0]," g")
            st.write("The sodium content is ", sodium_list[0], " g")
           

       with col2:
            st.image(image_list[1], caption=product_list[1],width = 150, use_column_width="always")
            st.write("For serving size of ", serving_list[1], " g:")
            st.write("The fat content is ", fat_list[1], " g")
            st.write("The sugar content is ",sugar_list[1]," g")
            st.write("The sodium content is ", sodium_list[1], " g")

       with col3:
            st.image(image_list[2], caption=product_list[2],width = 150, use_column_width="always")
            st.write("For serving size of ", serving_list[2], " g:")
            st.write("The fat content is ", fat_list[2], " g")
            st.write("The sugar content is ",sugar_list[2]," g")
            st.write("The sodium content is ", sodium_list[2], " g")
