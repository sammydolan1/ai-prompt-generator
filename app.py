import openai
import streamlit as st
import random

# Load API key securely from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# =============================
# Styles
# =============================

st.markdown("""
    <style>
        .title {
            color: #008cba !important;
            text-align: center;
            font-size: 36px;
            font-weight: bold;
        }
        .subtitle {
            color: #555;
            text-align: center;
            font-size: 18px;
        }
        .stButton>button {
            background-color: #008CBA !important;
            color: white !important;
            border-radius: 8px;
            font-size: 18px;
        }
        .stMarkdown {
            font-size: 18px !important;
        }
    </style>
""", unsafe_allow_html=True)

# =============================
# Main UI - AI Prompt Generator
# =============================

# App Title
st.markdown("<h1 class='title'>📝 AI Writing Prompt Generator</h1>", unsafe_allow_html=True)

# App Description
st.markdown("<p class='subtitle'>Generate creative writing prompts with AI! Customize the style, length, and tone.</p>", unsafe_allow_html=True)

# Using columns to improve UI layout
col1, col2 = st.columns(2)

with col1:

    # Choose the tone of the AI-generated prompt
    tone = st.selectbox("🎭 Select Writing Tone:", ["Creative", "Formal", "Humorous", "Inspiring", "Dramatic", "Casual", "Poetic", "Suspenseful", "Motivational", "Whimsical"])

    # Predefined list of random topics
    random_topics = [
        "A time traveler who gets stuck in a coffee shop",
        "A lost civilization hidden beneath the ocean",
        "A detective who can read memories from objects",
        "A robot discovering emotions for the first time",
        "A mysterious book that rewrites itself",
        "An alien invasion with an unexpected twist"
        "A scientist discovers a portal to a parallel universe",
        "A ghost seeking revenge on their past life enemies",
        "A child who wakes up with the ability to stop time",
        "A medieval kingdom where dragons are actually extinct",
        "A hacker who accidentally exposes a world-changing secret",
        "A spaceship lost in deep space finds an abandoned alien city",
        "An artist who paints scenes that later come to life",
        "A musician who finds a cursed instrument that plays itself",
        "A billionaire who fakes their own death to solve a mystery",
        "A journalist uncovering the truth behind a legendary monster",
        "A town where no one has slept in over a decade",
        "A secret underground society controlling the world’s history",
        "A detective investigating a series of crimes committed in dreams"
    ]

    # Initialize topic in session state if not set
    if "topic" not in st.session_state:
        st.session_state.topic = ""

    # User Input: Enter a topic for the AI to generate a prompt
    topic = st.text_input("✍️ Enter a topic:", value=st.session_state.topic, placeholder="Type your topic or hit Surprise Me!", help="Enter a subject for the AI to generate prompts about. Surprise Me button will generate a random topic.")

    # Surprise Me! button to generate a random topic
    if st.button("🎲 Surprise Me!"):
        st.session_state.topic = random.choice(random_topics)
        st.rerun()

with col2:
    # Choose the category/genre for the writing prompt
    category = st.selectbox("📖 Select Prompt Category:", ["General", "Sci-Fi", "Mystery", "Romance", "Fantasy", "Horror", "Thriller", "Historical Fiction", "Comedy", "Dystopian", "Adventure"])

    # Choose the length of the AI-generated prompt
    prompt_length = st.selectbox("📏 Select Prompt Length:", ["Short", "Medium", "Long"])

    # Choose the number of prompts to generate (from 1 to 5)
    num_prompts = st.slider("🔢 Number of Prompts", 1, 5, 3)

# Button to generate AI prompts
if st.button("Generate Prompt", use_container_width=True):
    if st.session_state.topic.strip() == "": # Check if the topic is empty
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
                            "content": f"You are an AI expert in {category} writing. Generate {num_prompts} {tone.lower()} and {prompt_length.lower()} prompts for a story about {st.session_state.topic}."
                        }
                    ]
                )

                # Extract AI-generated response
                prompt_text = response.choices[0].message.content.strip()
                prompts = [p.lstrip("12345.) ") for p in prompt_text.split("\n") if p.strip()]  # Remove empty placeholders and leading numbers

                # Display prompts
                st.success("✅ Here are your AI-generated prompts:")
                for i, p in enumerate(prompts):
                    with st.expander(f"✨ Prompt {i+1}"):
                        st.text_area(f"Prompt {i+1}", value=p, height=100, key=f"text_{i}")
                
                full_prompt_text = "\n\n".join([f"Prompt {i+1}: {p}" for i, p in enumerate(prompts)])

                # "Download Prompts" Option
                st.download_button("💾 Download Prompts", full_prompt_text, file_name="ai_prompts.txt")

            except openai.error.AuthenticationError:
                st.error("🚨 Oops! Something went wrong. Please check your API key or contact support.")
            except openai.error.RateLimitError:
                st.error("⚠️ Too many requests! Please wait a moment and try again.")
            except openai.error.OpenAIError:
                st.error("⚠️ The AI is taking longer than expected. Try again in a few seconds.")
            except Exception:
                st.error("⚠️ Something went wrong. Please refresh the page and try again.")

# =============================
# Footer
# =============================

st.markdown("---")
st.write("Built by Sammy Dolan using OpenAI")