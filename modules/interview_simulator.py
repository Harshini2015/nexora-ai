import gradio as gr


from modules.gemini_utils import get_gemini_json
from database.supabase_client import save_interview_result


from modules.session_utils import get_or_create_user_id

def interview_simulator_interface():
    user_id_state = gr.State(None)
    
    with gr.Column() as layout:
        gr.Markdown("Interview Simulator")
        gr.Markdown("Practice your interview skills and get instant feedback and scoring.")

        
        with gr.Row():
            mode = gr.Radio(choices=["HR", "Technical", "DSA"], label="Interview Mode", value="Technical")
            job_role = gr.Textbox(label="Job Role", placeholder="e.g. Frontend Developer")
            
        generate_btn = gr.Button("Generate Mock Question", variant="primary")
        
        question_display = gr.Markdown(label="Question")
        user_answer = gr.Textbox(label="Your Answer", lines=5, placeholder="Type your answer here...")
        evaluate_btn = gr.Button("Evaluate Answer")
        
        feedback_display = gr.Markdown(label="Feedback & Score")

        def generate_question(mode_val, role_val):
            if not role_val:
                return "Please enter a job role."
            prompt = f"Act as an interviewer for a {role_val} position. Generate ONE challenging {mode_val} interview question."
            # Use regular response for question generation (not score parsing)
            return get_gemini_json(
                "Return ONLY valid JSON for a single string question.\nSchema: {\"question\": str}.\nDo not include any other text.\n"
                + prompt,
                schema={"question": str},
                retries=3,
                delay=2,
            )["question"]


        def evaluate_response(mode_val, role_val, question, answer, user_id_state_val):
            user_id = get_or_create_user_id(user_id_state_val)
            if not answer:
                return "Please provide an answer to evaluate.", user_id
            
            prompt = f"""
            As an expert interviewer, evaluate this candidate's answer.
            Question: {question}
            Answer: {answer}
            Mode: {mode_val}
            Role: {role_val}
            
            Provide:
            1. Score: [0-10]
            2. Feedback: [Detailed critique]
            3. Correct/Better Answer: [How it should have been answered]
            """
            
            json_prompt = (
                "Return ONLY valid JSON with this schema: "
                "{\"score\": int, \"feedback\": str, \"improvements\": [str]}. "
                "Do not include any other text.\n\n"
                f"Question: {question}\n"
                f"Answer: {answer}\n"
                f"Mode: {mode_val}\n"
                f"Role: {role_val}\n\n"
                "Evaluate as an expert interviewer."
            )

            payload = None
            try:
                payload = get_gemini_json(
                    json_prompt,
                    schema={"score": int, "feedback": str, "improvements": list},
                    retries=3,
                    delay=2,
                )
            except Exception:
                payload = {"score": 0, "feedback": "", "improvements": []}

            feedback = (
                f"Score: {payload['score']}\n\n"
                f"Feedback:\n{payload['feedback']}\n\n"
                f"Improvements:\n- " + "\n- ".join(payload["improvements"]) if payload["improvements"] else "Improvements: -"
            )

            # Save to database
            save_interview_result(user_id, mode_val, int(payload["score"]), feedback)

            return feedback, user_id


        generate_btn.click(generate_question, inputs=[mode, job_role], outputs=[question_display])
        evaluate_btn.click(evaluate_response, inputs=[mode, job_role, question_display, user_answer, user_id_state], outputs=[feedback_display, user_id_state])

    
    return layout
