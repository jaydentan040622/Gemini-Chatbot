# Q&A Chatbot
#from langchain.llms import OpenAI

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image
import google.generativeai as genai
import random  # Add this import


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load OpenAI model and get respones

def get_gemini_response(input,image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    if input!="":
       response = model.generate_content([input,image])
    else:
       response = model.generate_content(image)
    return response.text

##initialize our streamlit app

st.set_page_config(page_title="Image Vision Explorer", page_icon="🔮")

st.title("🖼️ Image Vision Explorer")
st.markdown("Unlock the secrets hidden in your images with AI!")

# Add a fun fact about computer vision
vision_facts = [
    "Did you know? The first digital image was created in 1957!",
    "Fun fact: Computers can recognize faces faster than humans.",
    "AI tip: The more diverse your training data, the better the AI performs!",
]
st.info(random.choice(vision_facts))

input = st.text_input("🔍 Ask me anything about the image:", key="input", 
                      placeholder="E.g., 'What's the main color in this image?'")

uploaded_file = st.file_uploader("📤 Upload your image:", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Your masterpiece!", use_column_width=True)
    st.success("Image uploaded successfully! Now, ask me something about it.")

submit = st.button("🚀 Analyze Image", type="primary")

if submit:
    if image:
        with st.spinner("🧠 Gemini is thinking..."):
            response = get_gemini_response(input, image)
        st.subheader("🎨 Here's what I see:")
        st.write(response)
        st.balloons()
    else:
        st.error("Oops! Please upload an image before analyzing.")

st.markdown("---")
st.markdown("Made with ❤️ by Your Name | Powered by Google's Gemini AI")
