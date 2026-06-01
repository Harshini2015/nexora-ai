import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Load credentials from .env
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Create reusable Supabase client
try:
    if not url or not key:
        print("Warning: SUPABASE_URL or SUPABASE_KEY not found in environment variables.")
        supabase: Client = None
    else:
        supabase: Client = create_client(url, key)
except Exception as e:
    print(f"Error initializing Supabase client: {str(e)}")
    supabase = None

def get_supabase() -> Client:
    """Returns the initialized Supabase client."""
    return supabase

def save_chat(user_email: str, message: str, response: str):
    """Saves a chat message and response to the Supabase 'chats' table."""
    client = get_supabase()
    if client:
        try:
            data = {
                "user_email": user_email,
                "message": message,
                "response": response
            }
            client.table("chats").insert(data).execute()
        except Exception as e:
            print(f"Error saving chat to Supabase: {str(e)}")

def signup(email, password):
    """Signs up a new user using Supabase Auth."""
    client = get_supabase()
    if not client:
        return "Supabase client not initialized."
    try:
        response = client.auth.sign_up({"email": email, "password": password})
        if response.user:
            # Insert profile
            client.table("profiles").insert({"id": response.user.id, "email": email}).execute()
            return "Success! Please check your email for confirmation."
        return "Signup failed."
    except Exception as e:
        return f"Error: {str(e)}"

def login(email, password):
    """Logs in a user using Supabase Auth."""
    client = get_supabase()
    if not client:
        return None, "Supabase client not initialized."
    try:
        response = client.auth.sign_in_with_password({"email": email, "password": password})
        if response.session:
            return response.user.email, "Login successful!"
        return None, "Invalid credentials."
    except Exception as e:
        return None, f"Error: {str(e)}"

def logout():
    """Logs out the current user."""
    client = get_supabase()
    if client:
        try:
            client.auth.sign_out()
            return "Logged out successfully."
        except Exception as e:
            return f"Error: {str(e)}"
    return "Not logged in."
