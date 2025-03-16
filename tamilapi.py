import streamlit as st
import requests
from deep_translator import GoogleTranslator

# 🔹 Replace with your actual API key
MISTRAL_API_KEY = "9CUdAqhpHRcvEo2T380QVWyGl2I1QAHs"  

# 🔹 Function to call Mistral API with proper message format
def query_mistral(user_message):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-tiny",  # ✅ Use free-tier model
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "⚠️ No response received.")
    elif response.status_code == 401:
        return "🚨 API விசை பிழை: அங்கீகரிக்கப்படாதது (API விசையை சரிபார்க்கவும்)"
    elif response.status_code == 403:
        return "🚫 API அணுகல் மறுக்கப்பட்டது. உங்கள் திட்டத்தை மேம்படுத்தவும்."
    else:
        return f"⚠️ பிழை {response.status_code}: {response.text}"

# 🔹 Function for Tamil Processing
def generate_tamil_response(tamil_text):
    english_query = GoogleTranslator(source="ta", target="en").translate(tamil_text)
    english_response = query_mistral(english_query)
    tamil_response = GoogleTranslator(source="en", target="ta").translate(english_response)
    return tamil_response

# 🔹 Streamlit UI
st.set_page_config(page_title="தமிழ் AI", layout="centered")
st.title("📝 தமிழ் Generative AI Chatbot")

# User Input Box
tamil_text = st.text_area("**உங்கள் கேள்வியை தமிழில் உள்ளிடவும்**", height=150)

if st.button("🔄 பதில் உருவாக்கு"):
    if tamil_text.strip():
        with st.spinner("🔍 பதில் உருவாக்கப்படுகிறது..."):
            tamil_response = generate_tamil_response(tamil_text)
            st.success("✅ பதில்:")
            st.write(f"📝 **{tamil_response}**")
    else:
        st.warning("⚠️ தமிழில் ஒரு கேள்வியை உள்ளிடவும்!")

