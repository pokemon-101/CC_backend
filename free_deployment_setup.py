#!/usr/bin/env python3
"""
FREE Deployment Setup for ChordCircle
Configures your app for 100% free hosting
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def print_header(title):
    print("\n" + "="*60)
    print(f"  💰 {title}")
    print("="*60)

def check_git_setup():
    """Check if project is set up with Git"""
    print_header("CHECKING GIT SETUP")
    
    if not Path(".git").exists():
        print("❌ Git repository not initialized")
        print("🔧 Initializing Git repository...")
        
        try:
            subprocess.run(['git', 'init'], check=True)
            subprocess.run(['git', 'add', '.'], check=True)
            subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
            print("✅ Git repository initialized")
        except subprocess.CalledProcessError:
            print("❌ Failed to initialize Git")
            return False
    else:
        print("✅ Git repository found")
    
    # Check if connected to GitHub
    try:
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Connected to: {result.stdout.strip()}")
        else:
            print("⚠️  No GitHub remote found")
            print("📋 To connect to GitHub:")
            print("   1. Create repository on GitHub")
            print("   2. git remote add origin https://github.com/username/chordcircle.git")
            print("   3. git push -u origin main")
    except:
        pass
    
    return True

def optimize_for_free_tier():
    """Optimize application for free tier limits"""
    print_header("OPTIMIZING FOR FREE TIER")
    
    # Create optimized requirements.txt for faster builds
    optimized_requirements = """fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
python-jose[cryptography]==3.5.0
passlib[bcrypt]==1.7.4
sqlalchemy==2.0.42
requests==2.31.0
pydantic-settings==2.10.1
email-validator==2.2.0
PyJWT==2.10.1
psycopg2-binary==2.9.9
"""
    
    with open("requirements_optimized.txt", "w") as f:
        f.write(optimized_requirements)
    
    print("✅ Created optimized requirements.txt")
    
    # Create Render deployment script
    render_start_script = """#!/bin/bash
# Render.com startup script for ChordCircle

echo "🎵 Starting ChordCircle Backend..."

# Install dependencies
pip install -r requirements_optimized.txt

# Create database tables
python -c "
try:
    from app.core.database import Base, engine
    Base.metadata.create_all(bind=engine)
    print('✅ Database tables created')
except Exception as e:
    print(f'⚠️  Database setup: {e}')
"

# Start the server
python start.py
"""
    
    with open("render_start.sh", "w") as f:
        f.write(render_start_script)
    
    os.chmod("render_start.sh", 0o755)
    print("✅ Created Render startup script")
    
    # Create keep-alive service to prevent sleeping
    keep_alive_code = '''import requests
import threading
import time
import os

def keep_alive():
    """Keep Render service awake by pinging health endpoint"""
    service_url = os.getenv("RENDER_EXTERNAL_URL")
    if not service_url:
        return
    
    health_url = f"{service_url}/health"
    
    while True:
        try:
            response = requests.get(health_url, timeout=10)
            if response.status_code == 200:
                print("🔄 Keep-alive ping successful")
            else:
                print(f"⚠️  Keep-alive ping failed: {response.status_code}")
        except Exception as e:
            print(f"⚠️  Keep-alive error: {e}")
        
        # Wait 10 minutes before next ping
        time.sleep(600)

# Start keep-alive in background thread
if os.getenv("RENDER_EXTERNAL_URL"):
    keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()
    print("🔄 Keep-alive service started")
'''
    
    keep_alive_file = Path("app/utils/keep_alive.py")
    keep_alive_file.parent.mkdir(exist_ok=True)
    with open(keep_alive_file, "w") as f:
        f.write(keep_alive_code)
    
    print("✅ Created keep-alive service")
    
    return True

def create_deployment_configs():
    """Create configuration files for free hosting services"""
    print_header("CREATING DEPLOYMENT CONFIGS")
    
    # Vercel configuration for frontend
    vercel_config = {
        "builds": [
            {
                "src": "package.json",
                "use": "@vercel/static-build"
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "/index.html"
            }
        ]
    }
    
    frontend_dir = Path("..").resolve()
    vercel_file = frontend_dir / "vercel.json"
    
    with open(vercel_file, "w") as f:
        json.dump(vercel_config, f, indent=2)
    
    print("✅ Created vercel.json for frontend")
    
    # Render configuration
    render_config = """# Render.com configuration for ChordCircle Backend

