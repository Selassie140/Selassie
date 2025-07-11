#!/usr/bin/env python3
"""
Birthday Club Backend API Testing Suite
Tests all API endpoints for customer management system
"""

import requests
import sys
import json
from datetime import datetime, date
from typing import Dict, Any, Optional

class BirthdayClubAPITester:
    def __init__(self, base_url: str = "https://09f73bb4-3f31-4dd9-a9e7-200970fa5831.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.created_customers = []  # Track created customers for cleanup
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {test_name}: PASSED {details}")
        else:
            print(f"❌ {test_name}: FAILED {details}")
        return success

    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> tuple[bool, Dict, int]:
        """Make HTTP request and return success, response data, status code"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            else:
                return False, {}, 0
                
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text}
                
            return response.ok, response_data, response.status_code
            
        except Exception as e:
            return False, {"error": str(e)}, 0

    def test_health_check(self) -> bool:
        """Test health check endpoint"""
        success, data, status = self.make_request('GET', 'api/health')
        
        if success and status == 200:
            expected_keys = ['status', 'service']
            has_keys = all(key in data for key in expected_keys)
            return self.log_test("Health Check", has_keys, f"Status: {data.get('status')}")
        else:
            return self.log_test("Health Check", False, f"Status: {status}, Data: {data}")

    def test_customer_signup(self, customer_type: str) -> Optional[str]:
        """Test customer signup and return account number if successful"""
        timestamp = datetime.now().strftime("%H%M%S")
        test_customer = {
            "name": f"Test Customer {customer_type} {timestamp}",
            "phone_number": f"+1555{timestamp}",
            "email": f"test_{customer_type}_{timestamp}@example.com",
            "date_of_birth": "1990-01-15",  # Send as string
            "customer_type": customer_type
        }
        
        success, data, status = self.make_request('POST', 'api/customers/signup', test_customer)
        
        if success and status == 200:
            account_number = data.get('account_number')
            expected_prefix = {
                'subscription': 'SAN-',
                'non_subscription': 'NSAN-',
                'corporate': 'CSAN-'
            }.get(customer_type, 'GEN-')
            
            if account_number and account_number.startswith(expected_prefix):
                self.created_customers.append(account_number)
                self.log_test(f"Customer Signup ({customer_type})", True, 
                            f"Account: {account_number}")
                return account_number
            else:
                self.log_test(f"Customer Signup ({customer_type})", False, 
                            f"Invalid account number: {account_number}")
                return None
        else:
            self.log_test(f"Customer Signup ({customer_type})", False, 
                        f"Status: {status}, Error: {data}")
            return None

    def test_customer_profile_completion(self, account_number: str, customer_type: str) -> bool:
        """Test customer profile completion"""
        timestamp = datetime.now().strftime("%H%M%S")
        profile_data = {
            "account_number": account_number,
            "contact_name": f"Profile Contact {timestamp}",
            "email_address": f"profile_{timestamp}@example.com",
            "employment_title": "Software Engineer",
            "phone_number": f"+1555{timestamp}",
            "birthday_date": "1990-01-15",
            "favorite_bistro_food_items": "Pasta, Pizza",
            "preferred_bistro_beverage": "Wine",
            "interest_in_group_private_package": "both",
            "music_ambiance_preference": "Jazz",
            "allergies": "None",
            "dietary_restrictions": "Vegetarian",
            "celebration_budget": "100_200",
            "group_size_solo": "2_4",
            "preferred_contact_method": "email",
            "want_corporate_offers": True,
            "preferred_celebration_style": "Intimate",
            "personalized_bistro_birthday_treats": "Chocolate cake",
            "interest_in_rewards": True,
            "i_like_surprises": False,
            "special_notes": "Test profile completion"
        }
        
        success, data, status = self.make_request('POST', f'api/customers/{account_number}/profile', profile_data)
        
        if success and status == 200:
            profile_number = data.get('customer_profile_number')
            expected_prefix = {
                'subscription': 'SCPN-',
                'non_subscription': 'NSCPN-',
                'corporate': 'CSCPN-'
            }.get(customer_type, 'GCPN-')
            
            if profile_number and profile_number.startswith(expected_prefix):
                return self.log_test(f"Profile Completion ({customer_type})", True, 
                                   f"Profile: {profile_number}")
            else:
                return self.log_test(f"Profile Completion ({customer_type})", False, 
                                   f"Invalid profile number: {profile_number}")
        else:
            return self.log_test(f"Profile Completion ({customer_type})", False, 
                               f"Status: {status}, Error: {data}")

    def test_get_customer(self, account_number: str) -> bool:
        """Test getting specific customer"""
        success, data, status = self.make_request('GET', f'api/customers/{account_number}')
        
        if success and status == 200:
            required_fields = ['id', 'account_number', 'name', 'email', 'customer_type']
            has_fields = all(field in data for field in required_fields)
            return self.log_test("Get Customer", has_fields, 
                               f"Account: {data.get('account_number')}")
        else:
            return self.log_test("Get Customer", False, f"Status: {status}, Error: {data}")

    def test_get_customer_profile(self, account_number: str) -> bool:
        """Test getting customer profile"""
        success, data, status = self.make_request('GET', f'api/customers/{account_number}/profile')
        
        if success and status == 200:
            profile_fields = ['contact_name', 'email_address', 'customer_profile_number']
            has_fields = all(field in data for field in profile_fields)
            return self.log_test("Get Customer Profile", has_fields, 
                               f"Profile: {data.get('customer_profile_number')}")
        else:
            return self.log_test("Get Customer Profile", False, f"Status: {status}, Error: {data}")

    def test_get_customers_list(self) -> bool:
        """Test getting customers list"""
        success, data, status = self.make_request('GET', 'api/customers')
        
        if success and status == 200:
            is_list = isinstance(data, list)
            return self.log_test("Get Customers List", is_list, 
                               f"Count: {len(data) if is_list else 'Not a list'}")
        else:
            return self.log_test("Get Customers List", False, f"Status: {status}, Error: {data}")

    def test_get_stats(self) -> bool:
        """Test getting statistics"""
        success, data, status = self.make_request('GET', 'api/stats')
        
        if success and status == 200:
            required_stats = ['total_customers', 'subscription_customers', 
                            'non_subscription_customers', 'corporate_customers', 
                            'completed_profiles', 'profile_completion_rate']
            has_stats = all(stat in data for stat in required_stats)
            return self.log_test("Get Statistics", has_stats, 
                               f"Total: {data.get('total_customers', 0)}")
        else:
            return self.log_test("Get Statistics", False, f"Status: {status}, Error: {data}")

    def test_error_handling(self) -> bool:
        """Test error handling for invalid requests"""
        # Test invalid customer type
        invalid_customer = {
            "name": "Invalid Customer",
            "phone_number": "+15551234567",
            "email": "invalid@example.com",
            "date_of_birth": "1990-01-15",
            "customer_type": "invalid_type"
        }
        
        success, data, status = self.make_request('POST', 'api/customers/signup', invalid_customer)
        # Should still work as backend doesn't validate customer_type strictly
        
        # Test non-existent customer
        success, data, status = self.make_request('GET', 'api/customers/INVALID-00000')
        error_handled = not success and status == 404
        
        return self.log_test("Error Handling", error_handled, 
                           f"404 for invalid customer: {status}")

    def run_all_tests(self) -> bool:
        """Run complete test suite"""
        print("🚀 Starting Birthday Club API Tests")
        print("=" * 50)
        
        # Test health check
        self.test_health_check()
        
        # Test customer signup for all types
        customer_types = ['subscription', 'non_subscription', 'corporate']
        account_numbers = {}
        
        for customer_type in customer_types:
            account_number = self.test_customer_signup(customer_type)
            if account_number:
                account_numbers[customer_type] = account_number
        
        # Test profile completion for created customers
        for customer_type, account_number in account_numbers.items():
            self.test_customer_profile_completion(account_number, customer_type)
            
        # Test individual customer retrieval
        if account_numbers:
            first_account = list(account_numbers.values())[0]
            self.test_get_customer(first_account)
            self.test_get_customer_profile(first_account)
        
        # Test list operations
        self.test_get_customers_list()
        self.test_get_stats()
        
        # Test error handling
        self.test_error_handling()
        
        # Print results
        print("\n" + "=" * 50)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.created_customers:
            print(f"🔧 Created test customers: {', '.join(self.created_customers)}")
        
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"✨ Success Rate: {success_rate:.1f}%")
        
        return self.tests_passed == self.tests_run

def main():
    """Main test execution"""
    tester = BirthdayClubAPITester()
    
    try:
        all_passed = tester.run_all_tests()
        return 0 if all_passed else 1
    except Exception as e:
        print(f"❌ Test suite failed with error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())