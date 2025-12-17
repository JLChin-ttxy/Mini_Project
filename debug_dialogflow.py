"""
Debug script to check if Dialogflow can reach your webhook
"""
import requests
import json
from datetime import datetime

WEBHOOK_URL = "http://172.20.10.3:5000/dialogflow-webhook"

def test_webhook_accessible():
    """Test if webhook is accessible from this machine"""
    print("="*60)
    print("Testing Webhook Accessibility")
    print("="*60)
    
    # Test 1: Simple connectivity
    print("\n1. Testing basic connectivity...")
    try:
        response = requests.get("http://172.20.10.3:5000", timeout=5)
        print(f"   ✅ Flask server is accessible: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ ERROR: Cannot connect to Flask server!")
        print("   → Make sure Flask is running: python app.py")
        print("   → Make sure it's listening on 0.0.0.0, not just localhost")
        return False
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False
    
    # Test 2: Webhook endpoint
    print("\n2. Testing webhook endpoint...")
    test_payload = {
        "queryResult": {
            "queryText": "Requirements for Foundation in Science",
            "parameters": {
                "program_name": "Foundation in Science",
                "info_type": "requirements"
            }
        }
    }
    
    try:
        response = requests.post(
            WEBHOOK_URL,
            json=test_payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Webhook responded successfully!")
            print(f"   Response: {result.get('fulfillmentText', 'No fulfillmentText')}")
            return True
        else:
            print(f"   ❌ Webhook returned error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ ERROR: Cannot connect to webhook!")
        print("   → Check if Flask server is running")
        print("   → Check firewall settings")
        return False
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def check_flask_config():
    """Check if Flask is configured to accept external connections"""
    print("\n" + "="*60)
    print("Checking Flask Configuration")
    print("="*60)
    
    try:
        with open("app.py", "r") as f:
            content = f.read()
            if "host='0.0.0.0'" in content or 'host="0.0.0.0"' in content:
                print("   ✅ Flask is configured to accept external connections (0.0.0.0)")
            else:
                print("   ⚠️  WARNING: Flask might only be listening on localhost")
                print("   → Check app.py - should have: app.run(host='0.0.0.0', port=5000)")
    except Exception as e:
        print(f"   ⚠️  Could not check app.py: {e}")

def check_dialogflow_requirements():
    """Check Dialogflow configuration requirements"""
    print("\n" + "="*60)
    print("Dialogflow Configuration Checklist")
    print("="*60)
    print("\nPlease verify in Dialogflow console:")
    print("  [ ] Settings → Fulfillment → Webhook URL is set to:")
    print(f"      {WEBHOOK_URL}")
    print("  [ ] Settings → Fulfillment → Webhook is ENABLED")
    print("  [ ] Intent → Fulfillment → 'Enable webhook call' is CHECKED")
    print("  [ ] Intent → Responses → All static responses are DELETED")
    print("\n⚠️  IMPORTANT: Dialogflow cannot reach local IP addresses!")
    print("   Your IP 172.20.10.3 is a local/private IP.")
    print("   Dialogflow needs a PUBLIC URL to reach your webhook.")
    print("\n   Solutions:")
    print("   1. Use ngrok to create a public tunnel:")
    print("      - Download ngrok: https://ngrok.com/")
    print("      - Run: ngrok http 5000")
    print("      - Use the ngrok URL in Dialogflow")
    print("   2. Deploy your Flask app to a public server")
    print("   3. Use a cloud service (Heroku, AWS, etc.)")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Dialogflow Webhook Debug Tool")
    print("="*60)
    print(f"\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Webhook URL: {WEBHOOK_URL}\n")
    
    # Check Flask config
    check_flask_config()
    
    # Test webhook
    is_accessible = test_webhook_accessible()
    
    # Check Dialogflow requirements
    check_dialogflow_requirements()
    
    print("\n" + "="*60)
    if is_accessible:
        print("✅ Webhook is working locally!")
        print("⚠️  But Dialogflow might not be able to reach it (local IP issue)")
    else:
        print("❌ Webhook is NOT accessible!")
        print("   Fix the issues above first.")
    print("="*60)
