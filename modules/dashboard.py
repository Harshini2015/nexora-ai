import gradio as gr
import pandas as pd
import plotly.express as px
from database.supabase_client import get_user_stats
from modules.session_utils import get_or_create_user_id

def make_metric_card(label: str, value: str, emoji: str, color: str) -> str:
    """Generate HTML for metric card."""
    return f"""
    <div style="background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 20px; 
                box-shadow: 0 1px 3px rgba(0,0,0,0.05); position: relative; overflow: hidden; 
                display: flex; flex-direction: column; gap: 4px; transition: all 0.2s ease;">
        <div style="position: absolute; left: 0; top: 0; bottom: 0; width: 4px; background: {color};"></div>
        <div style="font-size: 11px; text-transform: uppercase; color: #4b5563; font-weight: 700; letter-spacing: 0.5px;">
            {emoji} {label}
        </div>
        <div style="font-size: 32px; font-weight: 800; color: #111827; line-height: 1.2;">
            {value}
        </div>
    </div>
    """

def dashboard_interface():
    user_id_state = gr.State(None)
    
    with gr.Column(elem_classes=["page-container"]) as layout:
        # Dashboard header
        gr.HTML("""
            <div style='margin-bottom: 24px;'>
                <h1 style='font-size: 24px; font-weight: 800; color: #111827; margin: 0;'>📊 Performance Dashboard</h1>
                <p style='color: #4b5563; font-size: 14px; margin-top: 4px;'>Real-time stats, AI feedback scores, and preparation logs.</p>
            </div>
        """)

        refresh_btn = gr.Button("🔄 Refresh Dashboard Data", variant="primary")
        
        # Metric Grid Row
        with gr.Row():
            chats_card = gr.HTML(make_metric_card("Total Chats", "0", "💬", "#4f46e5"))
            resumes_card = gr.HTML(make_metric_card("Resumes Analyzed", "0", "📄", "#0d9488"))
            interviews_card = gr.HTML(make_metric_card("Interviews Completed", "0", "🎤", "#3b82f6"))
            avg_score_card = gr.HTML(make_metric_card("Average Score", "0.0", "🎯", "#10b981"))

        with gr.Row():
            with gr.Column(scale=1):
                plot_area = gr.Plot(label="Activity Distribution")
            with gr.Column(scale=1):
                gr.HTML("<h3 style='margin:16px 0 8px 0; font-size: 16px; font-weight: 700; color: #111827;'>Recent Activity Logs</h3>")
                data_table = gr.DataFrame(
                    label="Logs", 
                    interactive=False, 
                    wrap=True,
                    datatype=["str", "str", "number"]
                )

        def update_dashboard(user_id_state_val):
            user_id = get_or_create_user_id(user_id_state_val)
            stats = get_user_stats(user_id)

            # Generate beautiful Plotly graph
            activities = ["Chats", "Resumes", "Interviews"]
            counts = [stats["chats"], stats["resumes"], stats["interviews"]]
            df = pd.DataFrame({
                "Activity": activities,
                "Count": counts
            })
            
            fig = px.bar(
                df, 
                x="Activity", 
                y="Count", 
                color="Activity",
                color_discrete_sequence=["#4f46e5", "#0d9488", "#3b82f6"],
                title="Activity Overview"
            )
            
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis_title="",
                yaxis_title="Count",
                margin=dict(l=40, r=20, t=40, b=40)
            )
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e5e7eb')

            # Dynamic metric updates
            chats_html = make_metric_card("Total Chats", str(stats["chats"]), "💬", "#4f46e5")
            resumes_html = make_metric_card("Resumes Analyzed", str(stats["resumes"]), "📄", "#0d9488")
            interviews_html = make_metric_card("Interviews Completed", str(stats["interviews"]), "🎤", "#3b82f6")
            
            avg_val = f"{stats['avg_score']:.1f}" if stats["avg_score"] > 0 else "0.0"
            avg_score_html = make_metric_card("Average Score", avg_val, "🎯", "#10b981")

            # Logs representation table
            logs_df = pd.DataFrame([
                {"Activity": "AI Coaching Chats", "Detail": "Conversation session", "Hits": stats["chats"]},
                {"Activity": "ATS Resume Analysis", "Detail": "Resume uploads", "Hits": stats["resumes"]},
                {"Activity": "Mock Interview Simulation", "Detail": "Mock interviews completed", "Hits": stats["interviews"]}
            ])

            return (
                chats_html, 
                resumes_html, 
                interviews_html, 
                avg_score_html, 
                fig,
                logs_df
            )

        refresh_btn.click(
            update_dashboard, 
            inputs=[user_id_state], 
            outputs=[chats_card, resumes_card, interviews_card, avg_score_card, plot_area, data_table]
        )
        
    return layout
