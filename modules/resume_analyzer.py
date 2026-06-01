import gradio as gr
from modules.gemini_utils import get_gemini_response

def resume_analyzer_interface():
    with gr.Column(visible=False, elem_classes="glass-card") as layout:
        gr.HTML("""
            <div style='margin-bottom: 24px;'>
                <h3 style='margin: 0; font-size: 20px; font-weight: 700;'>📄 Resume Intelligence</h3>
                <p style='margin: 0; font-size: 14px; color: #9ca3af;'>Upload your resume for AI-powered analysis and scoring.</p>
            </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                file_input = gr.File(
                    label="Drop your resume here",
                    file_types=[".pdf"],
                    elem_id="resume-upload"
                )
                analyze_btn = gr.Button("🔍 Analyze Resume", elem_classes="primary-btn")
            
            with gr.Column(scale=1):
                gr.HTML("""
                    <div style='background: rgba(255,255,255,0.02); padding: 20px; border-radius: 16px; border: 1px dashed rgba(255,255,255,0.1); height: 100%;'>
                        <h4 style='margin: 0 0 12px 0; font-size: 16px; color: #8b5cf6;'>What we analyze:</h4>
                        <ul style='margin: 0; padding-left: 20px; color: #9ca3af; font-size: 13px; line-height: 1.8;'>
                            <li>Keywords & ATS compatibility</li>
                            <li>Skill gap analysis</li>
                            <li>Experience formatting</li>
                            <li>Quantifiable achievements</li>
                        </ul>
                    </div>
                """)
        
        output = gr.Markdown(label="Analysis Result", elem_id="resume-output")

        def analyze(file):
            if file is None:
                return "Please upload a resume first."
            prompt = "Analyze this resume and provide feedback on structure, keywords, and areas of improvement."
            response = get_gemini_response(prompt)
            return response

        analyze_btn.click(analyze, inputs=[file_input], outputs=[output])
    
    return layout
