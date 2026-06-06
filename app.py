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

    with gr.Blocks(
        title="Nexora-AI",
        css=css_content,
        js=js_content,
        theme=gr.themes.Default()
    ) as demo:
        # App-level states for multiple chat sessions
        active_chat_id = gr.State("chat_1")
        all_chats_data = gr.State({"chat_1": []})
        chat_titles = gr.State({"chat_1": "New Chat"})
        user_id_state = gr.State("student_user_01")
        
        # Outer Row App Shell Layout (Complete Leftside Sidebar, zero spacing)
        with gr.Row(elem_id="app-layout"):
            # 1. Left Sidebar
            with gr.Column(elem_id="sidebar") as sidebar:
                # Brand logo space at the top (UPSIDE) in BLOCK LETTERS
                gr.HTML(
                    """
                    <div class="sidebar-brand">
                        <div class="brand-text">Nexora-AI</div>
                    </div>
                    """
                )
                
                with gr.Column(elem_classes=["sidebar-content"]):
                    home_nav = gr.Button("🏠 Home", variant="secondary", elem_classes=["nav-btn", "active"], elem_id="nav-home")
                    chat_nav = gr.Button("💬 Chat Assistant", variant="secondary", elem_classes=["nav-btn"], elem_id="nav-chat")
                    resume_nav = gr.Button("📄 Resume Analyzer", variant="secondary", elem_classes=["nav-btn"], elem_id="nav-resume")
                    interview_nav = gr.Button("🎤 Interview Simulator", variant="secondary", elem_classes=["nav-btn"], elem_id="nav-interview")
                    career_nav = gr.Button("🎯 Career Planner", variant="secondary", elem_classes=["nav-btn"], elem_id="nav-career")
                    
                # Sidebar footer (Settings)
                with gr.Column(elem_classes=["sidebar-footer"]):
                    settings_nav = gr.Button("⚙️ Settings", variant="secondary", elem_classes=["nav-btn"], elem_id="nav-settings")
                    
            # 2. Main content area
            with gr.Column(elem_id="main-panel") as main_panel:
                # Floating Sidebar Toggle button
                sidebar_toggle_btn = gr.Button("☰", elem_id="sidebar-toggle-btn")
                
                # Mount all subviews
                views, cards, chatbot_ref, reset_btn = mount_feature_views(
                    active_chat_id=active_chat_id,
                    all_chats_data=all_chats_data,
                    chat_titles=chat_titles,
                    user_id_state=user_id_state
                )

        # UI Wiring: Navigation Button and view definitions
        nav_buttons = {
            "home": home_nav,
            "chat": chat_nav,
            "resume": resume_nav,
            "interview": interview_nav,
            "career": career_nav,
            "settings": settings_nav
        }

        # Wire navigation buttons click events to JS handler for instant client-side page switching
        for btn_name, button in nav_buttons.items():
            button.click(
                None,
                inputs=None,
                outputs=None,
                js=f"() => {{ window.navigateToPage('{btn_name}'); }}"
            )

        # Wire home landing cards to JS handler for instant client-side page switching
        cards["chat"].click(None, inputs=None, outputs=None, js="() => { window.navigateToPage('chat'); }")
        cards["resume"].click(None, inputs=None, outputs=None, js="() => { window.navigateToPage('resume'); }")
        cards["interview"].click(None, inputs=None, outputs=None, js="() => { window.navigateToPage('interview'); }")
        cards["career"].click(None, inputs=None, outputs=None, js="() => { window.navigateToPage('career'); }")

        # Sidebar Collapsible JS handler
        sidebar_toggle_btn.click(
            None,
            None,
            None,
            js="() => { window.toggleSidebar(); }"
        )

        # Settings Clear/Reset handler
        def reset_application():
            new_id = f"chat_{uuid.uuid4().hex[:8]}"
            chats_dict = {new_id: []}
            titles_dict = {new_id: "New Chat"}
            empty_chatbot_val = []
            return [new_id, chats_dict, titles_dict, empty_chatbot_val]

        reset_btn.click(
            reset_application,
            inputs=None,
            outputs=[active_chat_id, all_chats_data, chat_titles, chatbot_ref],
            js="() => { window.navigateToPage('home'); }"
        )

    print("[Nexora AI] Starting on port 7860...")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True,
        prevent_thread_lock=False
    )

if __name__ == "__main__":
    main()
