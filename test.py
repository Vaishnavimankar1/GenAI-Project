"""
Test script to verify the multi-agent system
Run with: python test.py
"""

import os
import sys
from main import MultiAgentOrchestrator

def test_system():
    """Test the multi-agent system with a sample query"""
    
    print("="*70)
    print("TESTING MULTI-AGENT TRAVEL PLANNING SYSTEM")
    print("="*70)
    
    # Check environment variables
    required_vars = ["ANTHROPIC_API_KEY", "OPENWEATHER_API_KEY", "GOOGLE_PLACES_API_KEY"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"\n❌ FAIL: Missing environment variables: {', '.join(missing_vars)}")
        print("\nPlease set them in your .env file or environment.")
        print("Example:")
        print("  export ANTHROPIC_API_KEY=sk-ant-xxx")
        print("  export OPENWEATHER_API_KEY=xxx")
        print("  export GOOGLE_PLACES_API_KEY=xxx")
        return False
    
    print("\n✅ Environment variables configured")
    
    # Test query
    test_query = "Plan a weekend trip to Mumbai with weather forecast and top hotels"
    
    print(f"\n📝 Test Query: {test_query}\n")
    
    try:
        # Initialize and run
        orchestrator = MultiAgentOrchestrator()
        result = orchestrator.process_query(test_query)
        
        if result["success"]:
            print("\n" + "="*70)
            print("✅ TEST PASSED - System is working correctly!")
            print("="*70)
            
            # Verify key components
            checks = [
                ("Plan created", len(result.get("plan", [])) > 0),
                ("Steps executed", result.get("execution_results", {}).get("steps_completed", 0) > 0),
                ("Verification completed", "verification" in result),
                ("Final response generated", len(result.get("final_response", "")) > 0)
            ]
            
            print("\n🔍 Component Checks:")
            for check_name, passed in checks:
                status = "✅" if passed else "❌"
                print(f"  {status} {check_name}")
            
            return True
        else:
            print("\n" + "="*70)
            print("❌ TEST FAILED")
            print("="*70)
            print(f"Error: {result.get('error')}")
            return False
            
    except Exception as e:
        print("\n" + "="*70)
        print("❌ TEST FAILED - Exception occurred")
        print("="*70)
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_system()
    sys.exit(0 if success else 1)
