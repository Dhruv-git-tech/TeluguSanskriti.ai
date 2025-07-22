import os
import json
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

from openai import OpenAI
import firebase_admin
from firebase_admin import credentials, firestore

# 🔐 Firebase from secrets
if not firebase_admin._apps:
    firebase_config = json.loads(st.secrets["FIREBASE_KEY"])
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ✅ Use OpenAI SDK v1.x
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="TeluguSanskriti.ai", layout="centered")
st.title("🕉️ TeluguSanskriti.ai - Preserving Telugu Culture")

menu = st.sidebar.selectbox("Navigate", ["Home", "Cultural Chatbot", "Contribute", "Gallery"])

if menu == "Home":
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6e/Telugu_calligraphy_word.svg", width=200)
    st.subheader("🙏 Welcome to TeluguSanskriti.ai")
    st.write("Preserve and contribute to Telugu food, folklore, dialects, literature, and more.")

elif menu == "Cultural Chatbot":
    st.subheader("🤖 Ask About Telugu Culture (ChatGPT)")
    question = st.text_input("Ask your question:")
    if question and st.button("Ask ChatGPT"):
        with st.spinner("ChatGPT is thinking..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert in Telugu culture."},
                        {"role": "user", "content": question}
                    ]
                )
                st.markdown("**Answer:**")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"❌ Error: {e}")

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
