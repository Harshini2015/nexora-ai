import gradio as gr

import socket

from modules.chatbot import chatbot_interface
from modules.career_planner import career_planner_interface
from modules.dashboard import dashboard_interface
from modules.interview_simulator import interview_simulator_interface
from modules.resume_analyzer import resume_analyzer_interface


def find_free_port(start_port: int = 7860, max_tries: int = 100) -> int:
    """Return the first free TCP port starting at start_port.

    Prevents WinError 10048 when the default Gradio port is already in use.
    """
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
                © 2026 Nexora AI
            </div>
            """
        )

    port = find_free_port(7860)
    print(f"[Nexora AI] Starting Gradio on port: {port}")
    # Use localhost for browser-accessible URL (0.0.0.0 is a bind address, not a browser URL)
    demo.launch(server_name="127.0.0.1", server_port=port, theme=gr.themes.Default())


if __name__ == "__main__":
    main()

