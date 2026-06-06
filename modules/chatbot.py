import gradio as gr
from modules.gemini_utils import get_gemini_response
from database.supabase_client import save_chat_to_db

def chatbot_interface(
    active_chat_id: gr.State, 
    all_chats_data: gr.State, 
    chat_titles: gr.State,
    user_id_state: gr.State,
    history_buttons: list
):
    with gr.Column(elem_classes=["chat-container"]) as layout:
        # Chat header inside view
        gr.HTML("""
            <div class='main-header'>
                <h2>💬 AI Career Assistant</h2>
                <span style='font-size: 12px; color: #10b981; background: #ecfdf5; padding: 4px 8px; border-radius: 12px; font-weight:600;'>Online</span>
            </div>
        """)
        
        # Scrollable chatbot container
        chatbot = gr.Chatbot(
            show_label=False, 
            container=False, 
            elem_classes=["chatbot-wrapper"],
            type="messages"
        )
        
        # Sticky chat input container at the bottom
        with gr.Row(elem_classes=["sticky-chat-input-row"]):
            with gr.Row(elem_classes=["chat-input-container"]):
                msg = gr.Textbox(
                    placeholder="Ask about placement preparation, resumes, or interview simulators...",
                    container=False,
                    scale=10,
                    lines=1,
                    max_lines=3,
                    show_label=False,
                    autofocus=True
                )
                send_btn = gr.Button("➔", elem_classes=["chat-send-btn"], scale=1)

        def respond(message, current_id, chats_dict, titles_dict, user_id):
            if not message or not message.strip():
                # Avoid empty submissions
                history = chats_dict.get(current_id, [])
                sidebar_updates = []
                chat_ids = list(chats_dict.keys())
                for i in range(5):
                    if i < len(chat_ids):
                        cid = chat_ids[i]
                        title = titles_dict.get(cid, "New Chat")
                        sidebar_updates.append(gr.update(value=f"💬 {title}", visible=True))
                    else:
                        sidebar_updates.append(gr.update(visible=False))
                return ["", history, chats_dict, titles_dict] + sidebar_updates

            # Get conversation history for active chat
            if current_id not in chats_dict:
                chats_dict[current_id] = []
            
            history = chats_dict[current_id]
            
            # Format history for LLM context (keep last 5 messages to avoid token blow-up)
            context_prompt = "You are Nexora AI, a professional career coach. Provide a helpful, encouraging, and detailed response in Markdown.\n\n"
            for msg_item in history[-5:]:
                role = "Candidate" if msg_item["role"] == "user" else "Coach"
                context_prompt += f"{role}: {msg_item['content']}\n"
            context_prompt += f"Candidate: {message}\nCoach:"
            
            # Append user message
            history.append({"role": "user", "content": message})
            chats_dict[current_id] = history
            
            # Update title if it's the first message
            if current_id not in titles_dict or titles_dict[current_id] == "New Chat":
                words = message.split()
                title = " ".join(words[:4]) + ("..." if len(words) > 4 else "")
                titles_dict[current_id] = title
            
            # Get bot response
            bot_message = get_gemini_response(context_prompt)
            
            # Save to database
            save_chat_to_db(user_id, message, bot_message)
            
            # Append bot message
            history.append({"role": "assistant", "content": bot_message})
            chats_dict[current_id] = history
            
            sidebar_updates = []
            chat_ids = list(chats_dict.keys())
            for i in range(5):
                if i < len(chat_ids):
                    cid = chat_ids[i]
                    title = titles_dict.get(cid, "New Chat")
                    sidebar_updates.append(gr.update(value=f"💬 {title}", visible=True))
                else:
                    sidebar_updates.append(gr.update(visible=False))
            
            return ["", history, chats_dict, titles_dict] + sidebar_updates

        # Bind events
        msg.submit(
            respond, 
            inputs=[msg, active_chat_id, all_chats_data, chat_titles, user_id_state], 
            outputs=[msg, chatbot, all_chats_data, chat_titles] + history_buttons
        )
        send_btn.click(
            respond, 
            inputs=[msg, active_chat_id, all_chats_data, chat_titles, user_id_state], 
            outputs=[msg, chatbot, all_chats_data, chat_titles] + history_buttons
        )

    return layout, chatbot