# Build Command: pip install -r requirements_optimized.txt
# Start Command: ./render_start.sh

# Environment Variables needed:
# DATABASE_URL=postgresql://...
# SECRET_KEY=your-secret-key
# DEBUG=False
# ALLOWED_HOSTS=["https://chordcircle.vercel.app"]
"""
    
    with open("render.yaml", "w") as f:
        f.write(render_config)
    
    print("✅ Created render.yaml configuration")
    
    # Netlify configuration (alternative)
    netlify_config = """[build]
  publish = "build"
  command = "npm run build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  REACT_APP_API_URL = "https://chordcircle-backend.onrender.com/api/v1"
"""
    
    netlify_file = frontend_dir / "netlify.toml"
    with open(netlify_file, "w") as f:
        f.write(netlify_config)
    
    print("✅ Created netlify.toml (alternative)")
    
    return True

def create_environment_templates():
    """Create environment variable templates"""
    print_header("CREATING ENVIRONMENT TEMPLATES")
    
    # Backend environment template
    backend_env_template = """# ChordCircle Backend Environment Variables for FREE Deployment

# Database (Supabase FREE)
DATABASE_URL=postgresql://postgres:PASSWORD@db.PROJECT.supabase.co:5432/postgres

# Security
SECRET_KEY=your-super-secret-key-change-this
DEBUG=False
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (Update with your Vercel URL)
ALLOWED_HOSTS=["https://chordcircle.vercel.app", "https://your-custom-domain.com"]

# Music APIs (Optional - add when ready)
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
SPOTIFY_REDIRECT_URI=https://chordcircle-backend.onrender.com/api/v1/auth/spotify/callback

APPLE_MUSIC_TEAM_ID=
APPLE_MUSIC_KEY_ID=
APPLE_MUSIC_PRIVATE_KEY=

# Render.com specific
RENDER_EXTERNAL_URL=https://chordcircle-backend.onrender.com
"""
    
    with open(".env.production", "w") as f:
        f.write(backend_env_template)
    
    print("✅ Created .env.production template")
    
    # Frontend environment template
    frontend_env_template = """# ChordCircle Frontend Environment Variables

# API Configuration
REACT_APP_API_URL=https://chordcircle-backend.onrender.com/api/v1

# Supabase Configuration (FREE)
REACT_APP_SUPABASE_URL=https://PROJECT.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your-anon-key

# App Configuration
REACT_APP_NAME=ChordCircle
REACT_APP_VERSION=1.0.0
"""
    
    frontend_dir = Path("..").resolve()
    frontend_env_file = frontend_dir / ".env.production"
    
    with open(frontend_env_file, "w") as f:
        f.write(frontend_env_template)
    
    print("✅ Created frontend .env.production template")
    
    return True

def create_deployment_guide():
    """Create step-by-step deployment guide"""
    print_header("CREATING DEPLOYMENT GUIDE")
    
    deployment_steps = """# 🚀 ChordCircle FREE Deployment Steps

## 📋 Prerequisites
- GitHub account (free)
- Vercel account (free) 
- Render account (free)
- Supabase account (free)

## Step 1: Setup Supabase Database (FREE)
1. Go to https://supabase.com
2. Sign up with GitHub
3. Create new project: "chordcircle"
4. Choose strong password
5. Wait 2 minutes for setup
6. Go to Settings → Database
7. Copy connection string
8. Save for Step 3

## Step 2: Deploy Frontend to Vercel (FREE)
1. Install Vercel CLI: `npm install -g vercel`
2. In project root: `vercel`
3. Connect to GitHub repository
4. Deploy automatically
5. Add environment variables in dashboard:
   - REACT_APP_API_URL=https://chordcircle-backend.onrender.com/api/v1
   - REACT_APP_SUPABASE_URL=(from Supabase)
   - REACT_APP_SUPABASE_ANON_KEY=(from Supabase)

## Step 3: Deploy Backend to Render (FREE)
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect GitHub repository
5. Configure:
   - Name: chordcircle-backend
   - Environment: Python 3
   - Build Command: pip install -r requirements_optimized.txt
   - Start Command: ./render_start.sh
