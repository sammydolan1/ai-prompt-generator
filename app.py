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

# Theme Toggle: Allows users to switch between Light and Dark Mode
theme = st.sidebar.radio("🌓 Select Theme:", ["Light Mode", "Dark Mode"])

# =============================
# Dynamic CSS for Light/Dark Mode
# =============================

# Apply different styles depending on the selected theme
if theme == "Dark Mode":
    st.markdown(
        """
        <style>
            /* Dark Mode Styles */

            /* Change background and text color for the entire app */
            body, .stApp { background-color: #1E1E1E !important; color: white !important; }
            
            /* Style for buttons */
            .stButton>button { background-color: #4CAF50 !important; color: white !important; border-radius: 8px; padding: 10px 20px; }
            
            /* Style for text input fields */
            .stTextInput>div>div>input { background-color: #333 !important; color: white !important; }
            
            /* Change sidebar background color in Dark Mode */
            section[data-testid="stSidebar"] { background-color: #2C2F33 !important; color: white !important; }

            /* Improve text readability */
            .stMarkdown { font-size: 18px !important; }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
            /* Light Mode Styles */

            /* Change background and text color for the entire app */
            body, .stApp { background-color: white !important; color: black !important; }
            
            /* Style for buttons */
            .stButton>button { background-color: #4CAF50 !important; color: black !important; border-radius: 8px; padding: 10px 20px; }
            
            /* Style for text input fields */
            .stTextInput>div>div>input { background-color: #f3f3f3 !important; color: black !important; }
            
            /* Change sidebar background color in Dark Mode */
            .css-1d391kg { background-color: #f8f9fa !important; }
            
            /* Improve text readability */
            .stMarkdown { font-size: 18px !important; }
        </style>
        """,
        unsafe_allow_html=True
    )


# =============================
# 📝 Main UI - AI Prompt Generator
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
                prompts = [] # Store generated prompts

                # Loop through the number of prompts the user requested
                for i in range(num_prompts):  # Generate multiple prompts
                    response = openai.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": f"You are an AI expert in {category} writing. Generate a {tone.lower()} and {prompt_length.lower()} prompt for a story about {topic}."},
                            {"role": "user", "content": f"Give me a {prompt_length.lower()} {tone.lower()} writing prompt in the {category.lower()} genre about {topic}."}
                        ]
                    )

                    # Extract the AI-generated text
                    prompts.append(response.choices[0].message.content)

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