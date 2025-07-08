import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import firebase_admin 
from firebase_admin import credentials, firestore
from firebase_admin import auth
import json



st.set_page_config(page_title="AI Doubt Solver", page_icon="🤖", layout="wide")

with st.sidebar:
    st.title("AI Doubt Solver")
    st.title("Sessions")
    st.button("➕ New Session", on_click=lambda: st.session_state.update(messages=[]))
    st.markdown("Powered by **Gemini API** + **Firebase**")
    st.markdown("---")
    st.markdown("💬 Ask any academic doubt, get instant help, and review past Q&A.")
    st.caption("Made by Shobhit 🚀")


api_key = st.secrets["GEMINI_API_KEY"]
    
# Intialize session state variable

if "messages" not in st.session_state:
    st.session_state.messages = []


st.title("AI Doubt Solver")
st.write("Ask me any question, and I’ll help you understand it better!")


# Load API key from .env file
genai.configure(api_key=api_key)

# Ask user for a qustion
# User input box
if question := st.chat_input("Ask your doubt here..."):
    # Display user message
    st.chat_message("user").markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

#Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"Answer in a simple and clear way:\n\n{question}"
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})



st.write("Reading Firebase credentials...")
try:
    cred_dict = json.loads(st.secrets["FIREBASE_CREDS"])
    st.success("Secret loaded correctly")
except Exception as e:
    st.error(f"Secret loading failed: {e}")


 #save to firebase
        db = firestore.client()  
        db.collection("doubts").add({
            "question": question,
            "answer": response.text,
        })       



    
    

#Firebase Setup
if not firebase_admin._apps:
    cred_dict = json.loads(st.secrets["FIREBASE_CREDS"])
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()










    
    


