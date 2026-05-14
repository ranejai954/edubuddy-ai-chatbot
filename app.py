# EduBuddy - AI Learning Assistant (Powered by Groq)
# SDG 4: Quality Education

import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()

# Get API key
API_KEY = os.getenv("GROQ_API_KEY")

# Check if API key exists
if not API_KEY:
    st.error("⚠️ GROQ_API_KEY not found. Please add it to your .env file.")
    st.stop()

# Initialize Groq client
try:
    client = Groq(api_key=API_KEY)
except Exception as e:
    st.error(f"Failed to initialize Groq client: {e}")
    st.stop()

# Page setup
st.set_page_config(page_title="EduBuddy - AI Study Buddy", page_icon="📚")

# Title
st.title("📚 EduBuddy - AI Learning Assistant")
st.markdown("*Your 24/7 study companion. Ask me anything!*")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me a question..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Prepare messages for Groq
                messages = []
                for m in st.session_state.messages:
                    messages.append({"role": m["role"], "content": m["content"]})
                
                # Call Groq API
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model="llama-3.1-8b-instant",  # Updated model name
                )
                reply = chat_completion.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Try asking a simpler question or check your API key.")