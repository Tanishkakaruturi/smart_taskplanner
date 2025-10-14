# Smart Task Planner - AI-Powered Goal Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5--turbo-purple.svg)

**Transform goals into actionable, time-bound task plans with AI-powered intelligence**

</div>

## Overview

Smart Task Planner is an intelligent web application that leverages AI reasoning to break down complex goals into manageable, dependency-aware tasks with realistic timelines. Whether you're learning new skills, launching projects, or planning business initiatives, our system generates personalized action plans that adapt to your timeframe and goal complexity.

### Business Problem Solved

Traditional goal planning suffers from:
- **Planning paralysis** - Not knowing where to start
- **Unrealistic timelines** - Poor time estimation
- **Missing dependencies** - Overlooking task relationships
- **Lack of structure** - No clear progression path

**Our Solution**: AI-generated task breakdowns with intelligent time estimation, dependency mapping, and domain-specific insights.

## Features

## Intelligent AI Core
- **Domain-Aware Task Generation**: Specialized templates for sports, languages, business, and general goals
- **Smart Time Estimation**: Realistic hour calculations based on timeframe and complexity
- **Dependency Mapping**: Automatic task sequencing with proper prerequisite relationships
- **Adaptive Deadlines**: Intelligent deadline distribution across short and long timeframes

### Enhanced User Experience
- **Modern Responsive UI**: Clean interface that works seamlessly across all devices
- **Real-time Progress Tracking**: Live completion metrics and visual progress indicators
- **Interactive Task Management**: Mark tasks complete/reopen with progress persistence
- **Resource Recommendations**: AI-curated tools and resources based on goal type

### Enterprise-Grade Architecture
- **RESTful API Design**: Well-documented, versioned endpoints with proper HTTP status codes
- **SQLite Database**: Persistent storage with relational integrity for goals and tasks
- **CORS Configuration**: Secure cross-origin resource sharing for frontend-backend communication
- **Comprehensive Error Handling**: Graceful error recovery with meaningful user feedback

### Prerequisites
- Python 3.8 or higher
- Modern web browser
- OpenAI API key for enhanced AI capabilities
Installation & Setup
Clone the Repository

bash
git clone https://github.com/yourusername/smart-task-planner.git
cd smart-task-planner
Set Up Virtual Environment

bash
# Create virtual environment
python -m venv venv

# Activate environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Install Dependencies

bash
pip install -r requirements.txt
Configure Environment

bash
# Create .env file
echo "OPENAI_API_KEY=your-api-key-here" > .env
Launch Application

bash
# Terminal 1 - Start Backend Server (Port 5500)
python main.py

# Terminal 2 - Start Frontend Server (Port 3000)
python serve_frontend.py
Access Application

Web Interface: http://localhost:3000
API Documentation: http://localhost:5500/docs
API Base URL: http://localhost:5500
