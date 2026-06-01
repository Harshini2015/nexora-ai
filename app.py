import gradio as gr

from modules.chatbot import chatbot_interface
from modules.career_planner import career_planner_interface
from modules.dashboard import dashboard_interface
from modules.interview_simulator import interview_simulator_interface
from modules.resume_analyzer import resume_analyzer_interface


def main():
    with gr.Blocks(title="Nexora AI") as demo:
        gr.HTML(
            """
            <div style="text-align: center; padding: 18px 12px; border-bottom: 1px solid #e5e7eb; margin-bottom: 18px;">
                <h1 style="margin: 0; font-size: 28px; color: #111827;">Nexora AI</h1>
                <p style="margin: 6px 0 0 0; font-size: 14px; color: #4b5563;">AI Career & Placement Assistant</p>
            </div>
            """
        )

        with gr.Tabs():
            with gr.Tab("Chatbot"):
                chatbot_interface()
            with gr.Tab("Resume Analyzer"):
                resume_analyzer_interface()
            with gr.Tab("Interview Simulator"):
                interview_simulator_interface()

            with gr.Tab("Career Planner"):
                career_planner_interface()

            with gr.Tab("Dashboard"):
                dashboard_interface()


        gr.HTML(
            """
            <div style="text-align: center; padding: 16px 12px; color: #9ca3af; font-size: 12px; border-top: 1px solid #e5e7eb; margin-top: 24px;">
                © 2026 Nexora AI • GDGoC BYOC Challenge
            </div>
            """
        )

    demo.launch(server_name="0.0.0.0", server_port=7860, theme=gr.themes.Default())


if __name__ == "__main__":
    main()

