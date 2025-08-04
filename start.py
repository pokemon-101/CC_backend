#!/usr/bin/env python3
"""
ChordCircle Backend Startup Script
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        print("✅ Core dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def install_dependencies():
    """Install dependencies from requirements.txt"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def setup_environment():
    """Setup environment file if it doesn't exist"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print("🔧 Creating .env file from template...")
        env_file.write_text(env_example.read_text())
        print("✅ .env file created. Please update it with your configuration.")
        return True
    elif env_file.exists():
        print("✅ .env file found")
        return True
    else:
        print("⚠️  No .env file found. Creating basic configuration...")
        basic_env = """DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///./chordcircle.db
ALLOWED_HOSTS=["http://localhost:3000", "http://127.0.0.1:3000"]
"""
        env_file.write_text(basic_env)
        print("✅ Basic .env file created")
        return True

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting ChordCircle API server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

def main():
    """Main startup function"""
    print("🎵 ChordCircle Backend API")
    print("=" * 30)
    
    # Check Python version
    check_python_version()
    
    # Setup environment
    setup_environment()
    
    # Check and install dependencies
    if not check_dependencies():
        if not install_dependencies():
            sys.exit(1)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()