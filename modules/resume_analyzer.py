import gradio as gr
import pypdf
import re
import os
from modules.gemini_utils import get_gemini_response
from database.supabase_client import save_resume_report

def extract_text_from_pdf(file_path):
    try:
        reader = pypdf.PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error: {str(e)}"

from modules.session_utils import get_or_create_user_id

def resume_analyzer_interface():
    user_id_state = gr.State(None)
    
    with gr.Column() as layout:
        gr.Markdown("Resume Analyzer")
        gr.Markdown("Upload your resume in PDF format to get an ATS score and improvement tips.")

        
        with gr.Row():
            file_input = gr.File(label="Upload Resume (PDF)", file_types=[".pdf"])
            analyze_btn = gr.Button("Analyze Resume", variant="primary")
            
        output_report = gr.Markdown(label="Analysis Report")
        
        def analyze(file, user_id_state_val):
            user_id = get_or_create_user_id(user_id_state_val)
            if file is None:
                return "Please upload a PDF file.", user_id
            
            text = extract_text_from_pdf(file.name)
            if text.startswith("Error"):
                return text, user_id
            
            prompt = f"""
            Analyze the following resume text as an expert HR recruiter and ATS system.
            Provide a detailed report in the following format:
            1. ATS Score: [A number between 0-100]
            2. Strengths: [Bullet points]
            3. Weaknesses: [Bullet points]
            4. Actionable Suggestions: [Bullet points]
            
            Resume Text:
            {text}
            """
            
            report = get_gemini_response(prompt)
            
            # Extract score for database (simple regex)
            score_match = re.search(r"ATS Score:\s*(\d+)", report)
            score = int(score_match.group(1)) if score_match else 70
            
            # Save to database
            save_resume_report(user_id, os.path.basename(file.name), report, score)
            
            return report, user_id

        analyze_btn.click(analyze, inputs=[file_input, user_id_state], outputs=[output_report, user_id_state])

    
    return layout
