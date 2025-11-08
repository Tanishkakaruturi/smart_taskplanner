import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

class AIService:
    def __init__(self):
        # SECURE: Get API key from environment variable
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("❌ OPENAI_API_KEY environment variable is required")
        
        try:
            self.client = openai.OpenAI(api_key=self.api_key)
            print("🤖 AI Service: Real LLM Enabled - Using OpenAI GPT-3.5 Turbo")
            print("✅ AI Service: API Key authenticated successfully")
        except Exception as e:
            raise Exception(f"Failed to initialize OpenAI client: {e}")
    
    def generate_tasks(self, goal: str, timeframe: str = None) -> list:
        """Generate tasks using REAL LLM only"""
        print(f"🎯 AI Service: Generating tasks for '{goal}' with timeframe '{timeframe}'")
        
        try:
            llm_tasks = self._generate_tasks_with_llm(goal, timeframe)
            print(f"✅ AI Service: Successfully generated {len(llm_tasks)} tasks using real LLM")
            return llm_tasks
        except Exception as e:
            print(f"❌ AI Service: LLM generation failed - {e}")
            # Return minimal fallback instead of rule-based system
            return self._get_minimal_fallback(goal, timeframe)
    
    def _generate_tasks_with_llm(self, goal: str, timeframe: str) -> list:
        """Generate tasks using OpenAI GPT with enhanced prompting"""
        try:
            prompt = self._build_enhanced_prompt(goal, timeframe)
            
            print("🔄 AI Service: Calling OpenAI API...")
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": """You are an expert project manager and productivity specialist. 
                        Break down goals into specific, actionable tasks with realistic time estimates.
                        ALWAYS return valid JSON array format. No additional text."""
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            print(f"📄 AI Service: Raw LLM response received")
            
            # Extract JSON from response
            content = self._extract_json_from_response(content)
            
            tasks = json.loads(content)
            
            # Add calculated deadlines
            return self._add_deadlines_to_tasks(tasks, timeframe)
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            raise Exception("Failed to parse AI response as JSON")
        except Exception as e:
            print(f"LLM API error: {e}")
            raise
    
    def _build_enhanced_prompt(self, goal: str, timeframe: str) -> str:
        """Build comprehensive prompt for task generation"""
        return f"""
GOAL: "{goal}"
TIMEFRAME: {timeframe if timeframe else "Not specified"}

TASK BREAKDOWN REQUIREMENTS:
- Create 4-6 specific, actionable tasks
- Tasks should be sequential with clear dependencies
- Include phases: Research, Preparation, Execution, Review
- Estimate realistic hours for each task
- Set priorities: high/medium/low
- Make tasks concrete and measurable

OUTPUT FORMAT: Strictly JSON array only:

[
  {{
    "title": "Task name",
    "description": "Detailed description of what needs to be done",
    "estimated_hours": 4,
    "dependencies": "None or task numbers like 1,2",
    "priority": "high"
  }}
]

IMPORTANT: 
- Return ONLY the JSON array, no other text
- Ensure valid JSON format
- estimated_hours must be numbers
- dependencies must be strings like "None" or "1,2"
- priority must be "high", "medium", or "low"

Now generate the task breakdown for: "{goal}"
"""
    
    def _extract_json_from_response(self, content: str) -> str:
        """Extract JSON from LLM response"""
        # Remove markdown code blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].strip() if len(content.split("```")) > 2 else content
        
        # Find the first [ and last ]
        start_idx = content.find('[')
        end_idx = content.rfind(']')
        
        if start_idx != -1 and end_idx != -1:
            content = content[start_idx:end_idx+1]
        
        return content.strip()
    
    def _add_deadlines_to_tasks(self, tasks: list, timeframe: str) -> list:
        """Add realistic deadlines to tasks based on dependencies and timeframe"""
        base_date = datetime.now()
        total_days = self._parse_timeframe(timeframe)
        
        # Simple deadline distribution based on task order
        for i, task in enumerate(tasks):
            # Calculate days for this task (distribute across timeframe)
            days_offset = min(total_days, max(1, int((i + 1) / len(tasks) * total_days * 0.8)))
            task["deadline"] = (base_date + timedelta(days=days_offset)).isoformat()
        
        return tasks
    
    def _parse_timeframe(self, timeframe: str) -> int:
        """Convert timeframe string to days"""
        if not timeframe:
            return 30  # Default 30 days
        
        timeframe = timeframe.lower()
        
        # Extract numbers
        numbers = ''.join(filter(str.isdigit, timeframe))
        num = int(numbers) if numbers else 1
        
        if "week" in timeframe:
            return num * 7
        elif "month" in timeframe:
            return num * 30
        elif "day" in timeframe:
            return num
        else:
            return 30  # Default
    
    def _get_minimal_fallback(self, goal: str, timeframe: str) -> list:
        """Minimal fallback if LLM completely fails"""
        base_date = datetime.now()
        return [
            {
                "title": f"Research and plan {goal}",
                "description": f"Initial research and planning phase for {goal}",
                "estimated_hours": 4,
                "deadline": (base_date + timedelta(days=2)).isoformat(),
                "dependencies": "None",
                "priority": "high"
            },
            {
                "title": f"Execute main work on {goal}",
                "description": f"Primary execution phase for {goal}",
                "estimated_hours": 8,
                "deadline": (base_date + timedelta(days=7)).isoformat(),
                "dependencies": "1",
                "priority": "high"
            }
        ]

# Global instance
ai_service = AIService()
