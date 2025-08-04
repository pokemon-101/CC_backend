#!/usr/bin/env python3
"""
ChordCircle Music APIs Setup Script
Helps configure Spotify and Apple Music API credentials
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any

def print_header(title: str):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_step(step: str, description: str):
    """Print a formatted step"""
    print(f"\n🔧 {step}")
    print(f"   {description}")

def get_user_input(prompt: str, required: bool = True) -> str:
    """Get user input with validation"""
    while True:
        value = input(f"{prompt}: ").strip()
        if value or not required:
            return value
        print("   ❌ This field is required. Please try again.")

def validate_spotify_credentials(client_id: str, client_secret: str) -> bool:
    """Validate Spotify credentials by making a test request"""
    try:
        import requests
        import base64
        
        auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {"grant_type": "client_credentials"}
        
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers=headers,
            data=data,
            timeout=10
        )
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"   ⚠️  Could not validate credentials: {e}")
        return False

def setup_spotify():
    """Setup Spotify API credentials"""
    print_header("SPOTIFY API SETUP")
    
    print("""
🎵 To set up Spotify API integration:

1. Go to: https://developer.spotify.com/dashboard
2. Log in with your Spotify account
3. Click "Create App"
4. Fill in the details:
   - App Name: ChordCircle
   - App Description: Music platform integration
   - Website: http://localhost:3000
   - Redirect URI: http://localhost:8000/api/v1/auth/spotify/callback
5. Save the app and get your Client ID and Client Secret
    """)
    
    client_id = get_user_input("Enter your Spotify Client ID")
    client_secret = get_user_input("Enter your Spotify Client Secret")
    
    print("\n🔍 Validating Spotify credentials...")
    if validate_spotify_credentials(client_id, client_secret):
        print("   ✅ Spotify credentials are valid!")
    else:
        print("   ⚠️  Could not validate credentials. Please double-check them.")
    
    return {
        "SPOTIFY_CLIENT_ID": client_id,
        "SPOTIFY_CLIENT_SECRET": client_secret,
        "SPOTIFY_REDIRECT_URI": "http://localhost:8000/api/v1/auth/spotify/callback"
    }

def setup_apple_music():
    """Setup Apple Music API credentials"""
    print_header("APPLE MUSIC API SETUP")
    
    print("""
🍎 To set up Apple Music API integration:

1. Join Apple Developer Program ($99/year): https://developer.apple.com/programs/
2. Go to: https://developer.apple.com/account/
3. Navigate to "Certificates, Identifiers & Profiles"
4. Create a new Service ID with MusicKit enabled
5. Create a new Key with MusicKit enabled
6. Download the .p8 private key file (you can only do this once!)
7. Note your Team ID (top-right corner of developer portal)
8. Note your Key ID (from the key you created)
    """)
    
    has_apple_dev = get_user_input("Do you have an Apple Developer account? (y/n)", required=False).lower()
    
    if has_apple_dev != 'y':
        print("\n⚠️  Apple Music API requires an Apple Developer Program membership.")
        print("   You can skip this for now and set it up later.")
        skip = get_user_input("Skip Apple Music setup? (y/n)", required=False).lower()
        if skip == 'y':
            return {}
    
    team_id = get_user_input("Enter your Apple Music Team ID")
    key_id = get_user_input("Enter your Apple Music Key ID")
    
    print("\n📁 For the private key, you have two options:")
    print("   1. Paste the key content directly")
    print("   2. Provide the path to your .p8 file")
    
    key_option = get_user_input("Choose option (1 or 2)", required=False) or "1"
    
    if key_option == "2":
        key_path = get_user_input("Enter path to your .p8 file")
        if not Path(key_path).exists():
            print(f"   ❌ File not found: {key_path}")
            return {}
        
        return {
            "APPLE_MUSIC_TEAM_ID": team_id,
            "APPLE_MUSIC_KEY_ID": key_id,
            "APPLE_MUSIC_PRIVATE_KEY_PATH": key_path
        }
    else:
        print("\n📝 Paste your private key content (including -----BEGIN PRIVATE KEY----- and -----END PRIVATE KEY-----):")
        print("   Press Enter twice when done:")
        
        key_lines = []
        while True:
            line = input()
            if not line and key_lines:
                break
            key_lines.append(line)
        
        private_key = "\n".join(key_lines)
        
        if "BEGIN PRIVATE KEY" not in private_key:
            print("   ⚠️  Private key format may be incorrect.")
        
        return {
            "APPLE_MUSIC_TEAM_ID": team_id,
            "APPLE_MUSIC_KEY_ID": key_id,
            "APPLE_MUSIC_PRIVATE_KEY": private_key
        }

def update_env_file(credentials: Dict[str, str]):
    """Update the .env file with new credentials"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    # Read existing .env or create from example
    if env_file.exists():
        with open(env_file, 'r') as f:
            lines = f.readlines()
    elif env_example.exists():
        with open(env_example, 'r') as f:
            lines = f.readlines()
    else:
        lines = []
    
    # Update or add credentials
    updated_lines = []
    keys_added = set()
    
    for line in lines:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            key = line.split('=')[0]
            if key in credentials:
                updated_lines.append(f"{key}={credentials[key]}\n")
                keys_added.add(key)
            else:
                updated_lines.append(line + '\n')
        else:
            updated_lines.append(line + '\n')
    
    # Add any missing keys
    for key, value in credentials.items():
        if key not in keys_added:
            updated_lines.append(f"{key}={value}\n")
    
    # Write updated .env file
    with open(env_file, 'w') as f:
        f.writelines(updated_lines)
    
    print(f"\n✅ Updated {env_file}")

