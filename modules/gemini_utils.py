import os
import time
import google.generativeai as genai
from google.api_core import exceptions
from dotenv import load_dotenv

load_dotenv()

def init_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def get_gemini_response(prompt, history=None, retries=3, delay=2):
    for i in range(retries):
        try:
            model = init_gemini()
            if history:
                chat = model.start_chat(history=history)
                response = chat.send_message(prompt)
            else:
                response = model.generate_content(prompt)
            
            if not response or not response.text:
                return "Error: Gemini returned an empty response."
            return response.text
            
        except exceptions.ResourceExhausted:
            if i < retries - 1:
                time.sleep(delay * (2 ** i)) # Exponential backoff
                continue
            return "Error: Gemini API rate limit exceeded. Please try again later."
        except exceptions.ServiceUnavailable:
            if i < retries - 1:
                time.sleep(delay * (2 ** i))
                continue
            return "Error: Gemini service is currently unavailable. Please try again later."
        except Exception as e:
            return f"Error: {str(e)}"
    return "Error: Maximum retries reached."
