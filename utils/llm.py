# utils/llm.py

import os
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv

# Load & clean API key
load_dotenv(find_dotenv(), override=True)
api_key = os.getenv("GEMINI_API_KEY", "").strip()
genai.configure(api_key=api_key)

# Choose a Gemini model you have access to:
MODEL = "gemini-2.0-flash"

def generate_response(prompt: str) -> str:
    try:
        # Initialize the model
        model = genai.GenerativeModel(MODEL)
        # Generate content
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Loaded API key: {repr(api_key)}")
        return f"LLM Error: {str(e)}"
