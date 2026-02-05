"""
Streamlit Web Interface for Multi-Agent Travel Planning System
Run with: streamlit run app.py
"""

import streamlit as st
import os
import json
from main import MultiAgentOrchestrator, TravelPlanningTools
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

def main():
    st.title("✈️ Multi-Agent Travel Planning System")
    st.markdown("*Powered by Claude AI, OpenWeatherMap & Google Places*")
    
    # Sidebar with info
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This system uses **3 AI agents**:
        
        1. 🧠 **Planner Agent**  
           Creates execution plan
        
        2. ⚡ **Executor Agent**  
           Calls real APIs
        
        3. ✓ **Verifier Agent**  
           Validates results
        """)
        
        st.divider()
        
        st.header("🔑 API Status")
        
        # Check API keys
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        weather_key = os.getenv("OPENWEATHER_API_KEY")
        places_key = os.getenv("GOOGLE_PLACES_API_KEY")
        
        st.markdown(f"**Anthropic:** {'✅' if anthropic_key else '❌'}")
        st.markdown(f"**Weather:** {'✅' if weather_key else '❌'}")
        st.markdown(f"**Places:** {'✅' if places_key else '❌'}")
        
        if not all([anthropic_key, weather_key, places_key]):
            st.error("⚠️ Missing API keys! Check .env file")
        
        st.divider()
        
        st.header("📋 Example Queries")
        examples = [
            "Plan a weekend trip to Mumbai with weather and hotels",
            "I want to visit Goa. Show me weather and restaurants",
            "Plan a trip to Delhi with tourist attractions",
            "Beach vacation in Kerala with resorts",
            "Business trip to Bangalore with weather and hotels"
        ]
        
        for example in examples:
            if st.button(example, key=example):
                st.session_state.query = example
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Query input
        query = st.text_input(
            "🗣️ What trip would you like to plan?",
            value=st.session_state.get('query', ''),
            placeholder="E.g., Plan a weekend trip to Goa with weather and hotels"
        )
        
        submit_button = st.button("🚀 Plan My Trip", type="primary")
    
    with col2:
        st.metric("Total Queries", len(st.session_state.history))
    
    # Process query
    if submit_button and query:
        # Check API keys
        if not all([anthropic_key, weather_key, places_key]):
            st.error("❌ Please configure API keys in .env file first!")
            return
        
        with st.spinner("🤖 AI Agents are working..."):
            try:
                # Initialize orchestrator
                orchestrator = MultiAgentOrchestrator()
                
                # Create tabs for different views
                tab1, tab2, tab3, tab4 = st.tabs(["📝 Response", "📊 Plan", "⚙️ Execution", "✓ Verification"])
                
                # Process query
                result = orchestrator.process_query(query)
                
                if result["success"]:
                    # Tab 1: Final Response
                    with tab1:
                        st.success("✅ Trip planned successfully!")
                        st.markdown(result["final_response"])
                    
                    # Tab 2: Plan
                    with tab2:
                        st.subheader("🧠 Planner Agent Output")
                        for step in result["plan"]:
                            with st.expander(f"Step {step['step_number']}: {step['description']}"):
                                st.json({
                                    "action": step["action"],
                                    "parameters": step["parameters"]
                                })
                    
                    # Tab 3: Execution Results
                    with tab3:
                        st.subheader("⚡ Executor Agent Output")
                        exec_results = result["execution_results"]
                        
                        st.metric(
                            "Steps Completed",
                            f"{exec_results['steps_completed']}/{len(result['plan'])}"
                        )
                        
                        for step_result in exec_results["step_results"]:
                            with st.expander(f"Step {step_result['step_number']}: {step_result['description']}"):
                                if step_result["result"]["success"]:
                                    st.success("✅ Success")
                                    st.json(step_result["result"]["data"])
                                else:
                                    st.error(f"❌ Failed: {step_result['result']['error']}")
                    
                    # Tab 4: Verification
                    with tab4:
                        st.subheader("✓ Verifier Agent Output")
                        if result["verification"]:
                            verification = result["verification"]
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Completeness Score", f"{verification.get('completeness_score', 0)}%")
                            with col2:
                                status = "✅ PASSED" if verification.get('verification_passed') else "❌ FAILED"
                                st.metric("Status", status)
                            
                            if verification.get('issues'):
                                st.warning("⚠️ Issues Found:")
                                for issue in verification['issues']:
                                    st.markdown(f"- {issue}")
                            
                            st.markdown(f"**Summary:** {verification.get('summary', 'N/A')}")
                    
                    # Add to history
                    st.session_state.history.append({
                        "query": query,
                        "result": result
                    })
                    
                else:
                    st.error(f"❌ Error: {result.get('error')}")
                    st.json(result)
                    
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
                st.exception(e)
    
    # Show history
    if st.session_state.history:
        st.divider()
        st.subheader("📜 Query History")
        
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Query {len(st.session_state.history) - i}: {item['query'][:50]}..."):
                st.markdown(item['result']['final_response'])

if __name__ == "__main__":
    main()
