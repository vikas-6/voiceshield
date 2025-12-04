#!/usr/bin/env python3
"""
VoiceShield AI Backend API Testing
Tests all backend endpoints and functionality
"""
import requests
import sys
import json
import io
from datetime import datetime

class VoiceShieldAPITester:
    def __init__(self, base_url="https://voiceshield-1.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            self.failed_tests.append({"name": name, "details": details})
            print(f"❌ {name} - FAILED: {details}")

    def test_health_check(self):
        """Test basic health check endpoint"""
        try:
            response = requests.get(f"{self.api_url}/", timeout=10)
            success = response.status_code == 200
            data = response.json() if success else {}
            
            if success and "VoiceShield AI Backend" in data.get("message", ""):
                self.log_test("Health Check", True)
                return True
            else:
                self.log_test("Health Check", False, f"Status: {response.status_code}, Response: {data}")
                return False
        except Exception as e:
            self.log_test("Health Check", False, str(e))
            return False

    def test_status_endpoints(self):
        """Test status check endpoints"""
        # Test POST /api/status
        try:
            test_data = {"client_name": f"test_client_{datetime.now().strftime('%H%M%S')}"}
            response = requests.post(f"{self.api_url}/status", json=test_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "id" in data and "client_name" in data and "timestamp" in data:
                    self.log_test("POST /api/status", True)
                else:
                    self.log_test("POST /api/status", False, f"Missing fields in response: {data}")
            else:
                self.log_test("POST /api/status", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("POST /api/status", False, str(e))

        # Test GET /api/status
        try:
            response = requests.get(f"{self.api_url}/status", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("GET /api/status", True)
                else:
                    self.log_test("GET /api/status", False, f"Expected list, got: {type(data)}")
            else:
                self.log_test("GET /api/status", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/status", False, str(e))

    def test_voice_processing(self):
        """Test voice processing endpoint with mock audio"""
        try:
            # Create a mock audio file (small webm-like data)
            mock_audio_data = b"mock_audio_data_for_testing" * 10  # Make it larger than 100 bytes
            
            files = {
                'audio': ('test_recording.webm', io.BytesIO(mock_audio_data), 'audio/webm')
            }
            
            response = requests.post(f"{self.api_url}/voice", files=files, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["id", "transcript", "type", "severity", "assistant_reply", "timestamp"]
                
                missing_fields = [field for field in required_fields if field not in data]
                if not missing_fields:
                    # Validate emergency types
                    valid_types = ["FIRE", "MEDICAL", "VIOLENCE", "ACCIDENT", "NORMAL"]
                    if data["type"] in valid_types and 1 <= data["severity"] <= 10:
                        self.log_test("POST /api/voice", True)
                        return data
                    else:
                        self.log_test("POST /api/voice", False, f"Invalid type/severity: {data['type']}/{data['severity']}")
                else:
                    self.log_test("POST /api/voice", False, f"Missing fields: {missing_fields}")
            else:
                self.log_test("POST /api/voice", False, f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("POST /api/voice", False, str(e))
        
        return None

    def test_events_endpoint(self):
        """Test events retrieval endpoint"""
        try:
            response = requests.get(f"{self.api_url}/events", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "events" in data and "count" in data and isinstance(data["events"], list):
                    self.log_test("GET /api/events", True)
                    return data
                else:
                    self.log_test("GET /api/events", False, f"Invalid response format: {data}")
            else:
                self.log_test("GET /api/events", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/events", False, str(e))
        
        return None

    def test_emergency_types(self):
        """Test all 5 emergency types through voice processing"""
        emergency_keywords = {
            "FIRE": b"fire_emergency_test_data" * 15,
            "MEDICAL": b"medical_emergency_test_data" * 15,
            "VIOLENCE": b"violence_emergency_test_data" * 15,
            "ACCIDENT": b"accident_emergency_test_data" * 15,
            "NORMAL": b"normal_message_test_data" * 15
        }
        
        detected_types = set()
        
        for expected_type, audio_data in emergency_keywords.items():
            try:
                files = {
                    'audio': (f'test_{expected_type.lower()}.webm', io.BytesIO(audio_data), 'audio/webm')
                }
                
                response = requests.post(f"{self.api_url}/voice", files=files, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    detected_types.add(data.get("type", "UNKNOWN"))
                    print(f"  📝 Audio test for {expected_type}: Detected as {data.get('type', 'UNKNOWN')}")
                else:
                    print(f"  ❌ Audio test for {expected_type}: HTTP {response.status_code}")
            except Exception as e:
                print(f"  ❌ Audio test for {expected_type}: {str(e)}")
        
        # Check if we got variety in emergency types
        if len(detected_types) >= 3:  # Should detect at least 3 different types
            self.log_test("Emergency Type Variety", True)
        else:
            self.log_test("Emergency Type Variety", False, f"Only detected types: {detected_types}")

    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting VoiceShield AI Backend Tests")
        print(f"🔗 Testing against: {self.base_url}")
        print("=" * 60)
        
        # Basic connectivity
        if not self.test_health_check():
            print("❌ Health check failed - stopping tests")
            return False
        
        # Status endpoints
        self.test_status_endpoints()
        
        # Voice processing
        voice_result = self.test_voice_processing()
        
        # Events endpoint
        events_result = self.test_events_endpoint()
        
        # Emergency type variety
        self.test_emergency_types()
        
        # Print summary
        print("\n" + "=" * 60)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} passed")
        
        if self.failed_tests:
            print("\n❌ Failed Tests:")
            for test in self.failed_tests:
                print(f"  • {test['name']}: {test['details']}")
        
        success_rate = (self.tests_passed / self.tests_run) * 100 if self.tests_run > 0 else 0
        print(f"✨ Success Rate: {success_rate:.1f}%")
        
        return success_rate >= 70  # Consider 70%+ as acceptable

def main():
    tester = VoiceShieldAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())