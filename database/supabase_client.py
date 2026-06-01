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
        supabase: Client = None
    else:
        supabase: Client = create_client(url, key)
except Exception as e:
    print(f"Error initializing Supabase client: {str(e)}")
    supabase = None

def get_supabase() -> Client:
    return supabase

# Database Helper Functions
def save_chat_to_db(user_id: str, message: str, response: str):
    client = get_supabase()
    if client:
        try:
            client.table("chats").insert({
                "user_id": user_id,
                "message": message,
                "response": response
            }).execute()
        except Exception as e:
            print(f"DB Error (chats): {e}")

def save_resume_report(user_id: str, filename: str, report: str, score: int):
    client = get_supabase()
    if client:
        try:
            client.table("resumes").insert({
                "user_id": user_id,
                "filename": filename,
                "report": report,
                "score": score
            }).execute()
        except Exception as e:
            print(f"DB Error (resumes): {e}")

def save_interview_result(user_id: str, mode: str, score: int, feedback: str):
    client = get_supabase()
    if client:
        try:
            client.table("interviews").insert({
                "user_id": user_id,
                "mode": mode,
                "score": score,
                "feedback": feedback
            }).execute()
        except Exception as e:
            print(f"DB Error (interviews): {e}")

def get_user_stats(user_id: str):
    client = get_supabase()
    stats = {"chats": 0, "resumes": 0, "interviews": 0, "avg_score": 0}
    if client:
        try:
            c_res = client.table("chats").select("id", count="exact").eq("user_id", user_id).execute()
            r_res = client.table("resumes").select("score").eq("user_id", user_id).execute()
            i_res = client.table("interviews").select("score").eq("user_id", user_id).execute()
            
            stats["chats"] = c_res.count if c_res.count else 0
            stats["resumes"] = len(r_res.data)
            stats["interviews"] = len(i_res.data)
            
            all_scores = [r["score"] for r in r_res.data] + [i["score"] for i in i_res.data]
            if all_scores:
                stats["avg_score"] = sum(all_scores) / len(all_scores)
        except Exception as e:
            print(f"DB Error (stats): {e}")
    return stats
