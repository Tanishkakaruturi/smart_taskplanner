from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from typing import List, Optional

# Import AI service
from ai_service import ai_service

# Database setup
def get_db():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_text TEXT NOT NULL,
            timeframe TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            estimated_hours INTEGER,
            deadline TIMESTAMP,
            dependencies TEXT,
            status TEXT DEFAULT 'pending',
            priority TEXT DEFAULT 'medium',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (goal_id) REFERENCES goals (id)
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

app = FastAPI(
    title="Smart Task Planner",
    description="AI-powered task breakdown with LLM reasoning",
    version="3.0.0"
)

# CORS middleware - UPDATED TO ALLOW PORT 3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GoalRequest(BaseModel):
    goal: str
    timeframe: Optional[str] = None

class TaskResponse(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    estimated_hours: float  # ✅ CHANGED FROM int TO float
    deadline: str
    dependencies: str
    priority: str
    status: Optional[str] = "pending"
    
class GoalResponse(BaseModel):
    id: int
    goal: str
    timeframe: Optional[str]
    total_tasks: int
    estimated_total_hours: float  # ✅ CHANGED FROM int TO float
    tasks: List[TaskResponse]
    created_at: str
    ai_generated: bool

@app.post("/breakdown-goal", response_model=GoalResponse)
def break_down_goal(request: GoalRequest):
    """Break down a goal into tasks using AI reasoning"""
    try:
        print(f"Processing goal: {request.goal}")
        
        # Generate tasks using AI service
        tasks_data = ai_service.generate_tasks(request.goal, request.timeframe)
        
        # Add missing fields for validation
        for i, task in enumerate(tasks_data, 1):
            task["id"] = i
            task["status"] = "pending"
        
        # Save to database
        conn = get_db()
        cursor = conn.cursor()
        
        # Save goal
        cursor.execute(
            "INSERT INTO goals (goal_text, timeframe) VALUES (?, ?)",
            (request.goal, request.timeframe)
        )
        goal_id = cursor.lastrowid
        
        # Save tasks - convert to int for database storage
        for task in tasks_data:
            cursor.execute('''
                INSERT INTO tasks (goal_id, title, description, estimated_hours, deadline, dependencies, priority)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (goal_id, task["title"], task["description"], int(task["estimated_hours"]),  # ✅ Convert to int for DB
                  task["deadline"], task["dependencies"], task["priority"]))
        
        conn.commit()
        conn.close()
        
        # Prepare response
        response = GoalResponse(
            id=goal_id,
            goal=request.goal,
            timeframe=request.timeframe,
            total_tasks=len(tasks_data),
            estimated_total_hours=sum(task["estimated_hours"] for task in tasks_data),
            tasks=[TaskResponse(**task) for task in tasks_data],
            created_at=datetime.now().isoformat(),
            ai_generated=True
        )
        
        print(f"Success! Created goal {goal_id} with {len(tasks_data)} AI-generated tasks")
        return response
        
    except Exception as e:
        print(f"Error in break_down_goal: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process goal: {str(e)}")

@app.get("/goals", response_model=List[GoalResponse])
def get_all_goals():
    """Get all saved goals with their tasks"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        goals = cursor.execute("SELECT * FROM goals ORDER BY created_at DESC").fetchall()
        
        result = []
        for goal in goals:
            tasks = cursor.execute(
                "SELECT * FROM tasks WHERE goal_id = ? ORDER BY id", 
                (goal["id"],)
            ).fetchall()
            
            # Convert database tasks to response format
            task_list = []
            for task in tasks:
                task_dict = dict(task)
                task_dict["estimated_hours"] = float(task_dict["estimated_hours"])  # ✅ Convert to float for response
                task_list.append(TaskResponse(**task_dict))
            
            goal_data = GoalResponse(
                id=goal["id"],
                goal=goal["goal_text"],
                timeframe=goal["timeframe"],
                total_tasks=len(tasks),
                estimated_total_hours=sum(float(task["estimated_hours"]) for task in tasks),  # ✅ Convert to float
                tasks=task_list,
                created_at=goal["created_at"],
                ai_generated=True
            )
            result.append(goal_data)
        
        conn.close()
        return result
    except Exception as e:
        print(f"Error in get_all_goals: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/goals/{goal_id}", response_model=GoalResponse)
def get_goal(goal_id: int):
    """Get a specific goal by ID"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        goal = cursor.execute("SELECT * FROM goals WHERE id = ?", (goal_id,)).fetchone()
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        
        tasks = cursor.execute(
            "SELECT * FROM tasks WHERE goal_id = ? ORDER BY id", 
            (goal_id,)
        ).fetchall()
        
        # Convert database tasks to response format
        task_list = []
        for task in tasks:
            task_dict = dict(task)
            task_dict["estimated_hours"] = float(task_dict["estimated_hours"])  # ✅ Convert to float for response
            task_list.append(TaskResponse(**task_dict))
        
        goal_data = GoalResponse(
            id=goal["id"],
            goal=goal["goal_text"],
            timeframe=goal["timeframe"],
            total_tasks=len(tasks),
            estimated_total_hours=sum(float(task["estimated_hours"]) for task in tasks),  # ✅ Convert to float
            tasks=task_list,
            created_at=goal["created_at"],
            ai_generated=True
        )
        
        conn.close()
        return goal_data
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_goal: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/tasks/{task_id}/complete")
def complete_task(task_id: int):
    """Mark task as completed"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if task exists
    task = cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update task status
    cursor.execute(
        "UPDATE tasks SET status = 'completed', completed_at = CURRENT_TIMESTAMP WHERE id = ?",
        (task_id,)
    )
    conn.commit()
    
    # Get updated task count for the goal
    goal_stats = cursor.execute('''
        SELECT 
            COUNT(*) as total_tasks,
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_tasks
        FROM tasks 
        WHERE goal_id = ?
    ''', (task["goal_id"],)).fetchone()
    
    conn.close()
    
    return {
        "status": "success", 
        "message": f"Task {task_id} completed",
        "goal_progress": {
            "completed_tasks": goal_stats["completed_tasks"],
            "total_tasks": goal_stats["total_tasks"],
            "completion_percentage": round((goal_stats["completed_tasks"] / goal_stats["total_tasks"]) * 100, 1)
        }
    }

@app.put("/tasks/{task_id}/reopen")
def reopen_task(task_id: int):
    """Reopen a completed task"""
    conn = get_db()
    cursor = conn.cursor()
    
    task = cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    cursor.execute(
        "UPDATE tasks SET status = 'pending', completed_at = NULL WHERE id = ?",
        (task_id,)
    )
    conn.commit()
    conn.close()
    
    return {"status": "success", "message": f"Task {task_id} reopened"}

@app.get("/")
def home():
    return {
        "message": "Smart Task Planner with AI",
        "version": "3.0.0",
        "features": [
            "LLM-powered task generation",
            "Database storage", 
            "REST API",
            "Task dependencies & timelines",
            "Task completion tracking"
        ],
        "status": "running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=5500)
