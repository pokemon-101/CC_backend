import jwt
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from pathlib import Path
from app.core.config import settings

class AppleMusicService:
    def __init__(self):
        self.team_id = settings.APPLE_MUSIC_TEAM_ID
        self.key_id = settings.APPLE_MUSIC_KEY_ID
        self.private_key = self._load_private_key()
        self.base_url = "https://api.music.apple.com/v1"
        self._developer_token = None
        self._token_expires_at = None
    
    def _load_private_key(self) -> str:
        """Load private key from settings or file"""
        if settings.APPLE_MUSIC_PRIVATE_KEY:
            return settings.APPLE_MUSIC_PRIVATE_KEY
        
        # Try to load from file path if specified
        private_key_path = getattr(settings, 'APPLE_MUSIC_PRIVATE_KEY_PATH', None)
        if private_key_path and Path(private_key_path).exists():
            with open(private_key_path, 'r') as f:
                return f.read()
        
        raise ValueError("Apple Music private key not found in settings or file")
    
    def generate_developer_token(self) -> str:
        """Generate Apple Music developer token with caching"""
        # Return cached token if still valid
        if (self._developer_token and self._token_expires_at and 
            datetime.utcnow() < self._token_expires_at - timedelta(minutes=5)):
            return self._developer_token
        
        headers = {
            "alg": "ES256",
            "kid": self.key_id
        }
        
        now = datetime.utcnow()
        expires_at = now + timedelta(hours=12)
        
        payload = {
            "iss": self.team_id,
            "iat": int(now.timestamp()),
            "exp": int(expires_at.timestamp())
        }
        
        try:
            token = jwt.encode(payload, self.private_key, algorithm="ES256", headers=headers)
            self._developer_token = token
            self._token_expires_at = expires_at
            return token
        except Exception as e:
            raise ValueError(f"Failed to generate Apple Music developer token: {e}")
    
    def get_auth_url(self) -> str:
        """Generate Apple Music authorization URL"""
        # Apple Music uses MusicKit JS for web authentication
        # This returns a URL to a page that will handle the MusicKit JS flow
        return f"https://music.apple.com/authorize?app={self.team_id}"
    
    async def get_user_info(self, user_token: str) -> Dict[str, Any]:
        """Get user profile information"""
        developer_token = self.generate_developer_token()
        
        headers = {
            "Authorization": f"Bearer {developer_token}",
            "Music-User-Token": user_token
        }
        
        response = requests.get(f"{self.base_url}/me/storefront", headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    async def get_user_playlists(self, user_token: str) -> Dict[str, Any]:
        """Get user's playlists"""
        developer_token = self.generate_developer_token()
        
        headers = {
            "Authorization": f"Bearer {developer_token}",
            "Music-User-Token": user_token
        }
        
        response = requests.get(f"{self.base_url}/me/library/playlists", headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    async def search_tracks(self, query: str, limit: int = 20) -> Dict[str, Any]:
        """Search for tracks"""
        developer_token = self.generate_developer_token()
        
        headers = {"Authorization": f"Bearer {developer_token}"}
        params = {
            "term": query,
            "types": "songs",
            "limit": limit
        }
        
        response = requests.get(f"{self.base_url}/catalog/us/search", headers=headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    async def create_playlist(self, user_token: str, name: str, description: str = "") -> Dict[str, Any]:
        """Create a new playlist"""
        developer_token = self.generate_developer_token()
        
        headers = {
            "Authorization": f"Bearer {developer_token}",
            "Music-User-Token": user_token,
            "Content-Type": "application/json"
        }
        
        data = {
            "attributes": {
                "name": name,
                "description": description
            },
            "type": "library-playlists"
        }
        
        response = requests.post(f"{self.base_url}/me/library/playlists", headers=headers, json={"data": [data]})
        response.raise_for_status()
        
        return response.json()
    
    async def get_storefront(self, user_token: str) -> Dict[str, Any]:
        """Get user's storefront (country/region)"""
        developer_token = self.generate_developer_token()
        
        headers = {
            "Authorization": f"Bearer {developer_token}",
            "Music-User-Token": user_token
        }
        
        response = requests.get(f"{self.base_url}/me/storefront", headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    async def get_playlist_tracks(self, user_token: str, playlist_id: str) -> Dict[str, Any]:
        """Get tracks from a playlist"""
        developer_token = self.generate_developer_token()
        
        headers = {
            "Authorization": f"Bearer {developer_token}",
            "Music-User-Token": user_token
        }
        
        response = requests.get(
            f"{self.base_url}/me/library/playlists/{playlist_id}/tracks", 
            headers=headers
        )
        response.raise_for_status()
        
        return response.json()
    
    async def add_tracks_to_playlist(self, user_token: str, playlist_id: str, track_ids: list) -> Dict[str, Any]:
        """Add tracks to a playlist"""
        developer_token = self.generate_developer_token()
        
        headers = {
            "Authorization": f"Bearer {developer_token}",
            "Music-User-Token": user_token,
            "Content-Type": "application/json"
        }
        
        data = {
            "data": [
                {
                    "id": track_id,
                    "type": "songs"
                } for track_id in track_ids
            ]
        }
        
        response = requests.post(
            f"{self.base_url}/me/library/playlists/{playlist_id}/tracks",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        
        return response.json()
    
    async def get_catalog_song(self, song_id: str, storefront: str = "us") -> Dict[str, Any]:
        """Get song information from catalog"""
        developer_token = self.generate_developer_token()
        
        headers = {"Authorization": f"Bearer {developer_token}"}
        
        response = requests.get(
            f"{self.base_url}/catalog/{storefront}/songs/{song_id}",
            headers=headers
        )
        response.raise_for_status()
        
        return response.json()
    
    async def search_catalog(self, query: str, types: str = "songs", limit: int = 20, storefront: str = "us") -> Dict[str, Any]:
        """Search Apple Music catalog"""
        developer_token = self.generate_developer_token()
        
        headers = {"Authorization": f"Bearer {developer_token}"}
        params = {
            "term": query,
            "types": types,
            "limit": limit
        }
        
        response = requests.get(
            f"{self.base_url}/catalog/{storefront}/search",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        
        return response.json()
    
    def validate_user_token(self, user_token: str) -> bool:
        """Validate Apple Music user token"""
        try:
            developer_token = self.generate_developer_token()
            
            headers = {
                "Authorization": f"Bearer {developer_token}",
                "Music-User-Token": user_token
            }
            
            response = requests.get(f"{self.base_url}/me/storefront", headers=headers)
            return response.status_code == 200
        except:
            return False