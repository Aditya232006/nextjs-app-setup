#!/usr/bin/env python3
"""
Simple test script to verify API functionality
"""
import requests
import json
from datetime import datetime, date

BASE_URL = "http://localhost:8000"

def test_api():
    print("Testing Old Age Home Management API...")
    print("=" * 50)
    
    # Test 1: Get dashboard stats
    print("\n1. Testing Dashboard Stats...")
    try:
        response = requests.get(f"{BASE_URL}/api/dashboard/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Dashboard Stats: {stats}")
        else:
            print(f"❌ Dashboard Stats failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Dashboard Stats error: {e}")
    
    # Test 2: Get all residents
    print("\n2. Testing Get Residents...")
    try:
        response = requests.get(f"{BASE_URL}/api/residents/")
        if response.status_code == 200:
            residents = response.json()
            print(f"✅ Found {len(residents)} residents")
            if residents:
                print(f"   First resident: {residents[0]['name']}")
        else:
            print(f"❌ Get Residents failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get Residents error: {e}")
    
    # Test 3: Create a new resident
    print("\n3. Testing Create Resident...")
    try:
        new_resident = {
            "name": "Test Resident",
            "age": 75,
            "date_of_birth": "1948-12-25",
            "gender": "Male",
            "phone": "555-9999",
            "emergency_contact": "Test Contact",
            "emergency_phone": "555-8888",
            "address": "123 Test Street",
            "medical_conditions": "None",
            "admission_date": str(date.today()),
            "status": "active"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/residents/",
            json=new_resident,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            created_resident = response.json()
            print(f"✅ Created resident: {created_resident['name']} (ID: {created_resident['id']})")
            return created_resident['id']
        else:
            print(f"❌ Create Resident failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Create Resident error: {e}")
    
    # Test 4: Get vacant beds
    print("\n4. Testing Get Vacant Beds...")
    try:
        response = requests.get(f"{BASE_URL}/api/beds/vacant")
        if response.status_code == 200:
            vacant_beds = response.json()
            print(f"✅ Found {len(vacant_beds)} vacant beds")
        else:
            print(f"❌ Get Vacant Beds failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get Vacant Beds error: {e}")
    
    # Test 5: Get upcoming birthdays
    print("\n5. Testing Upcoming Birthdays...")
    try:
        response = requests.get(f"{BASE_URL}/api/birthdays/upcoming")
        if response.status_code == 200:
            birthdays = response.json()
            print(f"✅ Found {len(birthdays)} upcoming birthdays")
        else:
            print(f"❌ Get Upcoming Birthdays failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get Upcoming Birthdays error: {e}")
    
    # Test 6: Get today's checkups
    print("\n6. Testing Today's Checkups...")
    try:
        response = requests.get(f"{BASE_URL}/api/checkups/today")
        if response.status_code == 200:
            checkups = response.json()
            print(f"✅ Found {len(checkups)} checkups for today")
        else:
            print(f"❌ Get Today's Checkups failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get Today's Checkups error: {e}")
    
    # Test 7: Get upcoming events
    print("\n7. Testing Upcoming Events...")
    try:
        response = requests.get(f"{BASE_URL}/api/events/upcoming")
        if response.status_code == 200:
            events = response.json()
            print(f"✅ Found {len(events)} upcoming events")
        else:
            print(f"❌ Get Upcoming Events failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get Upcoming Events error: {e}")
    
    print("\n" + "=" * 50)
    print("API Testing Complete!")
    print("\nTo run the server:")
    print("cd backend && python run.py")
    print("\nAPI Documentation available at:")
    print("http://localhost:8000/docs")

if __name__ == "__main__":
    test_api()
