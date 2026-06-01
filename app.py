import streamlit as st
from modules.chatbot import chatbot_page
from modules.resume_analyzer import resume_analyzer_page
from modules.interview import interview_page
from modules.roadmap import roadmap_page
from modules.dashboard import dashboard_page

def main():
    st.set_page_config(page_title="Nexora AI", layout="wide")
    
    st.sidebar.title("Nexora AI")
    page = st.sidebar.radio("Navigation", ["Dashboard", "Chatbot", "Resume Analyzer", "Interview Prep", "Roadmap"])
    
    if page == "Dashboard":
        dashboard_page()
    elif page == "Chatbot":
        chatbot_page()
    elif page == "Resume Analyzer":
        resume_analyzer_page()
    elif page == "Interview Prep":
        interview_page()
    elif page == "Roadmap":
        roadmap_page()

if __name__ == "__main__":
    main()
