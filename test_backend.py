#!/usr/bin/env python3
"""
Simple backend test script
"""

import sys
import os
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy imported successfully")
    except ImportError as e:
        print(f"❌ SQLAlchemy import failed: {e}")
        return False
    
    try:
        from jose import jwt
        print("✅ Python-JOSE imported successfully")
    except ImportError as e:
        print(f"❌ Python-JOSE import failed: {e}")
        return False
    
    try:
        from passlib.context import CryptContext
        print("✅ Passlib imported successfully")
    except ImportError as e:
        print(f"❌ Passlib import failed: {e}")
        return False
    
    return True

def test_app_imports():
    """Test if our app modules can be imported"""
    print("\n🧪 Testing app imports...")
    
    try:
        from app.core.config import settings
        print("✅ Config imported successfully")
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from app.core.database import Base, engine
        print("✅ Database imported successfully")
    except ImportError as e:
        print(f"❌ Database import failed: {e}")
        return False
    
    try:
        from app.models.user import User
        print("✅ User model imported successfully")
    except ImportError as e:
        print(f"❌ User model import failed: {e}")
        return False
    
    try:
        from app.api.v1.api import api_router
        print("✅ API router imported successfully")
    except ImportError as e:
        print(f"❌ API router import failed: {e}")
        return False
    
    return True

def test_database_creation():
    """Test database table creation"""
    print("\n🧪 Testing database creation...")
    
    try:
        from app.core.database import engine, Base
        from app.models.user import User
        from app.models.music import Track, Playlist
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Database creation failed: {e}")
        return False

def test_fastapi_app():
    """Test FastAPI app creation"""
    print("\n🧪 Testing FastAPI app creation...")
    
    try:
        from fastapi import FastAPI
        from app.api.v1.api import api_router
        
        app = FastAPI(title="ChordCircle API Test")
        app.include_router(api_router, prefix="/api/v1")
        
        print("✅ FastAPI app created successfully")
        print(f"   Routes: {len(app.routes)} routes registered")
        return True
    except Exception as e:
        print(f"❌ FastAPI app creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🎵 ChordCircle Backend Test Suite")
    print("=" * 50)
    
    tests = [
        ("Core Dependencies", test_imports),
        ("App Modules", test_app_imports),
        ("Database Creation", test_database_creation),
        ("FastAPI App", test_fastapi_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready to start.")
        return True
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)