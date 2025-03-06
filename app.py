import openai
import streamlit as st

# Load API key securely from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# =============================
# Sidebar - User Customization Options
# =============================

st.sidebar.header("🎨 Customize Your Prompt")

# Choose the length of the AI-generated prompt
prompt_length = st.sidebar.selectbox("📏 Select Prompt Length:", ["Short", "Medium", "Long"])

# Choose the tone of the AI-generated prompt
tone = st.sidebar.selectbox("🎭 Select Writing Tone:", ["Creative", "Formal", "Humorous", "Inspiring"])

# Choose the category/genre for the writing prompt
category = st.sidebar.selectbox("📖 Select Prompt Category:", ["General", "Sci-Fi", "Mystery", "Romance"])

# Choose the number of prompts to generate (from 1 to 5)
num_prompts = st.sidebar.slider("🔢 Number of Prompts", 1, 5, 3)


# =============================
# Main UI - AI Prompt Generator
# =============================

# App Title
st.title("📝 AI Writing Prompt Generator")

# App Description
st.write("Generate creative writing prompts with AI! Customize the style, length, and tone.")

# User Input: Enter a topic for the AI to generate a prompt
topic = st.text_input("Enter a topic:")

# Button to generate AI prompts
if st.button("Generate Prompt"):
    if topic.strip() == "": # Check if the topic is empty
        st.warning("⚠️ Please enter a topic before generating a prompt.")
    else:
        with st.spinner("Generating your prompts..."): # Show loading spinner
            try:
                # Request multiple prompts in a single API call
                response = openai.chat.completions.create(
                        model="gpt-4",
                        messages=[
                        {
                            "role": "system",
                            "content": f"You are an AI expert in {category} writing. Generate {num_prompts} {tone.lower()} and {prompt_length.lower()} prompts for a story about {topic}."
                        }
                    ]
                )

                # Split the response into separate prompts
                prompts = response.choices[0].message.content.split("\n") )

                # Display prompts
                st.success("✅ Here are your AI-generated prompts:")
                full_prompt_text = "\n\n".join([f"**Prompt {i+1}:** {p}" for i, p in enumerate(prompts)])  # Format for display
                st.write(full_prompt_text)

                # "Copy Prompt" Button
                st.button("📋 Copy to Clipboard", key="copy_button")
                st.code(full_prompt_text, language="markdown")

                # "Download Prompt" Option
                st.download_button("💾 Download Prompts", full_prompt_text, file_name="ai_prompts.txt")

            except Exception as e:
                st.error(f"🚨 Error: {e}")

# =============================
# Footer
# =============================

st.markdown("---")
st.write("Built by Sammy Dolan using OpenAI")