6. Add environment variables:
   - DATABASE_URL=(from Supabase)
   - SECRET_KEY=(generate random string)
   - DEBUG=False
   - ALLOWED_HOSTS=["https://chordcircle.vercel.app"]

## Step 4: Test Your Live App
1. Frontend: https://chordcircle.vercel.app
2. Backend: https://chordcircle-backend.onrender.com
3. API Docs: https://chordcircle-backend.onrender.com/docs

## 🎉 You're Live!
Your ChordCircle music app is now running 100% FREE on professional infrastructure!

## 📈 Scaling Path
- Start: FREE (perfect for demos/portfolio)
- Growth: $5/month (when you need more resources)
- Scale: $20/month (thousands of users)
"""
    
    with open("DEPLOYMENT_STEPS.md", "w") as f:
        f.write(deployment_steps)
    
    print("✅ Created DEPLOYMENT_STEPS.md")
    
    return True

def show_free_tier_limits():
    """Show what you get with free tiers"""
    print_header("FREE TIER BENEFITS")
    
    print("🎉 What you get for FREE:")
    print("\n📱 Frontend (Vercel):")
    print("   ✅ Unlimited deployments")
    print("   ✅ 100GB bandwidth/month")
    print("   ✅ Custom domain support")
    print("   ✅ Automatic HTTPS")
    print("   ✅ Global CDN")
    
    print("\n🖥️  Backend (Render):")
    print("   ✅ 750 hours/month (24/7 uptime)")
    print("   ✅ 512MB RAM")
    print("   ✅ Custom domain")
    print("   ✅ Auto-deploy from Git")
    print("   ✅ HTTPS included")
    
    print("\n🗄️  Database (Supabase):")
    print("   ✅ 500MB PostgreSQL database")
    print("   ✅ 2GB bandwidth/month")
    print("   ✅ Real-time subscriptions")
    print("   ✅ Built-in authentication")
    print("   ✅ 50MB file storage")
    
    print("\n🎵 Perfect for Music Apps:")
    print("   ✅ Real-time playlist sync")
    print("   ✅ User authentication")
    print("   ✅ Music search & discovery")
    print("   ✅ Social features (friends)")
    print("   ✅ Professional deployment")
    
    print("\n📊 Estimated Capacity:")
    print("   👥 100-500 active users")
    print("   🎵 10,000+ tracks in database")
    print("   📱 Unlimited playlist syncs")
    print("   🌍 Global availability")

def main():
    """Main setup function"""
    print_header("CHORDCIRCLE FREE DEPLOYMENT SETUP")
    print("Configure your app for 100% FREE professional hosting!")
    
    steps = [
        ("Git Setup", check_git_setup),
        ("Free Tier Optimization", optimize_for_free_tier),
        ("Deployment Configs", create_deployment_configs),
        ("Environment Templates", create_environment_templates),
        ("Deployment Guide", create_deployment_guide)
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}")
        print("-" * 40)
        if not step_func():
            print(f"❌ {step_name} failed")
            return False
    
    # Show what they get for free
    show_free_tier_limits()
    
    print_header("SETUP COMPLETE!")
    
    print("🎉 Your ChordCircle is ready for FREE deployment!")
    
    print("\n📋 Files created:")
    print("   ✅ requirements_optimized.txt - Faster builds")
    print("   ✅ render_start.sh - Render deployment script")
    print("   ✅ vercel.json - Vercel configuration")
    print("   ✅ .env.production - Environment templates")
    print("   ✅ DEPLOYMENT_STEPS.md - Step-by-step guide")
    
    print("\n🚀 Next steps:")
    print("   1. Read DEPLOYMENT_STEPS.md")
    print("   2. Create Supabase account")
    print("   3. Deploy frontend to Vercel")
    print("   4. Deploy backend to Render")
    print("   5. Enjoy your FREE music app!")
    
    print("\n🌐 Your app will be live at:")
    print("   Frontend: https://chordcircle.vercel.app")
    print("   Backend: https://chordcircle-backend.onrender.com")
    print("   API Docs: https://chordcircle-backend.onrender.com/docs")
    
    print("\n💰 Total cost: $0/month")
    print("🎵 Perfect for portfolio, demos, and real users!")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)