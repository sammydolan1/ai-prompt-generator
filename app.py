import openai
import os
import streamlit as st
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit App UI
st.title("AI Writing Prompt Generator ✍️")
st.write("Enter a topic below, and the AI will generate a unique writing prompt!")

# User input
topic = st.text_input("Enter a topic:", "")

if st.button("Generate Prompt"):
    if topic.strip() == "":
        st.warning("Please enter a topic before generating a prompt.")
    else:
        with st.spinner("Generating your prompt..."):
            try:
                response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert creative writing assistant."},
                        {"role": "user", "content": f"Give me a unique writing prompt about {topic}."}
                    ]
                )
                prompt = response.choices[0].message.content
                st.success("Here is your AI-generated prompt:")
                st.write(prompt)
            except Exception as e:
                st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.write("Built with ❤️ using OpenAI & Streamlit")