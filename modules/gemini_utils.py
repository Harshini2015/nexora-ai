import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def init_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def get_gemini_response(prompt, history=None):
    try:
        model = init_gemini()
        if history:
            chat = model.start_chat(history=history)
            response = chat.send_message(prompt)
        else:
            response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
