import os
import uuid
import socket
import gradio as gr

from modules.view_factory import mount_feature_views

def find_free_port(start_port: int = 7860, max_tries: int = 100) -> int:
    """Return the first free TCP port starting at start_port."""
    for port in range(start_port, start_port + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(("0.0.0.0", port))
                return port
            except OSError:
                continue
    raise RuntimeError(
        f"No free port found in range {start_port}-{start_port + max_tries - 1}."
    )

def main():
    # Load assets
    current_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(current_dir, "assets", "style.css")
    js_path = os.path.join(current_dir, "assets", "app.js")

    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()

    with open(js_path, "r", encoding="utf-8") as f:
        js_content = f.read()

    with gr.Blocks(title="Nexora AI", css=css_content, js=js_content) as demo:
        # App-level states for multiple chat sessions
        active_chat_id = gr.State("chat_1")
        all_chats_data = gr.State({"chat_1": []})
        chat_titles = gr.State({"chat_1": "New Chat"})
        user_id_state = gr.State("student_user_01")
        
        # Outer Row App Shell Layout
        with gr.Row(elem_id="app-layout"):
            # 1. Left Sidebar
            with gr.Column(elem_id="sidebar") as sidebar:
                # Brand logo space
                gr.HTML(
                    """
                    <div class="sidebar-brand">
                        <div style="font-size: 24px; color: #4f46e5; font-weight: 800;">🌌</div>
                        <div class="brand-text">Nexora AI</div>
                    </div>
                    """
                )
                
                with gr.Column(elem_classes=["sidebar-content"]):
                    # New Chat Button
                    new_chat_btn = gr.Button("+ New Chat", elem_classes=["new-chat-btn"])
                    
                    # Navigation Section
                    gr.HTML("<div style='font-size: 11px; text-transform: uppercase; color: #9ca3af; font-weight: 600; padding: 0 10px; letter-spacing: 0.5px; margin-top: 8px;'>Navigation</div>")
                    
                    home_nav = gr.Button("🏠 Home", variant="secondary", elem_classes=["nav-btn", "active"])
                    dashboard_nav = gr.Button("📊 Dashboard", variant="secondary", elem_classes=["nav-btn"])
                    chat_nav = gr.Button("💬 Chat Assistant", variant="secondary", elem_classes=["nav-btn"])
                    resume_nav = gr.Button("📄 Resume Analyzer", variant="secondary", elem_classes=["nav-btn"])
                    interview_nav = gr.Button("🎤 Interview Simulator", variant="secondary", elem_classes=["nav-btn"])
                    career_nav = gr.Button("🎯 Career Planner", variant="secondary", elem_classes=["nav-btn"])
                    analytics_nav = gr.Button("📈 Analytics", variant="secondary", elem_classes=["nav-btn"])
                    
                    # Chat history section
                    gr.HTML("<div class='sidebar-history-title' style='margin-top: 12px;'>Chat History</div>")
                    
                    # Pre-defined history buttons (up to 5 history slots)
                    history_buttons = []
                    for i in range(5):
                        btn = gr.Button("Empty Chat", visible=False, elem_classes=["sidebar-history-btn"])
                        history_buttons.append(btn)
                        
                # Sidebar footer (Settings & About)
                with gr.Column(elem_classes=["sidebar-footer"]):
                    settings_nav = gr.Button("⚙️ Settings", variant="secondary", elem_classes=["nav-btn"])
                    about_nav = gr.Button("ℹ️ About Nexora", variant="secondary", elem_classes=["nav-btn"])
                    
            # 2. Main content area
            with gr.Column(elem_id="main-panel") as main_panel:
                # Floating Sidebar Toggle button
                sidebar_toggle_btn = gr.Button("☰", elem_id="sidebar-toggle-btn")
                
                # Mount all subviews
                views, cards, chatbot_ref, reset_btn = mount_feature_views(
                    active_chat_id=active_chat_id,
                    all_chats_data=all_chats_data,
                    chat_titles=chat_titles,
                    user_id_state=user_id_state,
                    history_buttons=history_buttons
                )

        # UI Wiring: Navigation Button and view definitions
        nav_buttons = {
            "home": home_nav,
            "dashboard": dashboard_nav,
            "chat": chat_nav,
            "resume": resume_nav,
            "interview": interview_nav,
            "career": career_nav,
            "analytics": analytics_nav,
            "settings": settings_nav,
            "about": about_nav
        }

        # List of output components to refresh on navigation
        ordered_pages = ["home", "dashboard", "chat", "resume", "interview", "career", "analytics", "settings", "about"]
        output_components = [views[p] for p in ordered_pages] + [nav_buttons[b] for b in ordered_pages]

        def make_navigation(target_page):
            def handler():
                updates = []
                # 1. Update columns visibilities
                for p in ordered_pages:
                    updates.append(gr.update(visible=(p == target_page)))
                # 2. Update button active classes
                for b in ordered_pages:
                    classes = ["nav-btn", "active"] if b == target_page else ["nav-btn"]
                    updates.append(gr.update(elem_classes=classes))
                return updates
            return handler

        # Wire navigation buttons click events
        for btn_name, button in nav_buttons.items():
            button.click(
                make_navigation(btn_name),
                inputs=None,
                outputs=output_components,
                queue=False
            )

        # Wire home landing cards
        cards["chat"].click(make_navigation("chat"), inputs=None, outputs=output_components, queue=False)
        cards["resume"].click(make_navigation("resume"), inputs=None, outputs=output_components, queue=False)
        cards["interview"].click(make_navigation("interview"), inputs=None, outputs=output_components, queue=False)
        cards["career"].click(make_navigation("career"), inputs=None, outputs=output_components, queue=False)

        # Sidebar Collapsible JS handler
        sidebar_toggle_btn.click(
            None,
            None,
            None,
            js="() => { window.toggleSidebar(); }"
        )

        # Shared history sidebar logic
        def update_history_sidebar_logic(chats_dict, titles_dict, active_id):
            chat_ids = list(chats_dict.keys())
            updates = []
            for i in range(5):
                if i < len(chat_ids):
                    cid = chat_ids[i]
                    title = titles_dict.get(cid, "New Chat")
                    label = f"💬 {title}"
                    # Show button
                    updates.append(gr.update(value=label, visible=True))
                else:
                    updates.append(gr.update(visible=False))
            return updates

        # 1. New Chat creation handler
        def start_new_chat(chats_dict, titles_dict):
            new_id = f"chat_{uuid.uuid4().hex[:8]}"
            chats_dict[new_id] = []
            titles_dict[new_id] = "New Chat"
            
            empty_chatbot_val = []
            nav_updates = make_navigation("chat")()
            sidebar_updates = update_history_sidebar_logic(chats_dict, titles_dict, new_id)
            
            return [new_id, chats_dict, titles_dict, empty_chatbot_val] + nav_updates + sidebar_updates

        new_chat_btn.click(
            start_new_chat,
            inputs=[all_chats_data, chat_titles],
            outputs=[active_chat_id, all_chats_data, chat_titles, chatbot_ref] + output_components + history_buttons
        )

        # 2. History buttons dynamic click handlers
        def make_load_chat_handler(index):
            def load_chat_handler(chats_dict, titles_dict):
                chat_ids = list(chats_dict.keys())
                if index >= len(chat_ids):
                    # No-op updates if slot is empty
                    noop_updates = [gr.update() for _ in range(18 + 5)]
                    return [gr.update(), gr.update()] + noop_updates
                
                selected_id = chat_ids[index]
                history = chats_dict.get(selected_id, [])
                
                nav_updates = make_navigation("chat")()
                sidebar_updates = update_history_sidebar_logic(chats_dict, titles_dict, selected_id)
                
                return [selected_id, history] + nav_updates + sidebar_updates
            return load_chat_handler

        for idx, btn in enumerate(history_buttons):
            btn.click(
                make_load_chat_handler(idx),
                inputs=[all_chats_data, chat_titles],
                outputs=[active_chat_id, chatbot_ref] + output_components + history_buttons
            )

        # 3. Settings Clear/Reset handler
        def reset_application():
            new_id = f"chat_{uuid.uuid4().hex[:8]}"
            chats_dict = {new_id: []}
            titles_dict = {new_id: "New Chat"}
            
            empty_chatbot_val = []
            nav_updates = make_navigation("home")()
            sidebar_updates = update_history_sidebar_logic(chats_dict, titles_dict, new_id)
            
            return [new_id, chats_dict, titles_dict, empty_chatbot_val] + nav_updates + sidebar_updates

        reset_btn.click(
            reset_application,
            inputs=None,
            outputs=[active_chat_id, all_chats_data, chat_titles, chatbot_ref] + output_components + history_buttons
        )

        # 4. App load state setup callback
        def init_sidebar_history(chats_dict, titles_dict, active_id):
            return update_history_sidebar_logic(chats_dict, titles_dict, active_id)

        demo.load(
            init_sidebar_history, 
            inputs=[all_chats_data, chat_titles, active_chat_id], 
            outputs=history_buttons
        )

    print("[Nexora AI] Starting...")
    demo.launch(
        server_name="127.0.0.1",
        theme=gr.themes.Default(),
        show_error=True,
        prevent_thread_lock=True,
    )

if __name__ == "__main__":
    main()
