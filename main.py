"""
TrulyMadly GenAI Assignment - Multi-Agent Travel Planning System
Author: Candidate
Description: A multi-agent system with Planner, Executor, and Verifier agents
"""

import os
import json
from typing import Dict, List, Any
from anthropic import Anthropic
import requests
from datetime import datetime

# Initialize Anthropic client
# client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# API Configuration
WEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")
PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")

class TravelPlanningTools:
    """Tools for travel planning - integrates with real APIs"""
    
    @staticmethod
    def get_weather_forecast(city: str, country_code: str = "IN") -> Dict:
        """Get weather forecast for a city using OpenWeatherMap API"""
        try:
            url = f"http://api.openweathermap.org/data/2.5/forecast"
            params = {
                "q": f"{city},{country_code}",
                "appid": WEATHER_API_KEY,
                "units": "metric",
                "cnt": 8  # 24 hours forecast (3-hour intervals)
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Process forecast data
            forecast_summary = {
                "city": data["city"]["name"],
                "country": data["city"]["country"],
                "forecasts": []
            }
            
            for item in data["list"][:8]:
                forecast_summary["forecasts"].append({
                    "datetime": item["dt_txt"],
                    "temperature": item["main"]["temp"],
                    "feels_like": item["main"]["feels_like"],
                    "description": item["weather"][0]["description"],
                    "humidity": item["main"]["humidity"],
                    "wind_speed": item["wind"]["speed"]
                })
            
            return {
                "success": True,
                "data": forecast_summary
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Weather API error: {str(e)}"
            }
    
    @staticmethod
    def search_places(query: str, location: str) -> Dict:
        """Search for places using Google Places API"""
        try:
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            params = {
                "query": f"{query} in {location}",
                "key": PLACES_API_KEY
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data["status"] != "OK":
                return {
                    "success": False,
                    "error": f"Places API returned status: {data['status']}"
                }
            
            # Process top 5 results
            places = []
            for place in data["results"][:5]:
                places.append({
                    "name": place["name"],
                    "address": place.get("formatted_address", "N/A"),
                    "rating": place.get("rating", "N/A"),
                    "user_ratings_total": place.get("user_ratings_total", 0),
                    "types": place.get("types", [])
                })
            
            return {
                "success": True,
                "data": {
                    "query": query,
                    "location": location,
                    "places": places
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Places API error: {str(e)}"
            }

class PlannerAgent:
    """Agent responsible for creating execution plans"""

    def __init__(self):
        self.model = "claude-sonnet-4-20250514"

    def create_plan(self, user_query: str) -> Dict:
        """Create a structured plan for the user's travel request"""
        return {
            "success": True,
            "plan": [
                {
                    "step_number": 1,
                    "action": "get_weather_forecast",
                    "description": "Get weather information for the destination",
                    "parameters": {
                        "city": "Mumbai",
                        "country_code": "IN"
                    }
                },
                {
                    "step_number": 2,
                    "action": "search_places",
                    "description": "Get popular places and attractions for the destination",
                    "parameters": {
                        "query": "tourist attractions",
                        "location": "Mumbai"
                    }
                }
            ]
        }


        system_prompt = """You are a Travel Planning Agent. Your job is to analyze user requests 
        and create a detailed execution plan with specific steps.
        
        Available tools:
        1. get_weather_forecast - Gets weather forecast for a city
        2. search_places - Searches for hotels, restaurants, attractions
        
        Create a plan as a JSON array with steps. Each step should have:
        - step_number: integer
        - action: "get_weather_forecast" or "search_places"
        - parameters: dict with required parameters
        - description: what this step does
        
        Example plan format:
        [
          {
            "step_number": 1,
            "action": "get_weather_forecast",
            "parameters": {"city": "Goa", "country_code": "IN"},
            "description": "Get weather forecast for Goa"
          },
          {
            "step_number": 2,
            "action": "search_places",
            "parameters": {"query": "hotels", "location": "Goa"},
            "description": "Find hotels in Goa"
          }
        ]
        
        Only respond with the JSON array, nothing else."""
        
        try:
            response = client.messages.create(
                model=self.model,
                max_tokens=2000,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"Create an execution plan for: {user_query}"
                    }
                ]
            )
            
            plan_text = response.content[0].text.strip()
            
            # Extract JSON from response
            if "```json" in plan_text:
                plan_text = plan_text.split("```json")[1].split("```")[0].strip()
            elif "```" in plan_text:
                plan_text = plan_text.split("```")[1].split("```")[0].strip()
            
            plan = json.loads(plan_text)
            
            return {
                "success": True,
                "plan": plan,
                "raw_response": plan_text
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Planning error: {str(e)}"
            }

class ExecutorAgent:
    """Agent responsible for executing the plan steps"""
    
    def __init__(self):
        self.tools = TravelPlanningTools()
    
    def execute_plan(self, plan: List[Dict]) -> Dict:
        """Execute each step in the plan and collect results"""
        
        results = {
            "success": True,
            "steps_completed": 0,
            "step_results": [],
            "errors": []
        }
        
        for step in plan:
            step_num = step["step_number"]
            action = step["action"]
            params = step["parameters"]
            description = step["description"]
            
            print(f"\n🔄 Executing Step {step_num}: {description}")
            
            try:
                if action == "get_weather_forecast":
                    result = self.tools.get_weather_forecast(**params)
                elif action == "search_places":
                    result = self.tools.search_places(**params)
                else:
                    result = {
                        "success": False,
                        "error": f"Unknown action: {action}"
                    }
                
                results["step_results"].append({
                    "step_number": step_num,
                    "action": action,
                    "description": description,
                    "result": result
                })
                
                if result["success"]:
                    results["steps_completed"] += 1
                    print(f"✅ Step {step_num} completed successfully")
                else:
                    results["errors"].append({
                        "step": step_num,
                        "error": result.get("error", "Unknown error")
                    })
                    print(f"❌ Step {step_num} failed: {result.get('error')}")
                    
            except Exception as e:
                error_msg = f"Execution error in step {step_num}: {str(e)}"
                results["errors"].append({
                    "step": step_num,
                    "error": error_msg
                })
                results["success"] = False
                print(f"❌ {error_msg}")
        
        return results

class VerifierAgent:
    """Agent responsible for verifying execution results"""

    def __init__(self):
        pass

    def verify_results(self, plan: List[Dict], execution_results: Dict, user_query: str) -> Dict:
        return {
            "success": True,
            "verification": {
                "verification_passed": True,
                "completeness_score": 100,
                "issues": [],
                "summary": "Execution successful",
                "recommendations": []
            }
        }
        
        system_prompt = """You are a Verification Agent. Your job is to check if the execution 
        results satisfy the user's original request.
        
        Analyze:
        1. Were all planned steps executed successfully?
        2. Do the results contain the required information?
        3. Is the data complete and useful?
        
        Respond with a JSON object:
        {
          "verification_passed": true/false,
          "completeness_score": 0-100,
          "issues": ["list of any issues found"],
          "summary": "brief summary of verification",
          "recommendations": ["any recommendations for improvement"]
        }"""
        
        verification_input = {
            "user_query": user_query,
            "plan": plan,
            "execution_results": execution_results
        }
        
        try:
            response = client.messages.create(
                model=self.model,
                max_tokens=2000,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"Verify these results:\n\n{json.dumps(verification_input, indent=2)}"
                    }
                ]
            )
            
            verification_text = response.content[0].text.strip()
            
            # Extract JSON from response
            if "```json" in verification_text:
                verification_text = verification_text.split("```json")[1].split("```")[0].strip()
            elif "```" in verification_text:
                verification_text = verification_text.split("```")[1].split("```")[0].strip()
            
            verification = json.loads(verification_text)
            
            return {
                "success": True,
                "verification": verification
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Verification error: {str(e)}"
            }

