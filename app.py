import os
import json
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

import openai
import whisper
import firebase_admin
from firebase_admin import credentials, firestore

# 🔐 Firebase from secrets
if not firebase_admin._apps:
    firebase_config = json.loads(st.secrets["FIREBASE_KEY"])
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 🔐 OpenAI from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 🎙️ Whisper model
whisper_model = whisper.load_model("base")

# 🖥️ Streamlit setup
st.set_page_config(page_title="TeluguSanskriti.ai", layout="centered")
st.title("🕉️ TeluguSanskriti.ai - Preserving Telugu Culture")

menu = st.sidebar.selectbox("Navigate", [
    "Home", "Cultural Chatbot", "Contribute", "Gallery", "Dialect Recorder"
])

# 🏠 Home
if menu == "Home":
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6e/Telugu_calligraphy_word.svg", width=200)
    st.subheader("🙏 Welcome to TeluguSanskriti.ai")
    st.write("Preserve and contribute to Telugu food, folklore, dialects, literature, and more.")

# 💬 Chatbot (OpenAI)
elif menu == "Cultural Chatbot":
    st.subheader("🤖 Ask About Telugu Culture (ChatGPT)")
    question = st.text_input("Ask a question:")
    if question and st.button("Ask ChatGPT"):
        with st.spinner("ChatGPT is thinking..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert in Telugu culture."},
                        {"role": "user", "content": question}
                    ]
                )
                st.markdown("**Answer:**")
                st.markdown(response["choices"][0]["message"]["content"])
            except Exception as e:
                st.error("❌ OpenAI failed to respond. Check your API key or question.")

# ✍️ Contribute
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

# 🖼️ Gallery
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

# 🎙️ Dialect Recorder
elif menu == "Dialect Recorder":
    st.subheader("🎙️ Upload Telugu Dialect Audio")
    dialect = st.selectbox("Dialect", ["Telangana", "Rayalaseema", "Coastal Andhra", "Other"])
    audio_file = st.file_uploader("Upload audio file", type=["wav", "mp3", "m4a"])
    if audio_file and st.button("Transcribe Audio"):
        audio_path = f"audio/{audio_file.name}"
        with open(audio_path, "wb") as f:
            f.write(audio_file.getbuffer())
        st.success("✅ Audio uploaded.")
        with st.spinner("Transcribing with Whisper..."):
            try:
                result = whisper_model.transcribe(audio_path)
                st.markdown("**Transcription:**")
                st.text(result["text"])
            except Exception as e:
                st.error("❌ Whisper failed to transcribe. Try another file.")
