from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import verify_token
from app.models.user import User
from app.models.music import Track, TrendingTrack, UserFavorite
from app.schemas.music import TrackResponse, TrendingTrackResponse, UserFavoriteResponse
from app.api.v1.endpoints.users import get_current_user

router = APIRouter()
security = HTTPBearer()

@router.get("/trending", response_model=List[TrendingTrackResponse])
async def get_trending_tracks(
    limit: int = Query(default=10, le=50),
    db: Session = Depends(get_db)
):
    trending = db.query(TrendingTrack).join(Track).order_by(TrendingTrack.rank).limit(limit).all()
    
    # If no trending data, return mock data
    if not trending:
        mock_trending = [
            {"track": {"id": 1, "title": "Blinding Lights", "artist": "The Weeknd", "album": "After Hours", "duration_ms": 200040, "genre": "Pop", "popularity": 95, "cover_image_url": None, "preview_url": None, "spotify_id": None, "apple_music_id": None, "created_at": "2024-01-01T00:00:00"}, "rank": 1, "plays_count": 2100000, "growth_percentage": 15},
            {"track": {"id": 2, "title": "Shape of You", "artist": "Ed Sheeran", "album": "÷", "duration_ms": 233712, "genre": "Pop", "popularity": 92, "cover_image_url": None, "preview_url": None, "spotify_id": None, "apple_music_id": None, "created_at": "2024-01-01T00:00:00"}, "rank": 2, "plays_count": 1800000, "growth_percentage": 12},
            {"track": {"id": 3, "title": "Bad Habits", "artist": "Ed Sheeran", "album": "=", "duration_ms": 231146, "genre": "Pop", "popularity": 88, "cover_image_url": None, "preview_url": None, "spotify_id": None, "apple_music_id": None, "created_at": "2024-01-01T00:00:00"}, "rank": 3, "plays_count": 1500000, "growth_percentage": 8},
            {"track": {"id": 4, "title": "Stay", "artist": "The Kid LAROI", "album": "F*CK LOVE 3", "duration_ms": 141806, "genre": "Hip-Hop", "popularity": 90, "cover_image_url": None, "preview_url": None, "spotify_id": None, "apple_music_id": None, "created_at": "2024-01-01T00:00:00"}, "rank": 4, "plays_count": 1300000, "growth_percentage": 22}
        ]
        return mock_trending
    
    return [
        {
            "track": item.track,
            "rank": item.rank,
            "plays_count": item.plays_count,
            "growth_percentage": item.growth_percentage
        }
        for item in trending
    ]

@router.get("/top-songs", response_model=List[TrackResponse])
async def get_top_songs(
    limit: int = Query(default=10, le=50),
    db: Session = Depends(get_db)
):
    # Mock data for top songs
    mock_top_songs = [
        {"id": 1, "title": "As It Was", "artist": "Harry Styles", "album": "Harry's House", "duration_ms": 167303, "genre": "Pop", "popularity": 98, "cover_image_url": None, "preview_url": None, "spotify_id": None, "apple_music_id": None, "created_at": "2024-01-01T00:00:00"},
        {"id": 2, "title": "Heat Waves", "artist": "Glass Animals", "album": "Dreamland", "duration_ms": 238805, "genre": "Alternative", "popularity": 95, "cover_image_url": None, "preview_url": None, "spotify_id": None, "apple_music_id": None, "created_at": "2024-01-01T00:00:00"},
        {"id": 3, "title": "Anti-Hero", "artist": "Taylor Swift", "album": "Midnights", "duration_ms": 200690, "genre": "Pop", "popularity": 97, "cover_image_url": None, "preview_url": None, "spotify_id": None, "apple_music_id": None, "created_at": "2024-01-01T00:00:00"},
        {"id": 4, "title": "Unholy", "artist": "Sam Smith", "album": "Gloria", "duration_ms": 156481, "genre": "Pop", "popularity": 93, "cover_image_url": None, "preview_url": None, "spotify_id": None, "apple_music_id": None, "created_at": "2024-01-01T00:00:00"}
    ]
    
    return mock_top_songs[:limit]

