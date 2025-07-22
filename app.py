import os
import json
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

import google.generativeai as genai
import whisper

import firebase_admin
from firebase_admin import credentials, firestore

# 🌐 Load Firebase credentials from Streamlit Secrets
if not firebase_admin._apps:
    firebase_config = json.loads(st.secrets["FIREBASE_KEY"])
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 🤖 Load Gemini key from secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
gemini_model = genai.GenerativeModel("gemini-pro")

# 🎙️ Load Whisper model once
whisper_model = whisper.load_model("base")

# 🚀 Streamlit Config
st.set_page_config(page_title="TeluguSanskriti.ai", layout="centered")
st.title("🕉️ TeluguSanskriti.ai - Preserving Telugu Culture")

# 🔄 Menu
menu = st.sidebar.selectbox("Navigate", [
    "Home", "Cultural Chatbot", "Contribute", "Gallery", "Dialect Recorder"
])

# 🏠 Home Page
if menu == "Home":
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6e/Telugu_calligraphy_word.svg", width=200)
    st.subheader("🙏 Welcome to TeluguSanskriti.ai")
    st.write("Preserve and contribute to Telugu food, folklore, dialects, literature, and more.")

# 💬 Gemini Cultural Chatbot
elif menu == "Cultural Chatbot":
    st.subheader("🤖 Ask About Telugu Culture")
    question = st.text_input("Ask a question (English or Telugu):")
    if question and st.button("Ask Gemini"):
        with st.spinner("Gemini is thinking..."):
            try:
                response = gemini_model.generate_content(question)
                st.markdown("**Answer:**")
                st.markdown(response.text)
            except Exception as e:
                st.error("Gemini failed to respond. Check your API key or question format.")

# ✍️ Contribute to the Culture
elif menu == "Contribute":
    st.subheader("📝 Share a Cultural Contribution")
    category = st.selectbox("Category", ["Folklore", "Festival", "Recipe", "Proverb", "Other"])
    title = st.text_input("Title")
    content = st.text_area("Describe your entry")
    name = st.text_input("Your Name (optional)")
    if st.button("Submit"):
        doc = {
            "category": category,
            "title": title,
            "content": content,
            "name": name,
            "timestamp": datetime.utcnow()
        }
        db.collection("contributions").add(doc)
        st.success("✅ Your contribution has been saved. Thank you!")

# 🖼️ Cultural Image Gallery
elif menu == "Gallery":
    st.subheader("📸 Upload a Cultural Photo")
    uploaded_img = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    caption = st.text_input("Caption (optional)")
    if uploaded_img and st.button("Upload Image"):
        img_path = f"uploads/{uploaded_img.name}"
        with open(img_path, "wb") as f:
            f.write(uploaded_img.getbuffer())
        st.success("✅ Uploaded successfully!")
        st.image(uploaded_img, caption=caption)

# 🔊 Dialect Recorder + Whisper Transcription
elif menu == "Dialect Recorder":
    st.subheader("🎙️ Upload Telugu Dialect Audio")
    dialect = st.selectbox("Dialect", ["Telangana", "Rayalaseema", "Coastal Andhra", "Other"])
    audio_file = st.file_uploader("Upload audio file", type=["wav", "mp3", "m4a"])
    if audio_file and st.button("Transcribe Audio"):
        audio_path = f"audio/{audio_file.name}"
        with open(audio_path, "wb") as f:
            f.write(audio_file.getbuffer())
        st.success("✅ Audio uploaded successfully.")
        with st.spinner("Transcribing with Whisper..."):
            try:
                result = whisper_model.transcribe(audio_path)
                st.markdown("**Transcription:**")
                st.text(result["text"])
            except Exception as e:
                st.error("❌ Transcription failed. Try a different audio format.")
