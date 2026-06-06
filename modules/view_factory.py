import gradio as gr
from modules.chatbot import chatbot_interface
from modules.dashboard import dashboard_interface
from modules.resume_analyzer import resume_analyzer_interface
from modules.interview_simulator import interview_simulator_interface
from modules.career_planner import career_planner_interface
from modules.analytics import analytics_interface

def build_home_view():
    with gr.Column(elem_classes=["page-container"]) as layout:
        gr.HTML("""
            <div class="hero-section">
                <h1 class="hero-title">Welcome to Nexora AI</h1>
                <p class="hero-subtitle">Your comprehensive AI-powered career assistant. Resume checks, interactive interview prep, and personalized path roadmaps in a single workspace.</p>
            </div>
        """)
        
        gr.HTML("<h2 style='font-size: 18px; font-weight: 700; color: #111827; margin: 16px 0;'>🚀 Explore Core Features</h2>")
        
        with gr.Row(elem_classes=["cards-grid"]):
            chat_card = gr.Button("💬 AI Chat Coach\nInstant placement coaching and career advice.", elem_classes=["feature-card"])
            resume_card = gr.Button("📄 Resume Analyzer\nCheck ATS compatibility and get scoring feedback.", elem_classes=["feature-card"])
            interview_card = gr.Button("🎤 Interview Simulator\nPractice HR, DSA, and technical mock sessions.", elem_classes=["feature-card"])
            career_card = gr.Button("🎯 Career Planner\nBuild tailored timelines and monthly roadmaps.", elem_classes=["feature-card"])

        gr.HTML("""
            <div style="margin-top: 40px; background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <h3 style="margin:0 0 8px 0; font-size:16px; font-weight:700; color:#111827;">💡 Placement Preparation Tips</h3>
                <ul style="margin:0; padding-left:20px; font-size:13px; color:#4b5563; line-height:1.7;">
                    <li>Keep your resume concise: ideally a single page focusing on impact metrics.</li>
                    <li>Simulate mock interviews at least twice a week to build confidence and refine your structure.</li>
                    <li>Utilize the Career Planner to identify technical skill gaps early.</li>
                </ul>
            </div>
        """)
        
    return layout, chat_card, resume_card, interview_card, career_card

def build_settings_view():
    with gr.Column(elem_classes=["page-container"]) as layout:
        gr.HTML("""
            <div style='margin-bottom: 24px;'>
                <h1 style='font-size: 24px; font-weight: 800; color: #111827; margin: 0;'>⚙️ Settings</h1>
                <p style='color: #4b5563; font-size: 14px; margin-top: 4px;'>Manage app configurations and details.</p>
            </div>
        """)
        
        with gr.Column(scale=1):
            gr.Markdown("### Appearance Theme")
            theme_info = gr.Markdown(
                "🔒 **Locked Theme:** Premium Light Mode is active (Dark Mode disabled for clean design consistency)."
            )
            
            gr.Markdown("### Model Configuration")
            model_box = gr.Textbox(
                label="Active LLM Model", 
                value="llama-3.1-8b-instant (via Groq API client)", 
                interactive=False
            )
            
            gr.Markdown("### User Profile")
            user_id_display = gr.Textbox(label="Student Session ID", value="student_user_01", interactive=False)
            
            gr.Markdown("### Reset Settings")
            reset_btn = gr.Button("🗑️ Clear Cache & Reset State", variant="stop")
            
    return layout, reset_btn

def build_about_view():
    with gr.Column(elem_classes=["page-container"]) as layout:
        gr.HTML("""
            <div style='margin-bottom: 24px;'>
                <h1 style='font-size: 24px; font-weight: 800; color: #111827; margin: 0;'>ℹ️ About Nexora AI</h1>
                <p style='color: #4b5563; font-size: 14px; margin-top: 4px;'>Learn more about the application.</p>
            </div>
        """)
        
        gr.Markdown(
            """
            Nexora AI is a comprehensive career readiness platform designed to elevate college students' preparation processes.
            
            ### Core Technology Stack
            - **Frontend:** Gradio 6.x Blocks, Custom HTML5/CSS3 Light-Theme Styles system, Vanilla Javascript
            - **Large Language Model:** Llama 3.1 8B via Groq API (High Performance Cloud Inference)
            - **Persistence Layer:** Supabase Client (Remote PostgreSQL Backend)
            - **Helpers:** PyPDF (local resume parsing), Plotly (analytics visualizations), Pandas (structured frames)
            
            ### Platform Version
            - **Release version:** v1.1.0-light-release (June 2026)
            """
        )
    return layout

def mount_feature_views(
    active_chat_id: gr.State, 
    all_chats_data: gr.State, 
    chat_titles: gr.State,
    user_id_state: gr.State,
    history_buttons: list
):
    """Mount all views and return references for nav wiring."""
    views = {}
    cards = {}
    
    # 1. Home (visible by default)
    home_layout, card_chat, card_res, card_int, card_car = build_home_view()
    views["home"] = home_layout
    cards["chat"] = card_chat
    cards["resume"] = card_res
    cards["interview"] = card_int
    cards["career"] = card_car
    
    # 2. Dashboard (invisible by default)
    dash_layout = dashboard_interface()
    dash_layout.visible = False
    views["dashboard"] = dash_layout
    
    # 3. Chat Assistant (invisible by default)
    chat_layout, chatbot_ref = chatbot_interface(
        active_chat_id=active_chat_id,
        all_chats_data=all_chats_data,
        chat_titles=chat_titles,
        user_id_state=user_id_state,
        history_buttons=history_buttons
    )
    chat_layout.visible = False
    views["chat"] = chat_layout
    
    # 4. Resume Analyzer (invisible by default)
    resume_layout = resume_analyzer_interface()
    resume_layout.visible = False
    views["resume"] = resume_layout
    
    # 5. Interview Simulator (invisible by default)
    interview_layout = interview_simulator_interface()
    interview_layout.visible = False
    views["interview"] = interview_layout
    
    # 6. Career Planner (invisible by default)
    career_layout = career_planner_interface()
    career_layout.visible = False
    views["career"] = career_layout
    
    # 7. Analytics (invisible by default)
    analytics_layout = analytics_interface()
    analytics_layout.visible = False
    views["analytics"] = analytics_layout
    
    # 8. Settings (invisible by default)
    settings_layout, reset_btn = build_settings_view()
    settings_layout.visible = False
    views["settings"] = settings_layout
    
    # 9. About (invisible by default)
    about_layout = build_about_view()
    about_layout.visible = False
    views["about"] = about_layout
    
    return views, cards, chatbot_ref, reset_btn
