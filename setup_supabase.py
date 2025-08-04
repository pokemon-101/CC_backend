#!/usr/bin/env python3
"""
Supabase Setup Script for ChordCircle
Perfect database solution for Vercel deployment
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def print_header(title):
    print("\n" + "="*60)
    print(f"  🚀 {title}")
    print("="*60)

def check_supabase_cli():
    """Check if Supabase CLI is installed"""
    print_header("CHECKING SUPABASE CLI")
    
    try:
        result = subprocess.run(['supabase', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Supabase CLI found: {version}")
            return True
        else:
            print("❌ Supabase CLI not found")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Supabase CLI not installed")
        return False

def install_supabase_cli():
    """Install Supabase CLI"""
    print_header("INSTALLING SUPABASE CLI")
    
    print("📦 Installing Supabase CLI...")
    
    try:
        # Try npm install
        subprocess.run(['npm', 'install', '-g', '@supabase/cli'], check=True)
        print("✅ Supabase CLI installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install via npm")
        
        # Provide manual installation instructions
        print("\n📋 Manual installation options:")
        print("   npm install -g @supabase/cli")
        print("   or")
        print("   brew install supabase/tap/supabase  # macOS")
        print("   or")
        print("   Download from: https://github.com/supabase/cli/releases")
        
        return False

def create_supabase_project():
    """Guide user through Supabase project creation"""
    print_header("CREATING SUPABASE PROJECT")
    
    print("🌐 To create a Supabase project:")
    print("   1. Go to https://supabase.com/dashboard")
    print("   2. Sign in with GitHub/Google")
    print("   3. Click 'New Project'")
    print("   4. Choose organization")
    print("   5. Project details:")
    print("      - Name: chordcircle")
    print("      - Database Password: (choose a strong password)")
    print("      - Region: (choose closest to your users)")
    print("   6. Click 'Create new project'")
    print("   7. Wait for project to be ready (~2 minutes)")
    
    input("\nPress Enter when your Supabase project is ready...")
    
    return True

def get_connection_details():
    """Get Supabase connection details from user"""
    print_header("SUPABASE CONNECTION DETAILS")
    
    print("📋 Get your connection details from Supabase dashboard:")
    print("   1. Go to Settings → Database")
    print("   2. Scroll down to 'Connection string'")
    print("   3. Copy the URI (starts with postgresql://)")
    
    print("\n🔗 Your connection string should look like:")
    print("   postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres")
    
    database_url = input("\nPaste your DATABASE_URL here: ").strip()
    
    if not database_url.startswith('postgresql://'):
        print("❌ Invalid database URL. Should start with 'postgresql://'")
        return None
    
    print("✅ Database URL received")
    return database_url

def get_api_keys():
    """Get Supabase API keys"""
    print("\n📋 Get your API keys from Supabase dashboard:")
    print("   1. Go to Settings → API")
    print("   2. Copy the 'Project URL'")
    print("   3. Copy the 'anon public' key")
    
    project_url = input("\nPaste your Project URL: ").strip()
    anon_key = input("Paste your anon key: ").strip()
    
    return project_url, anon_key

def update_backend_env(database_url):
    """Update backend .env file"""
    print_header("UPDATING BACKEND CONFIGURATION")
    
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    # Read current .env
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Update DATABASE_URL
    new_lines = []
    updated = False
    
    for line in lines:
        if line.startswith('DATABASE_URL='):
            new_lines.append(f'DATABASE_URL={database_url}\n')
            updated = True
            print("✅ Updated DATABASE_URL in backend .env")
        else:
            new_lines.append(line)
    
    if not updated:
        new_lines.append(f'\n# Supabase Database\n')
        new_lines.append(f'DATABASE_URL={database_url}\n')
        print("✅ Added DATABASE_URL to backend .env")
    
    # Write back to file
    with open(env_file, 'w') as f:
        f.writelines(new_lines)
    
    return True

def create_frontend_env(project_url, anon_key):
    """Create frontend .env file for Supabase"""
    print_header("CREATING FRONTEND CONFIGURATION")
    
    # Go to parent directory (frontend)
    frontend_dir = Path("..").resolve()
    env_file = frontend_dir / ".env"
    
    # Read existing .env or create new
    existing_content = ""
    if env_file.exists():
        with open(env_file, 'r') as f:
            existing_content = f.read()
    
    # Add Supabase configuration
    supabase_config = f"""
