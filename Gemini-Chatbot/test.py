import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api = os.getenv("GOOGLE_API_KEY")

# API Config
if api:
    genai.configure(api_key=api)
else:
    st.error("Google API NOT FOUND OR NOT CORRECT") 

st.write("Welcome to the Therapist App!")

if 'messages' not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Enter your text here")
if user_input:
    # Process user input and generate bot response
    bot_response = "Bot's response" 
    def generate_text(user_input):
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(user_input)
            return response.text
    if st.button("Enter"):
        if user_input:
            responsetext= generate_text(user_input)
            if responsetext:  
                st.session_state.messages.append({"role": "assistant", "content": responsetext})
        else:
            st.error("you should enter text first")  # Replace with your bot logic

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])