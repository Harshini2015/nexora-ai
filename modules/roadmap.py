import gradio as gr
from modules.gemini_utils import get_gemini_response

def roadmap_interface():
    with gr.Column(visible=False, elem_classes="glass-card") as layout:
        gr.HTML("""
            <div style='margin-bottom: 24px;'>
                <h3 style='margin: 0; font-size: 20px; font-weight: 700;'>🗺️ Career Roadmap</h3>
                <p style='margin: 0; font-size: 14px; color: #9ca3af;'>Generate a personalized learning path to achieve your career goals.</p>
            </div>
        """)
        
        with gr.Row():
            skill = gr.Textbox(
                label="What do you want to learn?", 
                placeholder="e.g. Full Stack Web Development",
                elem_id="skill-input"
            )
            create_btn = gr.Button("🚀 Generate Path", elem_classes="primary-btn")
        
        with gr.Row():
            roadmap_output = gr.Markdown(label="Your Personalized Path", elem_id="roadmap-output")

        def create_roadmap(skill_name):
            if not skill_name:
                return "Please enter a skill or career goal first."
            prompt = f"Create a detailed 4-week learning roadmap for {skill_name}, including resources and key milestones."
            return get_gemini_response(prompt)

        create_btn.click(create_roadmap, inputs=[skill], outputs=[roadmap_output])
    
    return layout
