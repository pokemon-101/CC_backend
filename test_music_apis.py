#!/usr/bin/env python3
"""
ChordCircle Music APIs Test Script
Tests Spotify and Apple Music API integrations
"""

import asyncio
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

from app.services.spotify import SpotifyService
from app.services.apple_music import AppleMusicService
from app.core.config import settings

def print_header(title: str):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_test(test_name: str, success: bool, details: str = ""):
    """Print test result"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} {test_name}")
    if details:
        print(f"    {details}")

async def test_spotify_service():
    """Test Spotify service functionality"""
    print_header("TESTING SPOTIFY SERVICE")
    
    try:
        spotify = SpotifyService()
        print_test("Spotify Service Initialization", True, "Service created successfully")
        
        # Test auth URL generation
        try:
            auth_url = spotify.get_auth_url()
            print_test("Auth URL Generation", True, f"URL: {auth_url[:50]}...")
        except Exception as e:
            print_test("Auth URL Generation", False, str(e))
        
        # Test credentials validation (if available)
        if settings.SPOTIFY_CLIENT_ID and settings.SPOTIFY_CLIENT_SECRET:
            try:
                # This would require actual API call - simplified for testing
                print_test("Credentials Configuration", True, "Client ID and Secret are set")
            except Exception as e:
                print_test("Credentials Configuration", False, str(e))
        else:
            print_test("Credentials Configuration", False, "Missing Client ID or Secret")
            
    except Exception as e:
        print_test("Spotify Service Initialization", False, str(e))

async def test_apple_music_service():
    """Test Apple Music service functionality"""
    print_header("TESTING APPLE MUSIC SERVICE")
    
    try:
        apple = AppleMusicService()
        print_test("Apple Music Service Initialization", True, "Service created successfully")
        
        # Test developer token generation
        try:
            token = apple.generate_developer_token()
            print_test("Developer Token Generation", True, f"Token: {token[:20]}...")
            
            # Test token caching
            token2 = apple.generate_developer_token()
            is_cached = token == token2
            print_test("Token Caching", is_cached, "Same token returned" if is_cached else "New token generated")
            
        except Exception as e:
            print_test("Developer Token Generation", False, str(e))
        
        # Test configuration
        if all([settings.APPLE_MUSIC_TEAM_ID, settings.APPLE_MUSIC_KEY_ID, settings.APPLE_MUSIC_PRIVATE_KEY]):
            print_test("Apple Music Configuration", True, "All required settings are present")
        else:
            missing = []
            if not settings.APPLE_MUSIC_TEAM_ID:
                missing.append("TEAM_ID")
            if not settings.APPLE_MUSIC_KEY_ID:
                missing.append("KEY_ID")
            if not settings.APPLE_MUSIC_PRIVATE_KEY:
                missing.append("PRIVATE_KEY")
            print_test("Apple Music Configuration", False, f"Missing: {', '.join(missing)}")
            
    except Exception as e:
        print_test("Apple Music Service Initialization", False, str(e))

async def test_api_endpoints():
    """Test API endpoints"""
    print_header("TESTING API ENDPOINTS")
    
    try:
        import requests
        base_url = "http://localhost:8000"
        
        # Test health endpoint
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            print_test("Health Endpoint", response.status_code == 200, f"Status: {response.status_code}")
        except Exception as e:
            print_test("Health Endpoint", False, f"Connection failed: {e}")
        
        # Test API root
        try:
            response = requests.get(f"{base_url}/api/v1", timeout=5)
            # This might return 404, but connection should work
            print_test("API Root Connection", True, f"Server responded with status: {response.status_code}")
        except Exception as e:
            print_test("API Root Connection", False, f"Connection failed: {e}")
            
    except ImportError:
        print_test("API Endpoints", False, "requests library not available")

def test_environment_configuration():
    """Test environment configuration"""
    print_header("TESTING ENVIRONMENT CONFIGURATION")
    
    # Test database URL
    print_test("Database URL", bool(settings.DATABASE_URL), settings.DATABASE_URL)
    
    # Test secret key
    print_test("Secret Key", bool(settings.SECRET_KEY), "Secret key is set" if settings.SECRET_KEY else "Not set")
    
    # Test CORS settings
    print_test("CORS Settings", bool(settings.ALLOWED_HOSTS), f"Allowed hosts: {settings.ALLOWED_HOSTS}")
    
    # Test Spotify settings
    spotify_configured = bool(settings.SPOTIFY_CLIENT_ID and settings.SPOTIFY_CLIENT_SECRET)
    print_test("Spotify Configuration", spotify_configured, 
              "Client ID and Secret configured" if spotify_configured else "Missing credentials")
    
    # Test Apple Music settings
    apple_configured = bool(settings.APPLE_MUSIC_TEAM_ID and settings.APPLE_MUSIC_KEY_ID and settings.APPLE_MUSIC_PRIVATE_KEY)
    print_test("Apple Music Configuration", apple_configured,
              "Team ID, Key ID, and Private Key configured" if apple_configured else "Missing credentials")

async def run_integration_tests():
    """Run integration tests with actual API calls"""
    print_header("INTEGRATION TESTS")
    
    # These tests would require actual API credentials and user tokens
    # For now, we'll just test the service methods that don't require authentication
    
    try:
        spotify = SpotifyService()
        
        # Test search (requires client credentials)
        # This would need actual implementation with client credentials flow
        print_test("Spotify Search Test", False, "Requires client credentials - implement if needed")
        
    except Exception as e:
        print_test("Spotify Integration", False, str(e))
    
    try:
        apple = AppleMusicService()
        
        # Test catalog search (requires developer token)
        # This would need actual API call
        print_test("Apple Music Catalog Test", False, "Requires API call - implement if needed")
        
    except Exception as e:
        print_test("Apple Music Integration", False, str(e))

def print_recommendations():
    """Print recommendations based on test results"""
    print_header("RECOMMENDATIONS")
    
    recommendations = []
    
    if not (settings.SPOTIFY_CLIENT_ID and settings.SPOTIFY_CLIENT_SECRET):
        recommendations.append("🎵 Set up Spotify API credentials (see SPOTIFY_SETUP.md)")
    
    if not (settings.APPLE_MUSIC_TEAM_ID and settings.APPLE_MUSIC_KEY_ID and settings.APPLE_MUSIC_PRIVATE_KEY):
        recommendations.append("🍎 Set up Apple Music API credentials (see APPLE_MUSIC_SETUP.md)")
    
    if not recommendations:
        recommendations.append("🎉 All APIs are configured! You can start testing the full integration.")
    
    for rec in recommendations:
        print(f"  {rec}")
    
    print("\n📚 Next Steps:")
    print("  1. Start the backend server: python start.py")
    print("  2. Start the frontend: npm run dev")
    print("  3. Test account linking in the web interface")
    print("  4. Try playlist sync functionality")

async def main():
    """Main test function"""
    print("🧪 ChordCircle Music APIs Test Suite")
    print("=" * 60)
    
    # Run all tests
    test_environment_configuration()
    await test_spotify_service()
    await test_apple_music_service()
    await test_api_endpoints()
    await run_integration_tests()
    
    # Print recommendations
    print_recommendations()
    
    print("\n" + "=" * 60)
    print("  Test Suite Complete")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())