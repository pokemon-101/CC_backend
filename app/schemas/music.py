from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TrackBase(BaseModel):
    title: str
    artist: str
    album: Optional[str] = None
    duration_ms: Optional[int] = None
    genre: Optional[str] = None

class TrackCreate(TrackBase):
    spotify_id: Optional[str] = None
    apple_music_id: Optional[str] = None

class TrackResponse(TrackBase):
    id: int
    spotify_id: Optional[str] = None
    apple_music_id: Optional[str] = None
    popularity: Optional[int] = None
    preview_url: Optional[str] = None
    cover_image_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class PlaylistBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False

class PlaylistCreate(PlaylistBase):
    pass

class PlaylistUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None

class PlaylistResponse(PlaylistBase):
    id: int
    user_id: int
    cover_image_url: Optional[str] = None
    spotify_id: Optional[str] = None
    apple_music_id: Optional[str] = None
    sync_enabled: bool
    last_synced: Optional[datetime] = None
    created_at: datetime
    track_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

class PlaylistWithTracks(PlaylistResponse):
    tracks: List[TrackResponse] = []

class PlaylistTrackAdd(BaseModel):
    track_id: int
    position: Optional[int] = None

class TrendingTrackResponse(BaseModel):
    track: TrackResponse
    rank: int
    plays_count: int
    growth_percentage: int
    
    class Config:
        from_attributes = True

class UserFavoriteResponse(BaseModel):
    track: TrackResponse
    rating: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class SyncRequest(BaseModel):
    playlist_id: int
    platforms: List[str]  # ['spotify', 'apple_music']

class SyncResponse(BaseModel):
    success: bool
    message: str
    synced_platforms: List[str]
    errors: Optional[List[str]] = None