import requests
import base64
from urllib.parse import urlencode
from typing import Dict, Any, Optional, List
import time
from app.core.config import settings

class SpotifyService:
    def __init__(self):
        self.client_id = settings.SPOTIFY_CLIENT_ID
        self.client_secret = settings.SPOTIFY_CLIENT_SECRET
        self.redirect_uri = settings.SPOTIFY_REDIRECT_URI
        self.base_url = "https://api.spotify.com/v1"
        self.auth_url = "https://accounts.spotify.com/authorize"
        self.token_url = "https://accounts.spotify.com/api/token"
        
        # Check if in demo mode (credentials not configured)
        self.demo_mode = not all([self.client_id, self.client_secret, self.redirect_uri])
        
        if self.demo_mode:
            print("🎧 Spotify running in DEMO MODE - configure real credentials for production")
    
    def get_auth_url(self, state: Optional[str] = None) -> str:
        """Generate Spotify authorization URL"""
        if self.demo_mode:
            # Return a demo URL that shows setup instructions
            return f"http://localhost:3001/demo/spotify-setup?state={state}&demo=true"
        
        scopes = [
            "user-read-private",
            "user-read-email", 
            "playlist-read-private",
            "playlist-read-collaborative",
            "playlist-modify-public",
            "playlist-modify-private",
            "user-library-read",
            "user-library-modify",
            "user-top-read",
            "user-read-recently-played"
        ]
        
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(scopes),
            "show_dialog": "true"
        }
        
        if state:
            params["state"] = state
            
        return f"{self.auth_url}?{urlencode(params)}"
    
    async def get_access_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        if self.demo_mode:
            return {
                "access_token": "demo_access_token",
                "token_type": "Bearer",
                "expires_in": 3600,
                "refresh_token": "demo_refresh_token",
                "scope": "user-read-private user-read-email"
            }
        
        auth_header = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri
        }
        
        response = requests.post(self.token_url, headers=headers, data=data)
        response.raise_for_status()
        
        return response.json()
    
    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token"""
        auth_header = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        
        response = requests.post(self.token_url, headers=headers, data=data)
        response.raise_for_status()
        
        return response.json()
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user profile information"""
        if self.demo_mode or access_token == "demo_access_token":
            return {
                "id": "demo_user_123",
                "display_name": "Demo User",
                "email": "demo@example.com",
                "followers": {"total": 42},
                "country": "US",
                "images": [{"url": "https://via.placeholder.com/150"}]
            }
        
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = requests.get(f"{self.base_url}/me", headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    async def get_user_playlists(self, access_token: str, limit: int = 50) -> Dict[str, Any]:
        """Get user's playlists"""
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"limit": limit}
        
        response = requests.get(f"{self.base_url}/me/playlists", headers=headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    async def get_playlist_tracks(self, access_token: str, playlist_id: str) -> Dict[str, Any]:
        """Get tracks from a playlist"""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = requests.get(f"{self.base_url}/playlists/{playlist_id}/tracks", headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    async def create_playlist(self, access_token: str, user_id: str, name: str, description: str = "", public: bool = False) -> Dict[str, Any]:
        """Create a new playlist"""
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "name": name,
            "description": description,
            "public": public
        }
        
        response = requests.post(f"{self.base_url}/users/{user_id}/playlists", headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()
    
    async def add_tracks_to_playlist(self, access_token: str, playlist_id: str, track_uris: list) -> Dict[str, Any]:
        """Add tracks to a playlist"""
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        data = {"uris": track_uris}
        
        response = requests.post(f"{self.base_url}/playlists/{playlist_id}/tracks", headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()
    
    async def search_tracks(self, access_token: str, query: str, limit: int = 20) -> Dict[str, Any]:
        """Search for tracks"""
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {
            "q": query,
            "type": "track",
            "limit": limit
        }
        
        response = requests.get(f"{self.base_url}/search", headers=headers, params=params)
        response.raise_for_status()
        
        return response.json()    

    async def get_user_top_tracks(self, access_token: str, time_range: str = "medium_term", limit: int = 20) -> Dict[str, Any]:
        """Get user's top tracks"""
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {
            "time_range": time_range,  # short_term, medium_term, long_term
            "limit": limit
        }
        
        response = requests.get(f"{self.base_url}/me/top/tracks", headers=headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    async def get_user_top_artists(self, access_token: str, time_range: str = "medium_term", limit: int = 20) -> Dict[str, Any]:
        """Get user's top artists"""
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {
            "time_range": time_range,
            "limit": limit
        }
        
        response = requests.get(f"{self.base_url}/me/top/artists", headers=headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    async def get_user_saved_tracks(self, access_token: str, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """Get user's saved tracks (liked songs)"""
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {
            "limit": limit,
            "offset": offset
        }
        
        response = requests.get(f"{self.base_url}/me/tracks", headers=headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    async def save_tracks(self, access_token: str, track_ids: List[str]) -> bool:
        """Save tracks to user's library"""
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Spotify allows max 50 tracks per request
        for i in range(0, len(track_ids), 50):
            batch = track_ids[i:i+50]
            response = requests.put(f"{self.base_url}/me/tracks", headers=headers, json={"ids": batch})
            response.raise_for_status()
        
        return True
    
    async def remove_saved_tracks(self, access_token: str, track_ids: List[str]) -> bool:
        """Remove tracks from user's library"""
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        for i in range(0, len(track_ids), 50):
            batch = track_ids[i:i+50]
            response = requests.delete(f"{self.base_url}/me/tracks", headers=headers, json={"ids": batch})
            response.raise_for_status()
        
        return True
    
    async def get_recommendations(self, access_token: str, seed_tracks: List[str] = None, 
                                seed_artists: List[str] = None, seed_genres: List[str] = None,
                                limit: int = 20, **audio_features) -> Dict[str, Any]:
        """Get track recommendations"""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        params = {"limit": limit}
        
        if seed_tracks:
            params["seed_tracks"] = ",".join(seed_tracks[:5])  # Max 5 seeds
        if seed_artists:
            params["seed_artists"] = ",".join(seed_artists[:5])
        if seed_genres:
            params["seed_genres"] = ",".join(seed_genres[:5])
        
        # Add audio feature parameters (e.g., target_energy=0.8, min_danceability=0.5)
        params.update(audio_features)
        
        response = requests.get(f"{self.base_url}/recommendations", headers=headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    async def get_audio_features(self, access_token: str, track_ids: List[str]) -> Dict[str, Any]:
        """Get audio features for tracks"""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Spotify allows max 100 tracks per request
        all_features = []
        for i in range(0, len(track_ids), 100):
            batch = track_ids[i:i+100]
            params = {"ids": ",".join(batch)}
            
            response = requests.get(f"{self.base_url}/audio-features", headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            all_features.extend(data.get("audio_features", []))
        
        return {"audio_features": all_features}
    
    async def get_track_info(self, access_token: str, track_id: str) -> Dict[str, Any]:
        """Get detailed track information"""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = requests.get(f"{self.base_url}/tracks/{track_id}", headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    async def get_album_tracks(self, access_token: str, album_id: str) -> Dict[str, Any]:
        """Get tracks from an album"""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = requests.get(f"{self.base_url}/albums/{album_id}/tracks", headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    async def get_artist_top_tracks(self, access_token: str, artist_id: str, country: str = "US") -> Dict[str, Any]:
        """Get artist's top tracks"""
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"country": country}
        
        response = requests.get(f"{self.base_url}/artists/{artist_id}/top-tracks", headers=headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    async def follow_playlist(self, access_token: str, playlist_id: str, public: bool = True) -> bool:
        """Follow a playlist"""
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        data = {"public": public}
        
        response = requests.put(f"{self.base_url}/playlists/{playlist_id}/followers", headers=headers, json=data)
        response.raise_for_status()
        
        return True
    
    async def unfollow_playlist(self, access_token: str, playlist_id: str) -> bool:
        """Unfollow a playlist"""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = requests.delete(f"{self.base_url}/playlists/{playlist_id}/followers", headers=headers)
        response.raise_for_status()
        
        return True
    
    def handle_rate_limit(self, response: requests.Response) -> None:
        """Handle Spotify rate limiting"""
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 1))
            time.sleep(retry_after)
            raise Exception(f"Rate limited. Retry after {retry_after} seconds")
    
    async def batch_request(self, access_token: str, requests_data: List[Dict]) -> List[Dict]:
        """Handle multiple requests with rate limiting"""
        results = []
        
        for request_data in requests_data:
            try:
                # Add delay between requests to avoid rate limiting
                time.sleep(0.1)
                
                method = request_data.get('method', 'GET')
                url = request_data['url']
                headers = {"Authorization": f"Bearer {access_token}"}
                
                if method == 'GET':
                    response = requests.get(url, headers=headers)
                elif method == 'POST':
                    response = requests.post(url, headers=headers, json=request_data.get('data'))
                elif method == 'PUT':
                    response = requests.put(url, headers=headers, json=request_data.get('data'))
                elif method == 'DELETE':
                    response = requests.delete(url, headers=headers)
                
                self.handle_rate_limit(response)
                response.raise_for_status()
                
                results.append(response.json())
                
            except Exception as e:
                results.append({"error": str(e)})
        
        return results