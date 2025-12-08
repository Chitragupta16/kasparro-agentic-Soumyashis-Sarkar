# src/config.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Configure Gemini
genai.configure(api_key=API_KEY)

def get_gemini_model():
    """Returns the configured model instance."""
    # Using 1.5 Flash for speed and efficiency
    return genai.GenerativeModel('gemini-flash-latest')