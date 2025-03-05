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
num_prompts = st.sidebar.slider("🔢 Number of Prompts", 1, 5, 3)

# User input
topic = st.text_input("Enter a topic:")

if st.button("Generate Prompt"):
    if topic.strip() == "":
        st.warning("⚠️ Please enter a topic before generating a prompt.")
    else:
        with st.spinner("Generating your prompts..."):
            try:
                prompts = []
                for i in range(num_prompts):  # Generate multiple prompts
                    response = openai.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": f"You are an AI expert in {category} writing. Generate a {tone.lower()} and {prompt_length.lower()} prompt for a story about {topic}."},
                            {"role": "user", "content": f"Give me a {prompt_length.lower()} {tone.lower()} writing prompt in the {category.lower()} genre about {topic}."}
                        ]
                    )
                    prompts.append(response.choices[0].message.content)

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

# Footer
st.markdown("---")
st.write("Built by Sammy Dolan using OpenAI")