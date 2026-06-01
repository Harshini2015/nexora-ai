import gradio as gr
import pandas as pd
import plotly.express as px

def dashboard_interface():
    with gr.Column(visible=False) as layout:
        gr.HTML("""
            <div style='margin-bottom: 32px;'>
                <h2 style='margin: 0; font-size: 28px; font-weight: 800;'>📊 Performance Dashboard</h2>
                <p style='color: #9ca3af; font-size: 16px;'>Track your career growth and AI interactions.</p>
            </div>
        """)
        
        with gr.Row():
            with gr.Column(elem_classes="glass-card", scale=1):
                gr.HTML("""
                    <div style='text-align: center;'>
                        <div style='color: #8b5cf6; font-size: 32px; margin-bottom: 8px;'>💬</div>
                        <div style='font-size: 36px; font-weight: 800;'>128</div>
                        <div style='color: #9ca3af; font-size: 14px; font-weight: 500;'>TOTAL CHATS</div>
                        <div style='margin-top: 12px; color: #10b981; font-size: 12px;'>↑ 12% this week</div>
                    </div>
                """)
            with gr.Column(elem_classes="glass-card", scale=1):
                gr.HTML("""
                    <div style='text-align: center;'>
                        <div style='color: #10b981; font-size: 32px; margin-bottom: 8px;'>🎯</div>
                        <div style='font-size: 36px; font-weight: 800;'>85</div>
                        <div style='color: #9ca3af; font-size: 14px; font-weight: 500;'>RESUME SCORE</div>
                        <div style='margin-top: 12px; color: #10b981; font-size: 12px;'>Top 5% in niche</div>
                    </div>
                """)
            with gr.Column(elem_classes="glass-card", scale=1):
                gr.HTML("""
                    <div style='text-align: center;'>
                        <div style='color: #f59e0b; font-size: 32px; margin-bottom: 8px;'>🎤</div>
                        <div style='font-size: 36px; font-weight: 800;'>12</div>
                        <div style='color: #9ca3af; font-size: 14px; font-weight: 500;'>INTERVIEWS</div>
                        <div style='margin-top: 12px; color: #6366f1; font-size: 12px;'>Next one tomorrow</div>
                    </div>
                """)
            with gr.Column(elem_classes="glass-card", scale=1):
                gr.HTML("""
                    <div style='text-align: center;'>
                        <div style='color: #ec4899; font-size: 32px; margin-bottom: 8px;'>🚀</div>
                        <div style='font-size: 36px; font-weight: 800;'>92%</div>
                        <div style='color: #9ca3af; font-size: 14px; font-weight: 500;'>ACCURACY</div>
                        <div style='margin-top: 12px; color: #10b981; font-size: 12px;'>Highly optimized</div>
                    </div>
                """)

        with gr.Row():
            with gr.Column(elem_classes="glass-card", scale=2):
                gr.HTML("<h4 style='margin-top: 0; color: #8b5cf6;'>Activity Distribution</h4>")
                data = pd.DataFrame({
                    "Category": ["Chatbot", "Resume", "Interview", "Roadmap"],
                    "Usage": [45, 25, 15, 15]
                })
                fig = px.pie(data, values='Usage', names='Category', hole=0.4,
                            color_discrete_sequence=['#8b5cf6', '#6366f1', '#10b981', '#f59e0b'])
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#9ca3af',
                    showlegend=False,
                    margin=dict(t=0, b=0, l=0, r=0)
                )
                gr.Plot(fig)
            
            with gr.Column(elem_classes="glass-card", scale=3):
                gr.HTML("<h4 style='margin-top: 0; color: #8b5cf6;'>Recent Progress</h4>")
                recent_data = pd.DataFrame({
                    "Date": ["Jun 01", "May 31", "May 30", "May 29"],
                    "Activity": ["Mock Interview: SE", "Resume Update", "Chatbot: Skills", "Roadmap Gen"],
                    "Status": ["Completed", "Saved", "Completed", "Processing"]
                })
                gr.DataFrame(recent_data, interactive=False)
    
    return layout
