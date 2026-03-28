import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

# The AI Engine Connection (Hidden & Safe)
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ----------------- WEBSITE DESIGN (ENGLISH) -----------------
st.set_page_config(page_title="Pilipek Labs", page_icon="🚀")
st.title("📦 Pilipek Labs: Order Parser")
st.write("Paste your raw WhatsApp or Instagram chats below to extract structured order data instantly!")

# The Input Box
chat_input = st.text_area("Paste Customer Chat Here:", height=150)

# The Magic Button
if st.button("Extract Data 🚀"):
    if chat_input:
        with st.spinner("Pilipek Labs AI is analyzing the text..."):
            prompt = f"""
            Extract the following info from the chat text: Customer Name, Phone Number, Full Delivery Address, Product Details, and Size.
            Return STRICTLY as a JSON object with keys: Name, Phone, Address, Product, Size.
            Chat Text: {chat_input}
            """
            try:
                response = model.generate_content(prompt)
                result = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(result)
                
                st.success("✅ Order Parsed Successfully! Ready for Excel.")
                df = pd.DataFrame([data])
                st.table(df)
            except Exception as e:
                st.error("❌ Invalid text format. Please clear and paste a valid order chat.")
    else:
        st.warning("⚠️ Please paste the chat in the box first!")
