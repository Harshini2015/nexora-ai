import gradio as gr
from modules.chatbot import chatbot_interface
from modules.resume_analyzer import resume_analyzer_interface
from modules.interview import interview_interface
from modules.roadmap import roadmap_interface
from modules.dashboard import dashboard_interface

# Advanced Premium SaaS CSS
css = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

:root {
    --primary: #8b5cf6;
    --primary-glow: rgba(139, 92, 246, 0.5);
    --secondary: #6366f1;
    --accent: #10b981;
    --bg-dark: #030712;
    --glass-bg: rgba(15, 23, 42, 0.6);
    --glass-border: rgba(255, 255, 255, 0.08);
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --sidebar-width: 280px;
}

body, .gradio-container { 
    background-color: var(--bg-dark) !important;
    background-image: 
        radial-gradient(circle at 0% 0%, rgba(139, 92, 246, 0.15) 0%, transparent 35%),
        radial-gradient(circle at 100% 100%, rgba(99, 102, 241, 0.15) 0%, transparent 35%) !important;
    color: var(--text-main) !important; 
    font-family: 'Plus Jakarta Sans', sans-serif !important; 
}

/* Glassmorphism Core */
.glass-card {
    background: var(--glass-bg) !important;
    backdrop-filter: blur(16px) saturate(180%) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 24px !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8) !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease !important;
}

/* Sidebar Styling */
.sidebar { 
    background: rgba(2, 6, 23, 0.8) !important; 
    backdrop-filter: blur(24px) !important;
    padding: 40px 24px !important; 
    height: 100vh !important; 
    border-right: 1px solid var(--glass-border) !important;
    position: sticky !important;
    top: 0 !important;
}

.nav-btn { 
    text-align: left !important; 
    width: 100% !important; 
    margin-bottom: 8px !important; 
    background: transparent !important; 
    border: 1px solid transparent !important; 
    color: var(--text-muted) !important; 
    padding: 14px 18px !important; 
    border-radius: 12px !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    font-size: 15px !important;
    font-weight: 500 !important;
}

.nav-btn:hover { 
    background: rgba(255, 255, 255, 0.05) !important; 
    color: white !important;
    transform: translateX(4px);
}

.nav-btn.active { 
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important; 
    color: white !important;
    box-shadow: 0 4px 20px var(--primary-glow) !important;
}

/* Hero Typography */
.hero-title {
    font-size: 3.5rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.04em !important;
    background: linear-gradient(to bottom right, #ffffff 30%, #94a3b8) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    margin-bottom: 12px !important;
}

.hero-subtitle {
    color: var(--text-muted) !important;
    font-size: 1.15rem !important;
    font-weight: 400 !important;
    max-width: 600px !important;
}

/* ChatGPT Style Chat */
#nexora-chatbot {
    background: transparent !important;
    border: none !important;
}

.message-user { 
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
    border-radius: 20px 20px 4px 20px !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
}

.message-bot { 
    background: rgba(30, 41, 59, 0.5) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 20px 20px 20px 4px !important;
}

/* Buttons */
.primary-btn {
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
    border: none !important;
    color: white !important;
    padding: 12px 24px !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 12px var(--primary-glow) !important;
}

.primary-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px var(--primary-glow) !important;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.main-content {
    animation: fadeIn 0.5s ease-out forwards;
    padding: 48px !important;
}

