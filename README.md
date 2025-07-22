
# TeluguSanskriti.ai

An open-source Streamlit app to preserve Telugu culture using AI and community contributions.

---

## 🛠️ Features

- 🤖 AI-powered Gemini chatbot for cultural Q&A
- 📝 Community submissions (folklore, proverbs, recipes)
- 🎙️ Dialect audio upload + Whisper transcription
- 📸 Cultural photo gallery
- ☁️ Firebase Firestore backend for storing submissions

---

## 🔧 Setup Instructions (Local)

### 1. Clone Repo & Install

```bash
pip install -r requirements.txt
```

### 2. Add Firebase Key

Save your Firebase Admin JSON as `firebase_key.json`

### 3. Add Gemini API Key

Create `.env` with:

```env
GEMINI_API_KEY=your_google_api_key
```

### 4. Run App

```bash
streamlit run app.py
```

---

## ☁️ Streamlit Cloud Deployment

1. Push to GitHub
2. Add `.streamlit/secrets.toml` in your repo
3. Paste your Firebase JSON & Gemini API Key
4. Deploy from [Streamlit Cloud](https://streamlit.io/cloud)

---

Made with ❤️ to preserve Telugu culture!
