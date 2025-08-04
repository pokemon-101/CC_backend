from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.models.user import User, MusicAccount
from app.models.music import Playlist, PlaylistTrack, Track
from app.services.spotify import SpotifyService
from app.services.apple_music import AppleMusicService

class PlaylistSyncService:
    def __init__(self, db: Session):
        self.db = db
        self.spotify_service = SpotifyService()
        self.apple_music_service = AppleMusicService()
    
    async def sync_playlist(self, user_id: int, playlist_id: int, platforms: List[str]) -> Dict[str, Any]:
        """Sync playlist across specified platforms"""
        playlist = self.db.query(Playlist).filter(Playlist.id == playlist_id).first()
        if not playlist:
            return {"success": False, "message": "Playlist not found", "synced_platforms": [], "errors": ["Playlist not found"]}
        
        user_accounts = self.db.query(MusicAccount).filter(
            MusicAccount.user_id == user_id,
            MusicAccount.platform.in_(platforms),
            MusicAccount.is_active == True
        ).all()
        
        if not user_accounts:
            return {"success": False, "message": "No connected accounts found for specified platforms", "synced_platforms": [], "errors": ["No connected accounts"]}
        
        synced_platforms = []
        errors = []
        
        # Get playlist tracks
        playlist_tracks = self.db.query(PlaylistTrack).join(Track).filter(
            PlaylistTrack.playlist_id == playlist_id
        ).order_by(PlaylistTrack.position).all()
        
        for account in user_accounts:
            try:
                if account.platform == "spotify":
                    success = await self._sync_to_spotify(account, playlist, playlist_tracks)
                    if success:
                        synced_platforms.append("spotify")
                    else:
                        errors.append("Failed to sync to Spotify")
                
                elif account.platform == "apple_music":
                    success = await self._sync_to_apple_music(account, playlist, playlist_tracks)
                    if success:
                        synced_platforms.append("apple_music")
                    else:
                        errors.append("Failed to sync to Apple Music")
                        
            except Exception as e:
                errors.append(f"Error syncing to {account.platform}: {str(e)}")
        
        # Update playlist sync status
        if synced_platforms:
            playlist.sync_enabled = True
            playlist.last_synced = self.db.execute("SELECT NOW()").scalar()
            self.db.commit()
        
        return {
            "success": len(synced_platforms) > 0,
            "message": f"Synced to {len(synced_platforms)} platform(s)",
            "synced_platforms": synced_platforms,
            "errors": errors if errors else None
        }
    
    async def _sync_to_spotify(self, account: MusicAccount, playlist: Playlist, tracks: List[PlaylistTrack]) -> bool:
        """Sync playlist to Spotify"""
        try:
            # Check if playlist already exists on Spotify
            if not playlist.spotify_id:
                # Create new playlist on Spotify
                user_info = await self.spotify_service.get_user_info(account.access_token)
                spotify_playlist = await self.spotify_service.create_playlist(
                    account.access_token,
                    user_info["id"],
                    playlist.name,
                    playlist.description or "",
                    playlist.is_public
                )
                playlist.spotify_id = spotify_playlist["id"]
                self.db.commit()
            
            # Get track URIs for Spotify
            track_uris = []
            for pt in tracks:
                if pt.track.spotify_id:
                    track_uris.append(f"spotify:track:{pt.track.spotify_id}")
                else:
                    # Try to find track on Spotify by search
                    search_query = f"{pt.track.title} {pt.track.artist}"
                    search_results = await self.spotify_service.search_tracks(account.access_token, search_query, 1)
                    if search_results["tracks"]["items"]:
                        spotify_track = search_results["tracks"]["items"][0]
                        pt.track.spotify_id = spotify_track["id"]
                        track_uris.append(spotify_track["uri"])
                        self.db.commit()
            
            # Add tracks to playlist
            if track_uris:
                await self.spotify_service.add_tracks_to_playlist(
                    account.access_token,
                    playlist.spotify_id,
                    track_uris
                )
            
            return True
            
        except Exception as e:
            print(f"Error syncing to Spotify: {e}")
            return False
    
    async def _sync_to_apple_music(self, account: MusicAccount, playlist: Playlist, tracks: List[PlaylistTrack]) -> bool:
        """Sync playlist to Apple Music"""
        try:
            # Check if playlist already exists on Apple Music
            if not playlist.apple_music_id:
                # Create new playlist on Apple Music
                apple_playlist = await self.apple_music_service.create_playlist(
                    account.access_token,
                    playlist.name,
                    playlist.description or ""
                )
                playlist.apple_music_id = apple_playlist["data"][0]["id"]
                self.db.commit()
            
            # Apple Music sync implementation would go here
            # This is a simplified version
            return True
            
        except Exception as e:
            print(f"Error syncing to Apple Music: {e}")
            return False