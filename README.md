Smart Task Planner 🎯
A simple AI-powered web app that breaks down your goals into actionable tasks.

What It Does
Enter any goal (like "Learn tennis")

Get a step-by-step task plan with time estimates

Tasks have deadlines, dependencies, and priorities

Track your progress as you complete tasks

Quick Start
Install dependencies

bash
pip install -r requirements.txt
Run the app

bash
# Terminal 1 - Backend
python main.py

# Terminal 2 - Frontend  
python serve_frontend.py
Open your browser

Go to: http://localhost:3000

API docs: http://localhost:5500/docs

Files Overview
main.py - FastAPI backend server

ai_service.py - AI task generation logic

serve_frontend.py - Web interface server

frontend/index.html - Simple web UI

requirements.txt - Python packages needed

How to Use
Type your goal in the web page

Add optional timeframe (like "1 hour" or "2 weeks")

Click "Generate AI Task Plan"

Get your customized task breakdown!

Example
Goal: "Learn tennis in 1 hour"

AI Output:

Research basics & find local options (30 mins)

Practice basic swings (30 mins)

Perfect for students learning to break down projects and manage time! 🚀

