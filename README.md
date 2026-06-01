# Nexora AI 🚀

Your AI-Powered Career & Placement Assistant, built for students to ace their professional journey. Developed for the GDGoC BYOC Challenge.

## ✨ Features

- **💬 AI Chatbot**: Professional career coaching powered by Gemini Pro.
- **📄 Resume Analyzer**: Upload PDF resumes to get ATS scores and improvement tips.
- **🎤 Interview Simulator**: Practice HR, Technical, and DSA questions with instant feedback.
- **🎯 Career Planner**: Generate personalized roadmaps based on your branch, year, and goal company.
- **📊 Performance Dashboard**: Track your progress with visual analytics and activity logs.

## 🛠️ Tech Stack

- **Frontend**: Gradio (Light Mode, Tabs-based)
- **AI Core**: Gemini Pro API
- **Database**: Supabase (PostgreSQL)
- **Visualization**: Plotly & Pandas
- **File Processing**: PyPDF

## 🚀 Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd nexora-ai
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file based on `.env.example` and add your keys:
   ```env
   GEMINI_API_KEY=your_key
   SUPABASE_URL=your_url
   SUPABASE_KEY=your_key
   ```

4. **Database Setup**:
   Create the following tables in Supabase:
   - `chats`: (user_id, message, response)
   - `resumes`: (user_id, filename, report, score)
  - `interviews`: (user_id, mode, score, feedback)
  - `profiles`: (id uuid primary key, email text, created_at timestamp)

5. **Run the application**:
   ```bash
   python app.py
   ```

## 🏗️ Architecture

Nexora AI follows a modular architecture for reliability and scalability:
- `app.py`: Main entry point and layout definition.
- `modules/`: Feature-specific UI and logic components.
- `database/`: Supabase client and data persistence helper functions.
- `assets/`: Static resources and styles.