/* Custom Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }

footer { display: none !important; }
"""

def main():
    with gr.Blocks(css=css, title="Nexora AI") as demo:
        with gr.Row():
            # Sidebar Navigation
            with gr.Column(scale=1, elem_classes="sidebar"):
                gr.HTML("""
                    <div style='margin-bottom: 48px; padding-left: 8px;'>
                        <div style='display: flex; align-items: center; gap: 14px; margin-bottom: 6px;'>
                            <div style='background: linear-gradient(135deg, #8b5cf6, #6366f1); width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 20px rgba(139, 92, 246, 0.4);'>
                                <span style='font-size: 22px;'>⚡</span>
                            </div>
                            <h2 style='margin: 0; font-size: 26px; font-weight: 800; letter-spacing: -1px; color: white;'>Nexora <span style='color: #8b5cf6'>AI</span></h2>
                        </div>
                        <p style='color: #475569; font-size: 11px; font-weight: 700; letter-spacing: 1.5px; margin: 0; text-transform: uppercase;'>The Future of Careers</p>
                    </div>
                """)
                
                nav_dashboard = gr.Button("📊 Dashboard", elem_classes="nav-btn")
                nav_resume = gr.Button("📄 Resume Analyzer", elem_classes="nav-btn")
                nav_interview = gr.Button("🎤 Mock Interview", elem_classes="nav-btn")
                nav_career = gr.Button("🧠 Career Assistant", elem_classes="nav-btn active")
                nav_history = gr.Button("🕒 Chat History", elem_classes="nav-btn")
                
                gr.HTML("""
                    <div style='margin-top: auto; padding-top: 30px;'>
                        <div style='background: linear-gradient(180deg, rgba(255,255,255,0.05) 0%, transparent 100%); padding: 20px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);'>
                            <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 12px;'>
                                <div style='width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #8b5cf6, #6366f1); display: flex; align-items: center; justify-content: center; font-weight: 800; color: white; font-size: 16px;'>H</div>
                                <div>
                                    <div style='font-size: 15px; font-weight: 700; color: white;'>Harshini S</div>
                                    <div style='font-size: 12px; color: #64748b;'>Premium Member</div>
                                </div>
                            </div>
                            <div style='background: rgba(139, 92, 246, 0.1); padding: 8px 12px; border-radius: 10px; text-align: center; cursor: pointer;'>
                                <span style='font-size: 12px; color: #a78bfa; font-weight: 600;'>⭐ Upgrade Plan</span>
                            </div>
                        </div>
                    </div>
                """)
            
            # Main Content Area
            with gr.Column(scale=4, elem_classes="main-content"):
                # Global Hero Section
                with gr.Group(elem_classes="hero-section"):
                    gr.HTML("""
                        <div style='margin-bottom: 48px;'>
                            <h1 class='hero-title'>Nexora AI</h1>
                            <p class='hero-subtitle'>Your AI-Powered Career Copilot. Accelerate your career growth with intelligent insights and personalized guidance.</p>
                        </div>
                    """)
                
                # Page Containers
                with gr.Group():
                    dashboard_page = dashboard_interface()
                    resume_page = resume_analyzer_interface()
                    interview_page = interview_interface()
                    career_page = chatbot_interface()
                    roadmap_page = roadmap_interface() # Roadmap used for career assistant logic
                    
                    # Chat History Page
                    with gr.Column(visible=False, elem_classes="glass-card") as history_page:
                        gr.HTML("""
                            <div style='padding: 20px;'>
                                <h3 style='font-size: 24px; font-weight: 700; margin-bottom: 24px;'>🕒 Chat History</h3>
                                <div style='display: flex; flex-direction: column; gap: 16px;'>
                                    <div style='background: rgba(255,255,255,0.03); padding: 20px; border-radius: 16px; border: 1px solid var(--glass-border); display: flex; justify-content: space-between; align-items: center;'>
                                        <div>
                                            <div style='font-weight: 600; font-size: 16px;'>Career Path Discussion</div>
                                            <div style='font-size: 13px; color: #64748b;'>June 01, 2026 • 12 messages</div>
                                        </div>
                                        <div style='color: #8b5cf6; font-size: 18px; cursor: pointer;'>→</div>
                                    </div>
                                    <div style='background: rgba(255,255,255,0.03); padding: 20px; border-radius: 16px; border: 1px solid var(--glass-border); display: flex; justify-content: space-between; align-items: center;'>
                                        <div>
                                            <div style='font-weight: 600; font-size: 16px;'>Resume Feedback Session</div>
                                            <div style='font-size: 13px; color: #64748b;'>May 31, 2026 • 8 messages</div>
                                        </div>
                                        <div style='color: #8b5cf6; font-size: 18px; cursor: pointer;'>→</div>
                                    </div>
                                    <div style='background: rgba(255,255,255,0.03); padding: 20px; border-radius: 16px; border: 1px solid var(--glass-border); display: flex; justify-content: space-between; align-items: center;'>
                                        <div>
                                            <div style='font-weight: 600; font-size: 16px;'>Interview Preparation</div>
                                            <div style='font-size: 13px; color: #64748b;'>May 30, 2026 • 15 messages</div>
                                        </div>
                                        <div style='color: #8b5cf6; font-size: 18px; cursor: pointer;'>→</div>
                                    </div>
                                </div>
                            </div>
                        """)
                
                # Navigation Logic
                pages = [dashboard_page, resume_page, interview_page, career_page, history_page]
                nav_btns = [nav_dashboard, nav_resume, nav_interview, nav_career, nav_history]
                
                def navigate(page_idx):
                    return [gr.update(visible=(i == page_idx)) for i in range(len(pages))]

                # Set initial state
                career_page.visible = True
                dashboard_page.visible = False
                resume_page.visible = False
                interview_page.visible = False
                history_page.visible = False

                for i, btn in enumerate(nav_btns):
                    btn.click(fn=lambda i=i: navigate(i), outputs=pages)

        # Bottom Decoration
        gr.HTML("""
            <div style='text-align: center; padding: 40px; color: #475569; font-size: 13px;'>
                Built with ❤️ by Nexora Team • © 2026 Nexora AI
            </div>
        """)

    demo.launch(css=css)

if __name__ == "__main__":
    main()