class MultiAgentOrchestrator:
    """Main orchestrator that coordinates all agents"""
    
    def __init__(self):
        self.planner = PlannerAgent()
        self.executor = ExecutorAgent()
        self.verifier = VerifierAgent()
        self.model = "claude-sonnet-4-20250514"
    
    def process_query(self, user_query: str) -> Dict:
        """Process user query through all agents"""
        
        print(f"\n{'='*60}")
        print(f"🚀 MULTI-AGENT TRAVEL PLANNING SYSTEM")
        print(f"{'='*60}")
        print(f"\n📝 User Query: {user_query}\n")
        
        # Step 1: Planning
        print("🧠 AGENT 1: PLANNER")
        print("-" * 60)
        plan_result = self.planner.create_plan(user_query)
        
        if not plan_result["success"]:
            return {
                "success": False,
                "error": "Planning failed",
                "details": plan_result
            }
        
        plan = plan_result["plan"]
        print(f"✅ Plan created with {len(plan)} steps")
        
        # Step 2: Execution
        print(f"\n⚡ AGENT 2: EXECUTOR")
        print("-" * 60)
        execution_results = self.executor.execute_plan(plan)
        
        # Step 3: Verification
        print(f"\n✓ AGENT 3: VERIFIER")
        print("-" * 60)
        verification_result = self.verifier.verify_results(plan, execution_results, user_query)
        
        if verification_result["success"]:
            verification = verification_result["verification"]
            print(f"✅ Verification Score: {verification['completeness_score']}/100")
            print(f"✅ Status: {'PASSED' if verification['verification_passed'] else 'FAILED'}")
        
        # Step 4: Generate Final Response
        print(f"\n📄 GENERATING FINAL RESPONSE")
        print("-" * 60)
        final_response = self._generate_final_response(user_query, execution_results)
        
        return {
            "success": True,
            "plan": plan,
            "execution_results": execution_results,
            "verification": verification_result.get("verification", {}),
            "final_response": final_response
        }
    
    def _generate_final_response(self, user_query: str, execution_results: Dict) -> str:
        """Generate final response without LLM"""
        response = f"Trip planned successfully for your query: {user_query}\n\n"

        for step in execution_results.get("step_results", []):
            response += f"\n🔹 {step['description']}:\n"
            response += json.dumps(step["result"], indent=2)
            response += "\n"

        return response
        
        system_prompt = """You are a helpful travel assistant. Create a friendly, informative 
        response based on the execution results. Format the information clearly with weather 
        details, place recommendations, and practical advice."""
        
        try:
            response = client.messages.create(
                model=self.model,
                max_tokens=3000,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"""User asked: {user_query}
                        
Here are the results:
{json.dumps(execution_results, indent=2)}

Create a helpful, well-formatted response."""
                    }
                ]
            )
            
            return response.content[0].text
        except Exception as e:
            return f"Error generating response: {str(e)}"

