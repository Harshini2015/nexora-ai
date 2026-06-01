import gradio as gr
from modules.gemini_utils import get_gemini_response
from database.supabase_client import save_chat

def chatbot_interface():
    # We'll use a hidden textbox or gr.State to store the current user's email
    user_email_state = gr.State("harshini@example.com") # Default for now
    
    with gr.Column(visible=False, elem_classes="glass-card") as layout:
        gr.HTML("""
            <div style='margin-bottom: 24px;'>
                <h3 style='margin: 0; font-size: 20px; font-weight: 700;'>💬 AI Career Assistant</h3>
                <p style='margin: 0; font-size: 14px; color: #9ca3af;'>Ask anything about your career, skills, or job search.</p>
            </div>
        """)
        
        chatbot = gr.Chatbot(
            label=None,
            show_label=False,
            elem_id="nexora-chatbot",
            height=500
        )
        
        with gr.Row():
            msg = gr.Textbox(
                label=None,
                show_label=False,
                placeholder="Type your message here...",
                container=False,
                scale=9,
                elem_id="chat-input"
            )
            send_btn = gr.Button("🚀", scale=1, elem_classes="primary-btn")
        
        with gr.Row(variant="compact"):
            gr.HTML("""
                <div style='display: flex; gap: 8px; margin-top: 12px; overflow-x: auto; padding-bottom: 8px;'>
                    <span style='background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.2); padding: 6px 12px; border-radius: 20px; font-size: 12px; color: #a78bfa; cursor: pointer; white-space: nowrap;'>Explain Generative AI</span>
                    <span style='background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.2); padding: 6px 12px; border-radius: 20px; font-size: 12px; color: #a78bfa; cursor: pointer; white-space: nowrap;'>How to improve my resume?</span>
                    <span style='background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.2); padding: 6px 12px; border-radius: 20px; font-size: 12px; color: #a78bfa; cursor: pointer; white-space: nowrap;'>Interview tips for FAANG</span>
                </div>
            """)
        
        def respond(message, chat_history, user_email):
            if not message:
                return "", chat_history
            
            bot_message = get_gemini_response(message)
            
            # Save to Supabase
            save_chat(user_email, message, bot_message)
            
            chat_history.append((message, bot_message))
            return "", chat_history

        msg.submit(respond, [msg, chatbot, user_email_state], [msg, chatbot])
        send_btn.click(respond, [msg, chatbot, user_email_state], [msg, chatbot])
    
    return layout
