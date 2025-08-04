#!/usr/bin/env python3
"""
Simple backend test - just check if server can start
"""

import sys
import asyncio
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

async def test_server_startup():
    """Test if the server can start up"""
    print("🧪 Testing server startup...")
    
    try:
        from main import app
        print("✅ FastAPI app imported successfully")
        
        # Check if app has routes
        routes = [route.path for route in app.routes]
        print(f"✅ Found {len(routes)} routes:")
        for route in routes[:10]:  # Show first 10 routes
            print(f"   - {route}")
        if len(routes) > 10:
            print(f"   ... and {len(routes) - 10} more")
        
        # Test basic app properties
        print(f"✅ App title: {app.title}")
        print(f"✅ App version: {app.version}")
        
        return True
        
    except Exception as e:
        print(f"❌ Server startup test failed: {e}")
        return False

def test_database():
    """Test database connection"""
    print("\n🧪 Testing database...")
    
    try:
        from app.core.database import engine, SessionLocal, Base
        from app.models.user import User
        from app.models.music import Track
        
        # Test database connection
        with engine.connect() as connection:
            print("✅ Database connection successful")
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        
        # Test session creation
        db = SessionLocal()
        try:
            # Try to count users
            user_count = db.query(User).count()
            print(f"✅ Database query successful - {user_count} users in database")
        finally:
            db.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_config():
    """Test configuration"""
    print("\n🧪 Testing configuration...")
    
    try:
        from app.core.config import settings
        
        print(f"✅ Config loaded successfully")
        print(f"   - Debug mode: {settings.DEBUG}")
        print(f"   - Database URL: {settings.DATABASE_URL}")
        print(f"   - Secret key: {'*' * 20} (hidden)")
        print(f"   - Spotify configured: {'Yes' if settings.SPOTIFY_CLIENT_ID else 'No'}")
        print(f"   - Apple Music configured: {'Yes' if settings.APPLE_MUSIC_TEAM_ID else 'No'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🎵 ChordCircle Backend Simple Tests")
    print("=" * 50)
    
    tests = [
        ("Server Startup", test_server_startup),
        ("Database", test_database),
        ("Configuration", test_config)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        if asyncio.iscoroutinefunction(test_func):
            result = await test_func()
        else:
            result = test_func()
        
        if result:
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready!")
        print("\n🚀 To start the server:")
        print("   python start.py")
        print("   or")
        print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        print("\n🌐 Server will be available at:")
        print("   - API: http://localhost:8000")
        print("   - Docs: http://localhost:8000/docs")
        return True
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)