@router.get("/favorites", response_model=List[UserFavoriteResponse])
async def get_user_favorites(
    current_user: User = Depends(get_current_user),
    limit: int = Query(default=10, le=50),
    db: Session = Depends(get_db)
):
    favorites = db.query(UserFavorite).join(Track).filter(
        UserFavorite.user_id == current_user.id
    ).limit(limit).all()
    
    # If no favorites, return mock data
    if not favorites:
        mock_favorites = [
            {"track": {"id": 1, "title": "Watermelon Sugar", "artist": "Harry Styles", "album": "Fine Line", "duration_ms": 174000, "genre": "Pop", "popularity": 89, "cover_image_url": None, "preview_url": None, "spotify_id": None, "apple_music_id": None, "created_at": "2024-01-01T00:00:00"}, "rating": 5, "created_at": "2024-01-01T00:00:00"},
            {"track": {"id": 2, "title": "Levitating", "artist": "Dua Lipa", "album": "Future Nostalgia", "duration_ms": 203064, "genre": "Pop", "popularity": 91, "cover_image_url": None, "preview_url": None, "spotify_id": None, "apple_music_id": None, "created_at": "2024-01-01T00:00:00"}, "rating": 5, "created_at": "2024-01-01T00:00:00"},
            {"track": {"id": 3, "title": "Good 4 U", "artist": "Olivia Rodrigo", "album": "SOUR", "duration_ms": 178147, "genre": "Pop", "popularity": 94, "cover_image_url": None, "preview_url": None, "spotify_id": None, "apple_music_id": None, "created_at": "2024-01-01T00:00:00"}, "rating": 4, "created_at": "2024-01-01T00:00:00"},
            {"track": {"id": 4, "title": "Peaches", "artist": "Justin Bieber", "album": "Justice", "duration_ms": 198000, "genre": "Pop", "popularity": 87, "cover_image_url": None, "preview_url": None, "spotify_id": None, "apple_music_id": None, "created_at": "2024-01-01T00:00:00"}, "rating": 4, "created_at": "2024-01-01T00:00:00"}
        ]
        return mock_favorites
    
    return [
        {
            "track": fav.track,
            "rating": fav.rating,
            "created_at": fav.created_at
        }
        for fav in favorites
    ]

@router.post("/favorites/{track_id}")
async def add_to_favorites(
    track_id: int,
    rating: Optional[int] = Query(default=None, ge=1, le=5),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if track exists
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Track not found"
        )
    
    # Check if already in favorites
    existing_favorite = db.query(UserFavorite).filter(
        UserFavorite.user_id == current_user.id,
        UserFavorite.track_id == track_id
    ).first()
    
    if existing_favorite:
        if rating:
            existing_favorite.rating = rating
            db.commit()
        return {"message": "Track updated in favorites"}
    
    # Add to favorites
    favorite = UserFavorite(
        user_id=current_user.id,
        track_id=track_id,
        rating=rating
    )
    db.add(favorite)
    db.commit()
    
    return {"message": "Track added to favorites"}

@router.delete("/favorites/{track_id}")
async def remove_from_favorites(
    track_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    favorite = db.query(UserFavorite).filter(
        UserFavorite.user_id == current_user.id,
        UserFavorite.track_id == track_id
    ).first()
    
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Track not in favorites"
        )
    
    db.delete(favorite)
    db.commit()
    
    return {"message": "Track removed from favorites"}

@router.get("/search")
async def search_tracks(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=20, le=50),
    db: Session = Depends(get_db)
):
    tracks = db.query(Track).filter(
        Track.title.contains(q) | Track.artist.contains(q) | Track.album.contains(q)
    ).limit(limit).all()
    
    return tracks