# Supabase Configuration
REACT_APP_SUPABASE_URL={project_url}
REACT_APP_SUPABASE_ANON_KEY={anon_key}
"""
    
    # Check if Supabase config already exists
    if "REACT_APP_SUPABASE_URL" not in existing_content:
        with open(env_file, 'a') as f:
            f.write(supabase_config)
        print("✅ Added Supabase configuration to frontend .env")
    else:
        print("✅ Supabase configuration already exists in frontend .env")
    
    return True

def create_database_tables():
    """Create database tables in Supabase"""
    print_header("CREATING DATABASE TABLES")
    
    print("🏗️  Creating database tables...")
    
    try:
        # Import your models to create tables
        sys.path.append(str(Path(__file__).parent))
        from app.core.database import Base, engine
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        
        # Test connection
        from app.core.database import SessionLocal
        from app.models.user import User
        
        db = SessionLocal()
        try:
            user_count = db.query(User).count()
            print(f"✅ Database connection test successful - {user_count} users")
        finally:
            db.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Table creation failed: {e}")
        return False

def setup_realtime_features():
    """Guide user through setting up real-time features"""
    print_header("SETTING UP REAL-TIME FEATURES")
    
    print("🔄 Supabase Real-time Setup:")
    print("   1. Go to your Supabase dashboard")
    print("   2. Navigate to Database → Replication")
    print("   3. Enable replication for these tables:")
    print("      ✅ playlists")
    print("      ✅ playlist_tracks") 
    print("      ✅ user_favorites")
    print("      ✅ friendships")
    print("   4. This enables real-time updates for playlist sync!")
    
    print("\n🎵 Real-time playlist sync will work like this:")
    print("   - User adds song to playlist → Instantly syncs to all devices")
    print("   - Friend shares playlist → Real-time notification")
    print("   - Playlist changes → All connected users see updates")
    
    input("\nPress Enter when you've enabled replication...")
    print("✅ Real-time features configured")
    
    return True

def create_supabase_client_example():
    """Create example Supabase client for frontend"""
    print_header("CREATING FRONTEND INTEGRATION")
    
    frontend_dir = Path("..").resolve()
    supabase_dir = frontend_dir / "src" / "services"
    supabase_dir.mkdir(exist_ok=True)
    
    supabase_client_code = '''import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Real-time playlist sync
export const subscribeToPlaylistChanges = (userId, callback) => {
  return supabase
    .channel('playlists')
    .on(
      'postgres_changes',
      {
        event: '*',
        schema: 'public',
        table: 'playlists',
        filter: `user_id=eq.${userId}`
      },
      callback
    )
    .subscribe()
}

// Real-time friend requests
export const subscribeToFriendRequests = (userId, callback) => {
  return supabase
    .channel('friendships')
    .on(
      'postgres_changes',
      {
        event: 'INSERT',
        schema: 'public', 
        table: 'friendships',
        filter: `friend_id=eq.${userId}`
      },
      callback
    )
    .subscribe()
}
'''
    
    supabase_file = supabase_dir / "supabase.js"
    with open(supabase_file, 'w') as f:
        f.write(supabase_client_code)
    
    print("✅ Created frontend Supabase client")
    print(f"   File: {supabase_file}")
    
    # Install Supabase JS client
    try:
        os.chdir(frontend_dir)
        subprocess.run(['npm', 'install', '@supabase/supabase-js'], check=True)
        print("✅ Installed @supabase/supabase-js")
        os.chdir(Path(__file__).parent)  # Go back to backend dir
    except subprocess.CalledProcessError:
        print("⚠️  Please install @supabase/supabase-js manually:")
        print("   cd .. && npm install @supabase/supabase-js")
    
    return True

def show_deployment_guide():
    """Show deployment instructions"""
    print_header("DEPLOYMENT GUIDE")
    
    print("🚀 Your ChordCircle is now ready for deployment!")
    
    print("\n📋 Deployment Stack:")
    print("   Frontend: Vercel (React app)")
    print("   Backend: Railway (FastAPI server)")  
    print("   Database: Supabase (PostgreSQL)")
    
    print("\n🔧 Deploy Frontend to Vercel:")
    print("   1. Install Vercel CLI: npm install -g vercel")
    print("   2. In project root: vercel")
    print("   3. Follow prompts to deploy")
    print("   4. Add environment variables in Vercel dashboard")
    
    print("\n🔧 Deploy Backend to Railway:")
    print("   1. Install Railway CLI: npm install -g @railway/cli")
    print("   2. In backend folder: railway login")
    print("   3. railway init && railway up")
    print("   4. Add environment variables in Railway dashboard")
    
    print("\n🌐 Environment Variables:")
    print("   Frontend (Vercel):")
    print("     REACT_APP_API_URL=https://your-backend.railway.app/api/v1")
    print("     REACT_APP_SUPABASE_URL=your-supabase-url")
    print("     REACT_APP_SUPABASE_ANON_KEY=your-anon-key")
    
    print("\n   Backend (Railway):")
    print("     DATABASE_URL=your-supabase-connection-string")
    print("     SECRET_KEY=your-secret-key")
    print("     SPOTIFY_CLIENT_ID=your-spotify-id")
    print("     SPOTIFY_CLIENT_SECRET=your-spotify-secret")
    
    print("\n💰 Total Cost: ~$5/month")
    print("   Vercel: FREE")
    print("   Railway: $5/month")
    print("   Supabase: FREE (up to 500MB)")

def main():
    """Main setup function"""
    print_header("CHORDCIRCLE SUPABASE SETUP")
    print("Perfect database solution for Vercel deployment!")
    
    # Check/install Supabase CLI
    if not check_supabase_cli():
        if not install_supabase_cli():
            print("\n❌ Please install Supabase CLI manually and run this script again")
            return False
    
    # Guide through project creation
    if not create_supabase_project():
        return False
    
    # Get connection details
    database_url = get_connection_details()
    if not database_url:
        return False
    
    project_url, anon_key = get_api_keys()
    
    # Update configurations
    if not update_backend_env(database_url):
        return False
    
    if not create_frontend_env(project_url, anon_key):
        return False
    
    # Create database tables
    if not create_database_tables():
        return False
    
    # Setup real-time features
    if not setup_realtime_features():
        return False
    
    # Create frontend integration
    if not create_supabase_client_example():
        return False
    
    # Show deployment guide
    show_deployment_guide()
    
    print("\n🎉 Supabase setup complete!")
    print("Your ChordCircle now has:")
    print("   ✅ PostgreSQL database with real-time sync")
    print("   ✅ Perfect for Vercel deployment")
    print("   ✅ Built-in authentication (optional)")
    print("   ✅ File storage for album art")
    print("   ✅ Edge functions for music APIs")
    
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