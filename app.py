import json
import streamlit as st
import google.generativeai as genai
import firebase_admin 
from firebase_admin import credentials, firestore

st.set_page_config(page_title="AI Doubt Solver", page_icon="🤖", layout="wide")

# ----------------------------- SIDEBAR -----------------------------
with st.sidebar:
    st.title("AI Doubt Solver")
    st.title("Sessions")
    st.button("➕ New Session", on_click=lambda: st.session_state.update(messages=[]))
    st.markdown("Powered by **Gemini API** + **Firebase**")
    st.markdown("---")
    st.markdown("💬 Ask any academic doubt, get instant help, and review past Q&A.")
    st.caption("Made by Shobhit 🚀")

# ----------------------------- CONFIG -----------------------------
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# ✅ Firebase Init BEFORE any firestore call
if not firebase_admin._apps:
    cred_dict = json.loads(st.secrets["FIREBASE_CREDS"])
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ----------------------------- SESSION -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("AI Doubt Solver")
st.write("Ask me any question, and I’ll help you understand it better!")

# ----------------------------- CHAT -----------------------------
question = st.chat_input("Ask your doubt here...")

if question:
    st.chat_message("user").markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"You are an AI Doubt Solver and tutor. Explain the following doubt in a simple and short way:\n\n{question}"
            response = model.generate_content(prompt)

        st.markdown(response.text)

        # Store in history
        st.session_state.messages.append({
            "role": "assistant",
            "content": response.text
        })

        # ✅ Store in Firestore
        try:
            db.collection("doubts").add({
                "question": question,
                "answer": response.text,
            })
        except Exception as e:
            st.error(f"Firestore error: {e}")











    
    


