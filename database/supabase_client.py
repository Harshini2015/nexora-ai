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

def _safe_int(x, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:
        return default


def get_user_stats(user_id: str):
    """Return dashboard stats for a single user.

    Implementation is defensive because Supabase client response shapes can vary.
    We avoid relying on `count` fields that may not be present.
    """

    client = get_supabase()
    stats = {"chats": 0, "resumes": 0, "interviews": 0, "avg_score": 0}

    if not client:
        return stats

    try:
        # Count chats without relying on response.count shape
        chats_rows = client.table("chats").select("id").eq("user_id", user_id).execute()
        stats["chats"] = len(getattr(chats_rows, "data", []) or [])

        resumes_rows = client.table("resumes").select("score").eq("user_id", user_id).execute()
        resumes_data = getattr(resumes_rows, "data", []) or []
        stats["resumes"] = len(resumes_data)

        interviews_rows = client.table("interviews").select("score").eq("user_id", user_id).execute()
        interviews_data = getattr(interviews_rows, "data", []) or []
        stats["interviews"] = len(interviews_data)

        all_scores = [_safe_int(r.get("score")) for r in resumes_data] + [_safe_int(i.get("score")) for i in interviews_data]
        all_scores = [s for s in all_scores if s is not None]
        if all_scores:
            stats["avg_score"] = sum(all_scores) / len(all_scores)

    except Exception as e:
        print(f"DB Error (stats): {e}")

    return stats

