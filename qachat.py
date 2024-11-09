from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

# Add this import for custom styling
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
import random

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini Pro model and get repsonses
model=genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])
def get_gemini_response(question):
    
    response=chat.send_message(question,stream=True)
    return response

##initialize our streamlit app

st.set_page_config(page_title="Q&A Demo", page_icon="🤖", layout="wide")

# Custom CSS for a more friendly and relaxed design
st.markdown("""
<style>
body {
    background-image: url('https://images.unsplash.com/photo-1585314062340-f1a5a7c9328d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: #333;
    font-family: 'Roboto', sans-serif;
}
.stApp {
    background-color: rgba(255, 255, 255, 0.85);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
div.stButton > button:first-child {
    background-color: #4CAF50;
    color: white;
    border-radius: 20px;
    padding: 10px 20px;
    font-size: 16px;
    transition: all 0.3s ease;
}
div.stButton > button:hover {
    background-color: #45a049;
    transform: scale(1.05);
}
.st-emotion-cache-1v0mbdj > img {
    border-radius: 50%;
}
</style>""", unsafe_allow_html=True)

# Friendly greetings
greetings = [
    "Hey there! 👋 Ready to chat about Adidas?",
    "Welcome to the Adidas chat zone! 🏃‍♂️",
    "What's up, sneakerhead? Let's talk Adidas! 👟",
    "Adidas fan? You're in the right place! 😎",
]

st.title("Adidas Friendly Chat Bot")
st.markdown(f"<h3 style='color: #4CAF50;'>{random.choice(greetings)}</h3>", unsafe_allow_html=True)

add_vertical_space(2)

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Create input field and submit button
input = st.text_input("What's on your mind?", key="input", placeholder="Ask me anything about Adidas...")
submit = st.button("Let's chat!", use_container_width=True)

if submit and input:
    with st.spinner("Thinking... 🤔"):
        response = get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    
    colored_header(label="Adidas Bot's Response", description="", color_name="light-blue-70")
    response_text = ""
    for chunk in response:
        response_text += chunk.text
    st.markdown(f"<div style='background-color: #e6f3ff; padding: 15px; border-radius: 10px;'>{response_text}</div>", unsafe_allow_html=True)
    st.session_state['chat_history'].append(("Bot", response_text))

# Display chat history with a more friendly design
if st.session_state['chat_history']:
    add_vertical_space(2)
    colored_header(label="Chat Highlights", description="", color_name="yellow-70")
    for role, text in reversed(st.session_state['chat_history']):
        with st.expander(f"{'🧑‍💻 You' if role == 'You' else '🤖 Adidas Bot'}: {text[:50]}..." if len(text) > 50 else f"{'🧑‍💻 You' if role == 'You' else '🤖 Adidas Bot'}: {text}"):
            st.markdown(f"<div style='background-color: {'#f0f0f0' if role == 'You' else '#e6f3ff'}; padding: 10px; border-radius: 10px;'>{text}</div>", unsafe_allow_html=True)

# Replace the clear chat button section with this:
if 'show_clear_confirmation' not in st.session_state:
    st.session_state.show_clear_confirmation = False

if st.button("Clear Chat History"):
    if st.session_state['chat_history']:
        st.session_state.show_clear_confirmation = True
    else:
        st.info("Chat history is already empty.")

if st.session_state.show_clear_confirmation:
    st.warning("Are you sure you want to clear the chat history?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, clear it"):
            st.session_state['chat_history'] = []
            st.session_state.show_clear_confirmation = False
            st.cache_data.clear()
            st.success("Chat history has been cleared!")
            st.rerun()
    with col2:
        if st.button("No, keep it"):
            st.session_state.show_clear_confirmation = False
            st.rerun()

# Add a fun fact or tip about Adidas at the bottom
adidas_facts = [
    "Did you know? The name 'Adidas' comes from the founder's name, Adolf 'Adi' Dassler.",
    "Adidas' iconic three stripes were bought for €1,600 and two bottles of whisky in 1951!",
    "The Adidas Superstar was the first low-top basketball shoe to feature an all-leather upper.",
    "Adidas has been the official sponsor of the FIFA World Cup since 1970.",
]

add_vertical_space(2)
st.markdown("---")
st.markdown(f"<p style='text-align: center; font-style: italic;'>👟 Fun Fact: {random.choice(adidas_facts)}</p>", unsafe_allow_html=True)




