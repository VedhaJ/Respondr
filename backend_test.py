import requests
import sys
import json
from datetime import datetime

class CyberIncidentAPITester:
    def __init__(self, base_url="https://incident-help.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.session_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                self.failed_tests.append({
                    "test": name,
                    "expected": expected_status,
                    "actual": response.status_code,
                    "response": response.text[:200]
                })
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.failed_tests.append({
                "test": name,
                "error": str(e)
            })
            return False, {}

    def test_root_endpoint(self):
        """Test root API endpoint"""
        return self.run_test(
            "Root API Endpoint",
            "GET",
            "",
            200
        )

    def test_get_incidents(self):
        """Test getting all incidents"""
        success, response = self.run_test(
            "Get All Incidents",
            "GET",
            "incidents",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} incidents")
            expected_platforms = ["Instagram", "Gmail", "Facebook", "WhatsApp", "Twitter", "Microsoft"]
            found_platforms = [incident.get('platform') for incident in response]
            
            for platform in expected_platforms:
                if platform in found_platforms:
                    print(f"   ✅ Found {platform} incident")
                else:
                    print(f"   ❌ Missing {platform} incident")
                    
        return success, response

    def test_get_recovery_links(self, platform="Instagram"):
        """Test getting recovery links for a platform"""
        success, response = self.run_test(
            f"Get Recovery Links for {platform}",
            "GET",
            f"recovery-links/{platform}",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} recovery links for {platform}")
            for link in response:
                if link.get('verified'):
                    print(f"   ✅ Verified link: {link.get('title')}")
                    
        return success, response

    def test_create_chat_session(self, platform="Instagram"):
        """Test creating a chat session"""
        success, response = self.run_test(
            f"Create Chat Session for {platform}",
            "POST",
            "chat/session",
            200,
            data={
                "incident_type": f"{platform} Account Compromised",
                "platform": platform
            }
        )
        
        if success and response.get('id'):
            self.session_id = response['id']
            print(f"   Created session: {self.session_id}")
            
        return success, response

    def test_send_chat_message(self):
        """Test sending a chat message"""
        if not self.session_id:
            print("❌ No session ID available for chat message test")
            return False, {}
            
        success, response = self.run_test(
            "Send Chat Message",
            "POST",
            "chat/message",
            200,
            data={
                "session_id": self.session_id,
                "message": "I can't log into my account. What should I do?"
            }
        )
        
        if success:
            user_msg = response.get('user_message', {})
            ai_msg = response.get('ai_message', {})
            
            if user_msg.get('content') and ai_msg.get('content'):
                print(f"   User message: {user_msg.get('content')[:50]}...")
                print(f"   AI response: {ai_msg.get('content')[:100]}...")
                print("   ✅ Chat exchange successful")
            else:
                print("   ❌ Missing message content in response")
                
        return success, response

    def test_get_chat_messages(self):
        """Test getting chat messages for a session"""
        if not self.session_id:
            print("❌ No session ID available for get messages test")
            return False, {}
            
        success, response = self.run_test(
            "Get Chat Messages",
            "GET",
            f"chat/session/{self.session_id}/messages",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} messages in session")
            
        return success, response

    def test_get_prevention_tips(self):
        """Test getting prevention tips"""
        success, response = self.run_test(
            "Get Prevention Tips",
            "GET",
            "prevention-tips",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} prevention tips")
            for tip in response:
                importance = tip.get('importance', 'unknown')
                title = tip.get('title', 'Unknown')
                print(f"   - {title} ({importance})")
                
        return success, response

    def test_invalid_platform_recovery_links(self):
        """Test getting recovery links for invalid platform"""
        success, response = self.run_test(
            "Get Recovery Links for Invalid Platform",
            "GET",
            "recovery-links/InvalidPlatform",
            404
        )
        return success, response

    def test_invalid_session_message(self):
        """Test sending message to invalid session"""
        success, response = self.run_test(
            "Send Message to Invalid Session",
            "POST",
            "chat/message",
            404,
            data={
                "session_id": "invalid-session-id",
                "message": "Test message"
            }
        )
        return success, response

def main():
    print("🚀 Starting Cyber Incident Response API Tests")
    print("=" * 60)
    
    tester = CyberIncidentAPITester()
    
    # Test all endpoints
    print("\n📋 Testing Core API Endpoints...")
    tester.test_root_endpoint()
    tester.test_get_incidents()
    
    # Test recovery links for multiple platforms
    platforms = ["Instagram", "Gmail", "Facebook", "WhatsApp", "Twitter", "Microsoft"]
    for platform in platforms:
        tester.test_get_recovery_links(platform)
    
    # Test chat functionality
    print("\n💬 Testing Chat Functionality...")
    tester.test_create_chat_session("Instagram")
    
    # Wait a moment for session to be created
    import time
    time.sleep(1)
    
    tester.test_send_chat_message()
    tester.test_get_chat_messages()
    
    # Test prevention tips
    print("\n🛡️ Testing Prevention Tips...")
    tester.test_get_prevention_tips()
    
    # Test error cases
    print("\n🚫 Testing Error Handling...")
    tester.test_invalid_platform_recovery_links()
    tester.test_invalid_session_message()
    
    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} passed")
    
    if tester.failed_tests:
        print("\n❌ Failed Tests:")
        for failure in tester.failed_tests:
            print(f"   - {failure}")
    
    success_rate = (tester.tests_passed / tester.tests_run) * 100 if tester.tests_run > 0 else 0
    print(f"📈 Success Rate: {success_rate:.1f}%")
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())