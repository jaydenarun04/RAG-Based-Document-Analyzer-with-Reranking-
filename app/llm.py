import os

from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Create Groq Client
client = Groq(
    api_key=GROQ_API_KEY
)


def ask_groq(prompt: str):
    """
    Send the prompt to Groq and return the generated answer.
    """

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2,
        max_tokens=512
    )

    return response.choices[0].message.content