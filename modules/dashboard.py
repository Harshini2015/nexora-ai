import gradio as gr
import pandas as pd
import plotly.express as px
from database.supabase_client import get_user_stats

def dashboard_interface():
    user_id_state = gr.State("student_user_01")
    
    with gr.Column() as layout:
        gr.Markdown("### 📊 Your Performance Dashboard")
        gr.Markdown("Overview of your activities and progress in Nexora AI.")
        
        refresh_btn = gr.Button("Refresh Data", size="sm")
        
        with gr.Row():
            chats_count = gr.Label(label="Total Chats")
            resumes_count = gr.Label(label="Resumes Analyzed")
            interviews_count = gr.Label(label="Interviews Completed")
            avg_score = gr.Label(label="Average Score")

        with gr.Row():
            plot_area = gr.Plot(label="Activity Distribution")
            data_table = gr.DataFrame(label="Activity Logs", interactive=False)

        def update_dashboard(user_id):
            stats = get_user_stats(user_id)
            
            # Prepare chart data
            df = pd.DataFrame({
                "Activity": ["Chats", "Resumes", "Interviews"],
                "Count": [stats["chats"], stats["resumes"], stats["interviews"]]
            })
            fig = px.bar(df, x="Activity", y="Count", title="Total Activity Overview", 
                         color="Activity", color_discrete_sequence=px.colors.qualitative.Pastel)
            
            return (
                stats["chats"], 
                stats["resumes"], 
                stats["interviews"], 
                f"{stats['avg_score']:.1f}", 
                fig,
                df
            )

        refresh_btn.click(
            update_dashboard, 
            inputs=[user_id_state], 
            outputs=[chats_count, resumes_count, interviews_count, avg_score, plot_area, data_table]
        )
        
        # Initial load logic moved to app.py or triggered by refresh
    
    return layout
