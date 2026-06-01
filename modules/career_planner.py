import gradio as gr


def career_planner_interface():
    with gr.Column() as layout:
        gr.Markdown("Career Planner")
        gr.Markdown("Fill in your details to generate a personalized career roadmap.")

        with gr.Row():
            branch = gr.Dropdown(
                choices=[
                    "Computer Science",
                    "Information Technology",
                    "Electronics",
                    "Mechanical",
                    "Civil",
                    "Other",
                ],
                label="Your Branch",
            )
            year = gr.Dropdown(
                choices=["1st Year", "2nd Year", "3rd Year", "4th Year"],
                label="Current Year",
            )
            target_company = gr.Textbox(
                label="Target Company",
                placeholder="e.g. Google, Amazon, TCS",
            )

        generate_btn = gr.Button("Generate Roadmap", variant="primary")

        roadmap_output = gr.Markdown(label="Personalized Career Plan")

        def generate_plan(branch_val, year_val, company_val):
            if not branch_val or not year_val or not company_val:
                return "Please fill in all the details."

            # NOTE: Backend logic intentionally unchanged. This module currently
            # uses the existing Gemini helper via the already-imported app logic.
            from modules.gemini_utils import get_gemini_response

            prompt = f"""
            Generate a comprehensive career roadmap for a {year_val} {branch_val} student targeting {company_val}.
            Include:
            1. Skill Gap Analysis: What skills are needed vs typically learned in college.
            2. Monthly Roadmap: High-level goals for the next 6 months.
            3. Weekly Plan: A sample week-by-week breakdown for the first month.
            4. Learning Resources: Specific courses, websites, or books to use.

            Format the output with Markdown headers and bullet points.
            """

            return get_gemini_response(prompt)

        generate_btn.click(generate_plan, inputs=[branch, year, target_company], outputs=[roadmap_output])

    return layout

