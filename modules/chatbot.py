import gradio as gr
import re
from modules.gemini_utils import get_gemini_response
from database.supabase_client import save_chat_to_db

def chatbot_interface():
    user_id_state = gr.State("student_user_01") # Placeholder for demo
    
    with gr.Column() as layout:
        gr.Markdown("### 💬 AI Career Assistant")
        gr.Markdown("Ask me about placements, preparation, or industry trends.")
        
        chatbot = gr.Chatbot(label="Conversation", height=450)
        
        with gr.Row():
            msg = gr.Textbox(
                label="Your Question",
                placeholder="How do I prepare for a Technical Interview?",
                scale=8
            )
            send_btn = gr.Button("Send", variant="primary", scale=2)
            
        clear_btn = gr.Button("Clear Chat History", size="sm")

        def respond(message, chat_history, user_id):
            if not message:
                return "", chat_history
            
            # Use a structured prompt for career guidance
            structured_prompt = f"You are Nexora AI, a professional career coach for students. Provide a helpful, encouraging, and concise response to: {message}"
            
            bot_message = get_gemini_response(structured_prompt)
            
            # Save to Supabase
            save_chat_to_db(user_id, message, bot_message)
            
            chat_history.append((message, bot_message))
            return "", chat_history

        msg.submit(respond, [msg, chatbot, user_id_state], [msg, chatbot])
        send_btn.click(respond, [msg, chatbot, user_id_state], [msg, chatbot])
        clear_btn.click(lambda: None, None, chatbot, queue=False)
    
    return layout
