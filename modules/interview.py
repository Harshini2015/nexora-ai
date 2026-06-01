import gradio as gr
from modules.gemini_utils import get_gemini_response

def interview_interface():
    with gr.Column(visible=False, elem_classes="glass-card") as layout:
        gr.HTML("""
            <div style='margin-bottom: 24px;'>
                <h3 style='margin: 0; font-size: 20px; font-weight: 700;'>🎤 AI Mock Interview</h3>
                <p style='margin: 0; font-size: 14px; color: #9ca3af;'>Practice your interview skills with real-time AI feedback.</p>
            </div>
        """)
        
        with gr.Row():
            job_title = gr.Textbox(
                label="Target Job Role", 
                placeholder="e.g. Senior Software Engineer",
                elem_id="job-input"
            )
            generate_btn = gr.Button("🎬 Start Session", elem_classes="primary-btn")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.HTML("""
                    <div style='background: rgba(139, 92, 246, 0.05); padding: 16px; border-radius: 12px; border: 1px solid rgba(139, 92, 246, 0.2);'>
                        <h4 style='margin: 0 0 8px 0; font-size: 14px; color: #8b5cf6;'>Interview Tips:</h4>
                        <p style='margin: 0; font-size: 12px; color: #9ca3af;'>Use the STAR method for behavioral questions. Be specific about your technical contributions.</p>
                    </div>
                """)
            
            with gr.Column(scale=2):
                questions_output = gr.Markdown(label="Generated Questions", elem_id="interview-output")

        def generate_questions(title):
            if not title:
                return "Please enter a job title first."
            prompt = f"Generate 5 technical and behavioral interview questions for a {title} position."
            return get_gemini_response(prompt)

        generate_btn.click(generate_questions, inputs=[job_title], outputs=[questions_output])
    
    return layout
