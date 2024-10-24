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

# model Function for generating text 
#def generate_text(text):
#    model=genai.GenerativeModel("gemini-pro")
#    response = model.generate_content(text) 
#    return response.text

class TherapistApp:
    def __init__(self):
        self.user_data = {}
    
    def welcome_message(self):
        st.write("Welcome to the Therapist App!")
        text = st.text_area("I'm here to listen and help you as best as I can.")
        name = st.text_area("What's your name? ")
        def generate_text(text):
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(text)
            return response.text
        if st.button("Enter"):
            st.write("Welcome" ,name)
            if text:
                responsetext= generate_text(text)
                if responsetext:  
                    st.subheader("AI response")
                    st.write(responsetext)
            else:
                st.error("you should enter text first")    


    def get_user_name(self):
        name = st.text_area("What's your name? ")
        self.user_data['name'] = name
        if st.button("Submit"):
            st.write("Welcome" ,name)

    def ask_feelings(self):
        feeling = st.text_area(f"How are you feeling today, {self.user_data['name']}? ")
        self.user_data['feeling'] = feeling
        self.respond_to_feelings(feeling)

    def respond_to_feelings(self, feeling):
        if st.button("submit"):
            if "good" in feeling or "great" in feeling:
                 
                 st.write("I'm glad to hear that! Keep up the positive spirit.")
            elif "sad" in feeling or "bad" in feeling or "not good" in feeling:
                 
                 st.write("I'm sorry to hear that. It might help to talk about it.")
            else:
                 st.write("Thank you for sharing. How else can I help you today?")

    def run(self):
        self.welcome_message()
        self.get_user_name()
        continue_session = st.text_area("Would you like to continue our session? (yes/no)")
        if st.button("enter"):
            while True:
                 self.ask_feelings()
                 if continue_session != 'yes':
                     st.write("Thank you for sharing today. Take care!")
                     break

if __name__ == "__main__":
    app = TherapistApp()


# streamlit part
st.title("Therapist Bot")
app.run()




