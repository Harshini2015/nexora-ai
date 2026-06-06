import gradio as gr
from modules.chatbot import chatbot_interface
from modules.resume_analyzer import resume_analyzer_interface
from modules.interview_simulator import interview_simulator_interface
from modules.career_planner import career_planner_interface

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

def mount_feature_views(
    active_chat_id: gr.State, 
    all_chats_data: gr.State, 
    chat_titles: gr.State,
    user_id_state: gr.State
):
    """Mount all views and return references for nav wiring."""
    views = {}
    cards = {}
    
    # 1. Home (visible by default)
    with gr.Column(visible=True, elem_id="page-home") as home_col:
        _, card_chat, card_res, card_int, card_car = build_home_view()
    views["home"] = home_col
    cards["chat"] = card_chat
    cards["resume"] = card_res
    cards["interview"] = card_int
    cards["career"] = card_car
    
    # 2. Chat Assistant (visible in DOM, hidden via CSS initially)
    with gr.Column(visible=True, elem_id="page-chat") as chat_col:
        _, chatbot_ref = chatbot_interface(
            active_chat_id=active_chat_id,
            all_chats_data=all_chats_data,
            chat_titles=chat_titles,
            user_id_state=user_id_state
        )
    views["chat"] = chat_col
    
    # 3. Resume Analyzer (visible in DOM, hidden via CSS initially)
    with gr.Column(visible=True, elem_id="page-resume") as resume_col:
        resume_analyzer_interface()
    views["resume"] = resume_col
    
    # 4. Interview Simulator (visible in DOM, hidden via CSS initially)
    with gr.Column(visible=True, elem_id="page-interview") as interview_col:
        interview_simulator_interface()
    views["interview"] = interview_col
    
    # 5. Career Planner (visible in DOM, hidden via CSS initially)
    with gr.Column(visible=True, elem_id="page-career") as career_col:
        career_planner_interface()
    views["career"] = career_col
    
    # 6. Settings (visible in DOM, hidden via CSS initially)
    with gr.Column(visible=True, elem_id="page-settings") as settings_col:
        _, reset_btn = build_settings_view()
    views["settings"] = settings_col
    
    return views, cards, chatbot_ref, reset_btn
