import openai
import os
import streamlit as st

# Load API key securely from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]


# Streamlit App UI
st.title("AI Writing Prompt Generator ✍️")
st.write("Generate creative writing prompts with AI! Customize the style, length, and tone.")

# Sidebar customization
st.sidebar.header("🎨 Customize Your Prompt")
prompt_length = st.sidebar.selectbox("📏 Select Prompt Length:", ["Short", "Medium", "Long"])
tone = st.sidebar.selectbox("🎭 Select Writing Tone:", ["Creative", "Formal", "Humorous", "Inspiring"])
category = st.sidebar.selectbox("📖 Select Prompt Category:", ["General", "Sci-Fi", "Mystery", "Romance"])

# User input
topic = st.text_input("Enter a topic:")

if st.button("Generate Prompt"):
    if topic.strip() == "":
        st.warning("⚠️ Please enter a topic before generating a prompt.")
    else:
        with st.spinner("Generating your prompt..."):
            try:
                # Modify API request to include customization
                response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": f"You are an AI expert in {category} writing. Generate a {tone.lower()} and {prompt_length.lower()} prompt for a story about {topic}."},
                        {"role": "user", "content": f"Give me a {prompt_length.lower()} {tone.lower()} writing prompt in the {category.lower()} genre about {topic}."}
                    ]
                )
                prompt = response.choices[0].message.content
                st.success("✅ Here is your AI-generated prompt:")
                st.write(prompt)

            except Exception as e:
                st.error(f"🚨 Error: {e}")

# Footer
st.markdown("---")
st.write("Built by Sammy Dolan using OpenAI")