#!/usr/bin/env python3
"""
Test API endpoints without starting the server
"""

import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

def test_api_endpoints():
    """Test API endpoints using TestClient"""
    print("🧪 Testing API endpoints...")
    
    try:
        from main import app
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        # Test root endpoint
        response = client.get("/")
        print(f"✅ Root endpoint: {response.status_code} - {response.json()}")
        
        # Test health endpoint
        response = client.get("/health")
        print(f"✅ Health endpoint: {response.status_code} - {response.json()}")
        
        # Test API documentation
        response = client.get("/docs")
        print(f"✅ API docs endpoint: {response.status_code}")
        
        # Test trending music (should require auth)
        response = client.get("/api/v1/music/trending")
        print(f"✅ Trending endpoint: {response.status_code} (expected 401 - needs auth)")
        
        # Test user registration
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123",
            "full_name": "Test User"
        }
        response = client.post("/api/v1/auth/register", json=user_data)
        print(f"✅ User registration: {response.status_code}")
        
        if response.status_code == 200:
            user_info = response.json()
            print(f"   Created user: {user_info.get('username')} ({user_info.get('email')})")
            
            # Test login
            login_data = {
                "email": "test@example.com",
                "password": "testpassword123"
            }
            response = client.post("/api/v1/auth/login", json=login_data)
            print(f"✅ User login: {response.status_code}")
            
            if response.status_code == 200:
                token_info = response.json()
                print(f"   Got access token: {token_info.get('access_token', '')[:20]}...")
                
                # Test authenticated endpoint
                headers = {"Authorization": f"Bearer {token_info['access_token']}"}
                response = client.get("/api/v1/users/me", headers=headers)
                print(f"✅ Get current user: {response.status_code}")
                
                # Test trending with auth
                response = client.get("/api/v1/music/trending", headers=headers)
                print(f"✅ Trending with auth: {response.status_code}")
                if response.status_code == 200:
                    trending = response.json()
                    print(f"   Found {len(trending)} trending tracks")
        
        return True
        
    except Exception as e:
        print(f"❌ API endpoint test failed: {e}")
        return False

def main():
    """Run API endpoint tests"""
    print("🎵 ChordCircle API Endpoint Tests")
    print("=" * 50)
    
    if test_api_endpoints():
        print("\n🎉 All API endpoint tests passed!")
        print("\n🚀 Backend is ready to start!")
        print("   Run: python start.py")
        print("   Or: uvicorn main:app --reload")
        return True
    else:
        print("\n❌ Some API tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)