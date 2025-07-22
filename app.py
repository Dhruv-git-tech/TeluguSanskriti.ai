import os
import json
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

import openai
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

# 🖥️ Streamlit UI config
st.set_page_config(page_title="TeluguSanskriti.ai", layout="centered")
st.title("🕉️ TeluguSanskriti.ai - Preserving Telugu Culture")

menu = st.sidebar.selectbox("Navigate", [
    "Home", "Cultural Chatbot", "Contribute", "Gallery"
])

# 🏠 Home Page
if menu == "Home":
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6e/Telugu_calligraphy_word.svg", width=200)
    st.subheader("🙏 Welcome to TeluguSanskriti.ai")
    st.write("Preserve and contribute to Telugu food, folklore, dialects, literature, and more.")

# 💬 Chatbot (with error logging)
elif menu == "Cultural Chatbot":
    st.subheader("🤖 Ask About Telugu Culture (Powered by ChatGPT)")
    question = st.text_input("Ask your question:")
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
                answer = response["choices"][0]["message"]["content"]
                st.markdown("**Answer:**")
                st.markdown(answer)
            except Exception as e:
                st.error(f"❌ Error: {e}")

# ✍️ Contribution Page
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

# 🖼️ Gallery Page
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
