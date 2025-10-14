import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key and self.api_key != "your-api-key-here":
            print("AI Service: OpenAI API ready")
        else:
            print("AI Service: No API key found, using enhanced rule-based tasks")
    
    def generate_tasks(self, goal: str, timeframe: str = None) -> list:
        """Generate tasks using enhanced rule-based system"""
        print(f"AI Service: Generating tasks for '{goal}' with timeframe '{timeframe}'")
        
        # Use enhanced rule-based tasks
        return self.get_enhanced_tasks(goal, timeframe)
    
    def get_enhanced_tasks(self, goal: str, timeframe: str) -> list:
        """Intelligent task breakdown with domain awareness"""
        goal_lower = goal.lower()
        
        # Domain-specific breakdowns
        if any(word in goal_lower for word in ["tennis", "sports", "fitness", "golf", "soccer"]):
            return self._create_sports_learning_tasks(goal, timeframe)
        elif any(word in goal_lower for word in ["language", "french", "spanish", "english"]):
            return self._create_language_learning_tasks(goal, timeframe)
        elif any(word in goal_lower for word in ["business", "startup", "company", "entrepreneur"]):
            return self._create_business_tasks(goal, timeframe)
        else:
            return self._create_universal_tasks(goal, timeframe)

    def _create_sports_learning_tasks(self, goal: str, timeframe: str) -> list:
        """Specialized tasks for sports learning with proper deadline distribution"""
        base_date = datetime.now()
        total_days = self._parse_timeframe(timeframe)
        
        # For very short timeframes (1-3 days), adjust task durations and deadlines
        if total_days <= 3:
            return [
                {
                    "title": "Research Basic Techniques & Local Options",
                    "description": f"Quick research on {goal} fundamentals and nearby facilities",
                    "estimated_hours": 2,
                    "deadline": (base_date + timedelta(hours=4)).isoformat(),
                    "dependencies": "None",
                    "priority": "high"
                },
                {
                    "title": "Get Starter Equipment",
                    "description": f"Acquire basic {goal} equipment for initial practice",
                    "estimated_hours": 3,
                    "deadline": (base_date + timedelta(hours=8)).isoformat(),
                    "dependencies": "1",
                    "priority": "high"
                },
                {
                    "title": "Learn Basic Fundamentals",
                    "description": f"Practice basic {goal} techniques and movements",
                    "estimated_hours": 4,
                    "deadline": (base_date + timedelta(hours=16)).isoformat(),
                    "dependencies": "2",
                    "priority": "high"
                },
                {
                    "title": "Practice Session",
                    "description": f"Dedicated practice time to reinforce {goal} skills",
                    "estimated_hours": 3,
                    "deadline": (base_date + timedelta(days=total_days)).isoformat(),
                    "dependencies": "3",
                    "priority": "high"
                }
            ]
        else:
            # Original logic for longer timeframes with improved deadline distribution
            return [
                {
                    "title": "Find Local Coach/Training Facilities",
                    "description": f"Research and contact local {goal} coaches, clubs, or training centers",
                    "estimated_hours": 3,
                    "deadline": (base_date + timedelta(days=min(2, total_days * 0.1))).isoformat(),
                    "dependencies": "None",
                    "priority": "high"
                },
                {
                    "title": "Acquire Proper Equipment & Gear",
                    "description": f"Research and purchase appropriate {goal} equipment, shoes, and clothing",
                    "estimated_hours": 2,
                    "deadline": (base_date + timedelta(days=min(4, total_days * 0.2))).isoformat(),
                    "dependencies": "1",
                    "priority": "high"
                },
                {
                    "title": "Learn Fundamentals & Basic Techniques",
                    "description": f"Master basic {goal} techniques through lessons and practice sessions",
                    "estimated_hours": max(8, total_days * 1),
                    "deadline": (base_date + timedelta(days=min(total_days * 0.5, total_days - 2))).isoformat(),
                    "dependencies": "1,2",
                    "priority": "high"
                },
                {
                    "title": "Practice & Skill Development",
                    "description": f"Regular practice sessions focusing on consistency and technique improvement",
                    "estimated_hours": max(12, total_days * 1.5),
                    "deadline": (base_date + timedelta(days=min(total_days * 0.8, total_days - 1))).isoformat(),
                    "dependencies": "3",
                    "priority": "high"
                },
                {
                    "title": "Advanced Techniques & Match Play",
                    "description": f"Learn advanced strategies and participate in practice matches",
                    "estimated_hours": max(6, total_days * 0.8),
                    "deadline": (base_date + timedelta(days=total_days)).isoformat(),
                    "dependencies": "4",
                    "priority": "medium"
                }
            ]

    def _create_language_learning_tasks(self, goal: str, timeframe: str) -> list:
        """Specialized tasks for language learning with improved deadlines"""
        base_date = datetime.now()
        total_days = self._parse_timeframe(timeframe)
        
        if total_days <= 3:
            return [
                {
                    "title": "Learn Essential Vocabulary",
                    "description": f"Master basic {goal} words and common phrases",
                    "estimated_hours": 3,
                    "deadline": (base_date + timedelta(hours=6)).isoformat(),
                    "dependencies": "None",
                    "priority": "high"
                },
                {
                    "title": "Practice Basic Conversations",
                    "description": f"Practice simple {goal} dialogues and greetings",
                    "estimated_hours": 4,
                    "deadline": (base_date + timedelta(hours=12)).isoformat(),
                    "dependencies": "1",
                    "priority": "high"
                },
                {
                    "title": "Listening Comprehension",
                    "description": f"Practice understanding basic {goal} speech",
                    "estimated_hours": 3,
                    "deadline": (base_date + timedelta(days=total_days)).isoformat(),
                    "dependencies": "2",
                    "priority": "medium"
                }
            ]
        else:
            return [
                {
                    "title": "Learn Basic Vocabulary & Phrases",
                    "description": f"Master essential {goal} vocabulary, greetings, and common phrases",
                    "estimated_hours": 8,
                    "deadline": (base_date + timedelta(days=min(7, total_days * 0.2))).isoformat(),
                    "dependencies": "None",
                    "priority": "high"
                },
                {
                    "title": "Practice Grammar & Sentence Structure",
                    "description": f"Study {goal} grammar rules and practice constructing sentences",
                    "estimated_hours": 10,
                    "deadline": (base_date + timedelta(days=min(14, total_days * 0.4))).isoformat(),
                    "dependencies": "1",
                    "priority": "high"
                },
                {
                    "title": "Listening & Comprehension Practice",
                    "description": f"Practice understanding {goal} through audio materials and conversations",
                    "estimated_hours": max(5, total_days * 0.8),
                    "deadline": (base_date + timedelta(days=min(total_days * 0.6, total_days - 3))).isoformat(),
                    "dependencies": "2",
                    "priority": "medium"
                },
                {
                    "title": "Speaking Practice & Conversation",
                    "description": f"Practice speaking {goal} with partners or through language apps",
                    "estimated_hours": max(8, total_days * 1.2),
                    "deadline": (base_date + timedelta(days=min(total_days * 0.8, total_days - 1))).isoformat(),
                    "dependencies": "3",
                    "priority": "high"
                },
                {
                    "title": "Cultural Immersion & Advanced Practice",
                    "description": f"Immerse in {goal} culture and practice advanced conversations",
                    "estimated_hours": max(4, total_days * 0.6),
                    "deadline": (base_date + timedelta(days=total_days)).isoformat(),
                    "dependencies": "4",
                    "priority": "medium"
                }
            ]

    def _create_business_tasks(self, goal: str, timeframe: str) -> list:
        """Specialized tasks for business goals with improved deadlines"""
        base_date = datetime.now()
        total_days = self._parse_timeframe(timeframe)
        
        if total_days <= 3:
            return [
                {
                    "title": "Quick Market Research",
                    "description": f"Basic research on {goal} market and competition",
                    "estimated_hours": 4,
                    "deadline": (base_date + timedelta(hours=8)).isoformat(),
                    "dependencies": "None",
                    "priority": "high"
                },
                {
                    "title": "Create Basic Business Outline",
                    "description": f"Develop simple business plan for {goal}",
                    "estimated_hours": 6,
                    "deadline": (base_date + timedelta(days=total_days)).isoformat(),
                    "dependencies": "1",
                    "priority": "high"
                }
            ]
        else:
            return [
                {
                    "title": "Market Research & Analysis",
                    "description": f"Research target market, competition, and customer needs for {goal}",
                    "estimated_hours": 12,
                    "deadline": (base_date + timedelta(days=min(5, total_days * 0.15))).isoformat(),
                    "dependencies": "None",
                    "priority": "high"
                },
                {
                    "title": "Business Plan Development",
                    "description": f"Create detailed business plan including financial projections for {goal}",
                    "estimated_hours": 15,
                    "deadline": (base_date + timedelta(days=min(10, total_days * 0.3))).isoformat(),
                    "dependencies": "1",
                    "priority": "high"
                },
                {
                    "title": "Legal Structure & Registration",
                    "description": f"Establish legal entity and complete necessary registrations for {goal}",
                    "estimated_hours": 8,
                    "deadline": (base_date + timedelta(days=min(15, total_days * 0.45))).isoformat(),
                    "dependencies": "2",
                    "priority": "medium"
                },
                {
                    "title": "Product/Service Development",
                    "description": f"Develop the core product or service for {goal}",
                    "estimated_hours": max(20, total_days * 2),
                    "deadline": (base_date + timedelta(days=min(total_days * 0.8, total_days - 3))).isoformat(),
                    "dependencies": "3",
                    "priority": "high"
                },
                {
                    "title": "Marketing & Launch Preparation",
                    "description": f"Prepare marketing materials and launch strategy for {goal}",
                    "estimated_hours": 10,
                    "deadline": (base_date + timedelta(days=total_days)).isoformat(),
                    "dependencies": "4",
                    "priority": "high"
                }
            ]

    def _create_universal_tasks(self, goal: str, timeframe: str) -> list:
        """Universal task breakdown for any goal with improved deadlines"""
        base_date = datetime.now()
        total_days = self._parse_timeframe(timeframe)
        
        if total_days <= 2:
            return [
                {
                    "title": f"Quick Research on {goal}",
                    "description": f"Basic research and planning for {goal}",
                    "estimated_hours": 2,
                    "deadline": (base_date + timedelta(hours=4)).isoformat(),
                    "dependencies": "None",
                    "priority": "high"
                },
                {
                    "title": f"Start Working on {goal}",
                    "description": f"Begin hands-on work for {goal}",
                    "estimated_hours": 6,
                    "deadline": (base_date + timedelta(days=total_days)).isoformat(),
                    "dependencies": "1",
                    "priority": "high"
                }
            ]
        else:
            return [
                {
                    "title": f"Research and Plan {goal}",
                    "description": f"Research the best approach and create a detailed plan for {goal}",
                    "estimated_hours": 4,
                    "deadline": (base_date + timedelta(days=min(2, total_days * 0.1))).isoformat(),
                    "dependencies": "None",
                    "priority": "high"
                },
                {
                    "title": f"Gather Resources for {goal}",
                    "description": f"Collect all necessary materials, tools, or information for {goal}",
                    "estimated_hours": 3,
                    "deadline": (base_date + timedelta(days=min(4, total_days * 0.2))).isoformat(),
                    "dependencies": "1",
                    "priority": "high"
                },
                {
                    "title": f"Begin Active Work on {goal}",
                    "description": f"Start hands-on implementation and practice for {goal}",
                    "estimated_hours": max(10, total_days * 1.5),
                    "deadline": (base_date + timedelta(days=min(total_days * 0.7, total_days - 2))).isoformat(),
                    "dependencies": "2",
                    "priority": "high"
                },
                {
                    "title": f"Review and Refine {goal}",
                    "description": f"Evaluate progress and make improvements to {goal} approach",
                    "estimated_hours": max(6, total_days * 1),
                    "deadline": (base_date + timedelta(days=total_days)).isoformat(),
                    "dependencies": "3",
                    "priority": "medium"
                }
            ]

    def _parse_timeframe(self, timeframe: str) -> int:
        """Convert timeframe string to days"""
        if not timeframe:
            return 30
        
        timeframe = timeframe.lower()
        if "week" in timeframe:
            weeks = int(''.join(filter(str.isdigit, timeframe)) or 1)
            return weeks * 7
        elif "month" in timeframe:
            months = int(''.join(filter(str.isdigit, timeframe)) or 1)
            return months * 30
        elif "day" in timeframe:
            days = int(''.join(filter(str.isdigit, timeframe)) or 1)  # Fixed: default to 1 day, not 7
            return days
        else:
            return 30

# Global instance
ai_service = AIService()
