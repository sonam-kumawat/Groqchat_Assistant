import os
import webbrowser
from dotenv import load_dotenv
from groq import Groq

# ---------------------- LOAD ENV ----------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found in .env file!")

# ---------------------- GROQ CLIENT ----------------------
client = Groq(api_key=GROQ_API_KEY)

# ---------------------- LLM CALL ----------------------
def generate_reply(message):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful chatbot."},
            {"role": "user", "content": message},
        ]
    )
    return response.choices[0].message.content

# ---------------------- COMMAND HANDLER ----------------------
def handle_special_commands(message):
    lower = message.lower()
    if lower.startswith("youtube "):
        query = message[8:]
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)
        return f"Opening YouTube search for '{query}'..."
    elif lower.startswith("google "):
        query = message[7:]
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return f"Opening Google search for '{query}'..."
    return None  # No special command