def test_configuration():
    """Test the API configuration"""
    print_header("TESTING CONFIGURATION")
    
    try:
        # Import and test services
        sys.path.append(str(Path(__file__).parent))
        
        from app.services.spotify import SpotifyService
        from app.services.apple_music import AppleMusicService
        
        print("\n🧪 Testing Spotify service...")
        try:
            spotify = SpotifyService()
            auth_url = spotify.get_auth_url()
            print("   ✅ Spotify service initialized successfully")
            print(f"   🔗 Auth URL: {auth_url[:50]}...")
        except Exception as e:
            print(f"   ❌ Spotify service error: {e}")
        
        print("\n🧪 Testing Apple Music service...")
        try:
            apple = AppleMusicService()
            token = apple.generate_developer_token()
            print("   ✅ Apple Music service initialized successfully")
            print(f"   🔑 Developer token generated: {token[:20]}...")
        except Exception as e:
            print(f"   ❌ Apple Music service error: {e}")
            
    except ImportError as e:
        print(f"   ⚠️  Could not import services: {e}")
        print("   Make sure you've installed the requirements: pip install -r requirements.txt")

def main():
    """Main setup function"""
    print_header("CHORDCIRCLE MUSIC APIS SETUP")
    
    print("""
🎵 Welcome to ChordCircle Music APIs Setup!

This script will help you configure:
- Spotify Web API integration
- Apple Music API integration

Make sure you have the necessary developer accounts before proceeding.
    """)
    
    proceed = get_user_input("Do you want to continue? (y/n)", required=False).lower()
    if proceed != 'y':
        print("Setup cancelled.")
        return
    
    all_credentials = {}
    
    # Setup Spotify
    setup_spotify_choice = get_user_input("Set up Spotify API? (y/n)", required=False).lower()
    if setup_spotify_choice == 'y':
        spotify_creds = setup_spotify()
        all_credentials.update(spotify_creds)
    
    # Setup Apple Music
    setup_apple_choice = get_user_input("Set up Apple Music API? (y/n)", required=False).lower()
    if setup_apple_choice == 'y':
        apple_creds = setup_apple_music()
        all_credentials.update(apple_creds)
    
    if all_credentials:
        print_header("SAVING CONFIGURATION")
        update_env_file(all_credentials)
        
        # Test configuration
        test_config = get_user_input("Test the configuration? (y/n)", required=False).lower()
        if test_config == 'y':
            test_configuration()
    
    print_header("SETUP COMPLETE")
    print("""
🎉 Setup complete!

Next steps:
1. Start your backend server: python start.py
2. Start your frontend: npm run dev
3. Test the music account linking in your app

For detailed setup instructions, see:
- SPOTIFY_SETUP.md
- APPLE_MUSIC_SETUP.md
    """)

if __name__ == "__main__":
    main()