import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_prompt(topic):
    """Generates a creative writing prompt based on user input."""
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert creative writing assistant."},
            {"role": "user", "content": f"Give me a unique writing prompt about {topic}."}
        ]
    )
    return response.choices[0].message.content  # New response format

# Ask the user for input
topic = input("Enter a topic for a writing prompt: ")
print("\nHere is your AI-generated prompt:\n")
print(generate_prompt(topic))