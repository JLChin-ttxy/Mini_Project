"""
Test script for Dialogflow webhook
Run this after starting your Flask server to test the webhook endpoint
"""
import requests
import json

# Base URL - change if your server is running on a different port/host
BASE_URL = "http://localhost:5000"
WEBHOOK_URL = f"{BASE_URL}/dialogflow-webhook"

def test_webhook(program_name, info_type="requirements"):
    """Test the Dialogflow webhook with a program name"""
    
    # Simulate Dialogflow request format
    payload = {
        "queryResult": {
            "queryText": f"Requirements for {program_name}",
            "parameters": {
                "program_name": program_name,
                "info_type": info_type
            },
            "intent": {
                "displayName": "get_program_requirements"
            }
        }
    }
    
    print(f"\n{'='*60}")
    print(f"Testing: {program_name} ({info_type})")
    print(f"{'='*60}")
    print(f"Request URL: {WEBHOOK_URL}")
    print(f"Request Payload:")
    print(json.dumps(payload, indent=2))
    print(f"\nSending request...")
    
    try:
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ SUCCESS!")
            print(f"Response:")
            print(json.dumps(result, indent=2))
            
            fulfillment_text = result.get("fulfillmentText", "")
            if fulfillment_text:
                print(f"\n📝 Chatbot Response:")
                print(f"   {fulfillment_text}")
            
            # Check if URL is in response
            if "http" in fulfillment_text:
                print(f"\n✅ URL found in response!")
            else:
                print(f"\n⚠️  Warning: No URL found in response")
        else:
            print(f"\n❌ ERROR: Status code {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ ERROR: Could not connect to {WEBHOOK_URL}")
        print(f"   Make sure your Flask server is running!")
        print(f"   Run: python app.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

def test_without_parameters():
    """Test webhook when no program_name is provided"""
    payload = {
        "queryResult": {
            "queryText": "What programs are available?",
            "parameters": {},
            "intent": {
                "displayName": "general_query"
            }
        }
    }
    
    print(f"\n{'='*60}")
    print(f"Testing: No program name provided")
    print(f"{'='*60}")
    
    try:
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        result = response.json()
        print(f"Response: {result.get('fulfillmentText', 'No response')}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

def test_query_text_extraction():
    """Test webhook's ability to extract program name from query text"""
    payload = {
        "queryResult": {
            "queryText": "Requirements for Foundation In Science",
            "parameters": {},  # No parameters - webhook should extract from queryText
            "intent": {
                "displayName": "get_program_requirements"
            }
        }
    }
    
    print(f"\n{'='*60}")
    print(f"Testing: Query text extraction (no parameters)")
    print(f"{'='*60}")
    
    try:
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        result = response.json()
        print(f"Response: {result.get('fulfillmentText', 'No response')}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    print("="*60)
    print("Dialogflow Webhook Test Script")
    print("="*60)
    print(f"\nMake sure your Flask server is running on {BASE_URL}")
    print("If not, start it with: python app.py\n")
    
    input("Press Enter to start testing...")
    
    # Test 1: Foundation in Science
    test_webhook("Foundation in Science", "requirements")
    
    # Test 2: Foundation in Arts
    test_webhook("Foundation in Arts", "requirements")
    
    # Test 3: Different info type
    test_webhook("Foundation in Science", "deadlines")
    
    # Test 4: Case variation
    test_webhook("Foundation In Science", "requirements")
    
    # Test 5: No parameters
    test_without_parameters()
    
    # Test 6: Query text extraction
    test_query_text_extraction()
    
    print(f"\n{'='*60}")
    print("Testing Complete!")
    print(f"{'='*60}")
    print("\nCheck your Flask server console for detailed logs.")
    print("The webhook logs all incoming requests and responses.")
