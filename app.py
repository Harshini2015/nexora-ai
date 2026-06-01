import gradio as gr
from modules.chatbot import chatbot_interface
from modules.resume_analyzer import resume_analyzer_interface
from modules.interview_simulator import interview_simulator_interface
from modules.career_planner import career_planner_interface
from modules.dashboard import dashboard_interface

def main():
    with gr.Blocks(title="Nexora AI") as demo:
        gr.HTML("""
            <div style="text-align: center; padding: 20px; border-bottom: 1px solid #ddd; margin-bottom: 20px;">
                <h1 style="margin: 0; color: #2d3436; font-size: 2.5rem;">🚀 Nexora AI</h1>
                <p style="margin: 5px 0; color: #636e72; font-size: 1.1rem;">Your AI-Powered Career & Placement Assistant</p>
            </div>
        """)
        
        with gr.Tabs():
            with gr.Tab("💬 Chatbot"):
                chatbot_interface()
            
            with gr.Tab("📄 Resume Analyzer"):
                resume_analyzer_interface()
                
            with gr.Tab("🎤 Interview Simulator"):
                interview_simulator_interface()
                
            with gr.Tab("🎯 Career Planner"):
                career_planner_interface()
                
            with gr.Tab("📊 Dashboard"):
                dashboard_interface()

        gr.HTML("""
            <div style="text-align: center; padding: 20px; color: #b2bec3; font-size: 0.9rem; border-top: 1px solid #ddd; margin-top: 30px;">
                © 2026 Nexora AI • GDGoC BYOC Challenge
            </div>
        """)

    demo.launch(server_name="0.0.0.0", server_port=7860, theme=gr.themes.Default())

if __name__ == "__main__":
    main()
