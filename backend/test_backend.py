#!/usr/bin/env python3
"""
Quick test script to verify backend functionality
"""
import requests
import json
import sys

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on port 8000")
        return False

def test_query():
    """Test query endpoint"""
    print("\nTesting query endpoint...")
    try:
        payload = {
            "query": "Where can I eat ramen near Blok M?",
            "user_lat": -6.2441,  # Blok M coordinates
            "user_lng": 106.7991
        }
        
        response = requests.post(
            "http://localhost:8000/api/query",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Query endpoint works!")
            print(f"\nAI Response: {data['ai_response']}")
            print(f"Found {len(data['places'])} places")
            
            if data['places']:
                place = data['places'][0]
                print(f"\nFirst place: {place['name']}")
                print(f"Address: {place['address']}")
                if place.get('recommended_transport'):
                    print(f"Recommended: {place['recommended_transport']}")
            
            return True
        else:
            print(f"❌ Query failed: {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Query timed out (>30s). Check if Ollama is running.")
        return False
    except Exception as e:
        print(f"❌ Query error: {e}")
        return False

def main():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  HeyPico AI Maps - Backend Test")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    
    # Test health
    if not test_health():
        sys.exit(1)
    
    # Test query
    if not test_query():
        sys.exit(1)
    
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  All tests passed! ✅")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("\nBackend is working correctly.")
    print("You can now start the frontend with: npm run dev")

if __name__ == "__main__":
    main()
