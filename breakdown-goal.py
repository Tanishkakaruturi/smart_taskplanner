from http.server import BaseHTTPRequestHandler
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            goal = data.get('goal', '')
            timeframe = data.get('timeframe', '')
            
            # Import your AI service
            from ai_service import ai_service
            
            # Generate tasks
            tasks_data = ai_service.generate_tasks(goal, timeframe)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "goal": goal,
                "timeframe": timeframe,
                "total_tasks": len(tasks_data),
                "estimated_total_hours": sum(task["estimated_hours"] for task in tasks_data),
                "tasks": tasks_data
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {"error": str(e)}
            self.wfile.write(json.dumps(error_response).encode())
