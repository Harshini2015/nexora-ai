import os
import time
import groq
from dotenv import load_dotenv

load_dotenv()

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    return groq.Groq(api_key=api_key)

def get_gemini_response(prompt, retries=3, delay=2):
    for i in range(retries):
        try:
            client = get_groq_client()
            chat_completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1024
            )
            response_text = chat_completion.choices[0].message.content
            if not response_text:
                return "Error: Groq returned an empty response."
            return response_text
        except groq.RateLimitError:
            if i < retries - 1:
                time.sleep(delay * (2 ** i))
                continue
            return "Error: Rate limit exceeded. Please try again later."
        except groq.APIError as e:
            if i < retries - 1:
                time.sleep(delay * (2 ** i))
                continue
            return f"Error: API error - {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"
    return "Error: Maximum retries reached."
