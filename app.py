
import os
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
import google.generativeai as genai
import whisper
import json

st.set_page_config(page_title="TeluguSanskriti.ai", layout="centered")

# Load env or Streamlit secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    firebase_config = json.loads(st.secrets["FIREBASE_KEY"])
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)
else:
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
model = genai.GenerativeModel("gemini-pro")
whisper_model = whisper.load_model("base")

st.title("🕉️ TeluguSanskriti.ai - Preserving Telugu Culture")

menu = st.sidebar.selectbox("Navigate", ["Home", "Cultural Chatbot", "Contribute", "Gallery", "Dialect Recorder"])

if menu == "Home":
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6e/Telugu_calligraphy_word.svg", width=200)
    st.subheader("🙏 Welcome!")
    st.write("This open-source app aims to preserve Telugu cultural heritage.")

elif menu == "Cultural Chatbot":
    st.subheader("🤖 Ask About Telugu Culture")
    question = st.text_input("Ask your question")
    if question and st.button("Ask Gemini"):
        with st.spinner("Gemini is thinking..."):
            response = model.generate_content(question)
            st.markdown(response.text)

elif menu == "Contribute":
    st.subheader("✍️ Share Your Contribution")
    category = st.selectbox("Category", ["Folklore", "Festival", "Recipe", "Proverb", "Other"])
    title = st.text_input("Title")
    content = st.text_area("Description / Content")
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
        st.success("Thanks for your contribution!")

elif menu == "Gallery":
    st.subheader("📸 Cultural Gallery")
    uploaded_img = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
    caption = st.text_input("Caption")
    if st.button("Upload") and uploaded_img:
        with open(f"uploads/{uploaded_img.name}", "wb") as f:
            f.write(uploaded_img.getbuffer())
        st.success("Uploaded!")
        st.image(uploaded_img, caption=caption)

elif menu == "Dialect Recorder":
    st.subheader("🎙️ Upload Telugu Dialect Audio")
    dialect = st.selectbox("Dialect", ["Coastal", "Telangana", "Rayalaseema", "Other"])
    audio = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])
    if st.button("Submit & Transcribe") and audio:
        path = f"audio/{audio.name}"
        with open(path, "wb") as f:
            f.write(audio.getbuffer())
        st.success("Uploaded successfully.")
        st.markdown("**Transcription:**")
        result = whisper_model.transcribe(path)
        st.text(result["text"])