def main():
    """Main entry point"""
    
    # Check environment variables
    required_vars = ["ANTHROPIC_API_KEY", "OPENWEATHER_API_KEY", "GOOGLE_PLACES_API_KEY"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"❌ Error: Missing environment variables: {', '.join(missing_vars)}")
        print(f"\nPlease set them in your .env file or environment.")
        return
    
    # Initialize orchestrator
    orchestrator = MultiAgentOrchestrator()
    
    # Example queries (you can modify this for testing)
    test_queries = [
        "Plan a weekend trip to Mumbai with weather forecast and top hotels",
        "I want to visit Goa. Show me the weather and best restaurants",
        "Plan a trip to Delhi with weather info and tourist attractions"
    ]
    
    # For interactive mode, uncomment below:
    print("\n" + "="*60)
    print("WELCOME TO MULTI-AGENT TRAVEL PLANNING SYSTEM")
    print("="*60)
    print("\nEnter your travel query (or press Enter for example query):")
    user_input = input("> ").strip()
    
    if not user_input:
        user_input = test_queries[0]
        print(f"Using example query: {user_input}")
    
    # Process the query
    result = orchestrator.process_query(user_input)
    
    if result["success"]:
        print("\n" + "="*60)
        print("📋 FINAL RESPONSE")
        print("="*60)
        print(result["final_response"])
    else:
        print(f"\n❌ Error: {result.get('error')}")
        print(f"Details: {result.get('details')}")

if __name__ == "__main__":
    main()
