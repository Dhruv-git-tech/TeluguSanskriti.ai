import os
import json
import streamlit as st
from datetime import datetime
from openai import OpenAI
import firebase_admin
from firebase_admin import credentials, firestore

# 🔐 Firebase from secrets
if not firebase_admin._apps:
    firebase_config = json.loads(st.secrets["FIREBASE_KEY"])
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ✅ OpenAI v1.x client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Streamlit UI setup
st.set_page_config(page_title="TeluguSanskriti.ai", layout="centered")
st.title("🕉️ TeluguSanskriti.ai - Preserving Telugu Culture")

menu = st.sidebar.selectbox("Navigate", ["Home", "Cultural Chatbot", "Contribute", "Gallery"])

# 🏠 Modernized Home Page
if menu == "Home":
    st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6e/Telugu_calligraphy_word.svg" width="180">
            <h2 style='margin-top: 10px;'>🙏 Welcome to <span style="color: #8B0000;">TeluguSanskriti.ai</span></h2>
            <p style='font-size: 16px;'>An open-source AI-powered initiative to preserve, celebrate, and crowdsource the rich cultural heritage of Telugu people — from food and folklore to literature and local dialects.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### ✨ What You Can Do:")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Ugadi_Pachadi.jpg/400px-Ugadi_Pachadi.jpg", use_column_width=True)
        st.markdown("**Share Recipes & Festivals**\n\nPost your stories, dishes, and rituals from your region.")

    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Kuchipudi.jpg/400px-Kuchipudi.jpg", use_column_width=True)
        st.markdown("**Explore Telugu Arts**\n\nLearn about dance forms, crafts, and performing traditions.")

    with col3:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Tenali_Rama.jpg/400px-Tenali_Rama.jpg", use_column_width=True)
        st.markdown("**Preserve Folklore**\n\nRecord your native dialect or share folk stories from elders.")

    st.markdown("---")
    st.info("📣 *Join our mission to build the largest open AI-ready cultural archive of Telugu heritage.*")

# 💬 OpenAI-powered Chatbot
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

# ✍️ Contribute Page
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

# 🖼️ Cultural Gallery with Uploads
elif menu == "Gallery":
    st.subheader("📸 Upload a Cultural Photo")
    uploaded_img = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    caption = st.text_input("Caption (optional)")
    if uploaded_img and st.button("Upload Image"):
        os.makedirs("uploads", exist_ok=True)  # Ensure folder exists
        img_path = f"uploads/{uploaded_img.name}"
        with open(img_path, "wb") as f:
            f.write(uploaded_img.getbuffer())
        st.success("✅ Uploaded successfully!")
        st.image(uploaded_img, caption=caption)
