import gradio as gr
import re
from modules.gemini_utils import get_gemini_json


from database.supabase_client import save_chat_to_db

from modules.session_utils import get_or_create_user_id


def chatbot_interface():
    user_id_state = gr.State(None)
    
    with gr.Column() as layout:
        gr.Markdown("AI Career Assistant")
        gr.Markdown("Ask questions about placements, preparation, and industry trends.")
        
        chatbot = gr.Chatbot(label="Conversation", height=450)

        
        with gr.Row():
            msg = gr.Textbox(
                label="Your Question",
                placeholder="How do I prepare for a Technical Interview?",
                scale=8
            )
            send_btn = gr.Button("Send", variant="primary", scale=2)
            
        clear_btn = gr.Button("Clear Chat History", size="sm")

        def respond(message, chat_history, user_id_state_val):
            user_id = get_or_create_user_id(user_id_state_val)
            if not message:
                return "", chat_history, user_id
            
            structured_prompt = (
                "You are Nexora AI, a professional career coach for students. "
                f"Provide a helpful, encouraging, and concise response to: {message}"
            )
            
            bot_message = ""
            try:
                payload = get_gemini_json(
                    "Return ONLY valid JSON with schema {\"response\": str}. Do not include any other text.\n"
                    + structured_prompt,
                    schema={"response": str},
                    retries=3,
                    delay=2,
                )
                bot_message = payload["response"]
            except Exception:
                bot_message = "Sorry—could not generate a response right now." 

            
            # Save to Supabase
            save_chat_to_db(user_id, message, bot_message)
            
            chat_history.append((message, bot_message))
            return "", chat_history, user_id

        msg.submit(respond, [msg, chatbot, user_id_state], [msg, chatbot, user_id_state])
        send_btn.click(respond, [msg, chatbot, user_id_state], [msg, chatbot, user_id_state])
        clear_btn.click(lambda x: None, inputs=[user_id_state], outputs=[user_id_state], queue=False)

    
    return layout
