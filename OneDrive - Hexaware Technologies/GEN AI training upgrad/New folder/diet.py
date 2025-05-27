import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import openai
import pandas as pd
 
from openai import AzureOpenAI

AZURE_ENDPOINT = "https://hexavarsity-secureapi.azurewebsites.net/api/azureai"

API_KEY = "80597e18d74f981e"

API_VERSION = "2024-02-15-preview"

MODEL = "gpt-4o-mini"

# Initialize OpenAI client

openai = AzureOpenAI(

    azure_endpoint=AZURE_ENDPOINT,

    api_key=API_KEY,

    api_version=API_VERSION

)

# Chat-based assistance function
def generate_nutrition_plan(user_info):
    """Query Azure OpenAI for chat-based learning assistance."""
    messages = [
        {"role": "system", "content": "You are a helpful assistant that generates personalized nutrition plans."},
        {"role": "user", "content": f"Create a personalized nutrition plan for the following individual:\n\n{user_info}\n\nThe plan should include breakfast, lunch, dinner, and snacks, with specific food items and portion sizes."}
    ]
    
    try:
        
        # Generate the response using the chat-completions endpoint
        response = openai.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",   
        max_tokens=500,
        temperature=0.7
    ) 
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error: {e}"   
    
    
# Streamlit app
st.title("Personalized Nutrition Plan Chatbot")

st.write("Enter your details to get a personalized nutrition plan.")

# User input
name = st.text_input("Name")
age = st.number_input("Age", min_value=0)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
weight = st.number_input("Weight (kg)", min_value=0.0)
height = st.number_input("Height (cm)", min_value=0.0)
activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly active", "Moderately active", "Very active", "Super active"])
health_goals = st.text_area("Health Goals (e.g., weight loss, muscle gain, maintain weight)")

# Generate nutrition plan button
if st.button("Generate Nutrition Plan"):
    user_info = f"Name: {name}\nAge: {age}\nGender: {gender}\nWeight: {weight} kg\nHeight: {height} cm\nActivity Level: {activity_level}\nHealth Goals: {health_goals}"
    nutrition_plan = generate_nutrition_plan(user_info)
    st.write("### Your Personalized Nutrition Plan")
    st.write(nutrition_plan)
