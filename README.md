# 🚀 Smart Task Planner - AI Powered

**Live Demo:** [https://smart-task-planner.onrender.com](https://smart-task-planner.onrender.com)

## 🤖 About
AI-powered task management system that breaks down complex goals into actionable tasks using OpenAI GPT-3.5 Turbo.

## ✨ Features
- **Real AI Integration** - OpenAI GPT-3.5 Turbo for intelligent task decomposition
- **Smart Task Generation** - Creates sequential tasks with dependencies and deadlines
- **Production Ready** - Deployed on Render.com with proper CORS and error handling
- **Modern UI** - Responsive design with real-time progress tracking

## 🛠️ Tech Stack
- **Backend:** FastAPI, Python, SQLite
- **AI:** OpenAI GPT-3.5 Turbo
- **Frontend:** HTML5, CSS3, JavaScript
- **Deployment:** Render.com
- **Database:** SQLite

## 🚀 Quick Start

### Local Development
```bash
# 1. Clone repository
git clone https://github.com/yourusername/smart-task-planner.git
cd smart-task-planner

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

# 4. Run application
uvicorn main:app --reload --port 5500
