from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.music import Playlist, PlaylistTrack, Track
from app.schemas.music import (
    PlaylistCreate, PlaylistUpdate, PlaylistResponse, 
    PlaylistWithTracks, PlaylistTrackAdd, SyncRequest, SyncResponse
)
from app.api.v1.endpoints.users import get_current_user
from app.services.playlist_sync import PlaylistSyncService

router = APIRouter()
security = HTTPBearer()

@router.get("/", response_model=List[PlaylistResponse])
async def get_user_playlists(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    playlists = db.query(Playlist).filter(Playlist.user_id == current_user.id).all()
    
    # Add track count to each playlist
    for playlist in playlists:
        track_count = db.query(PlaylistTrack).filter(PlaylistTrack.playlist_id == playlist.id).count()
        playlist.track_count = track_count
    
    return playlists

@router.post("/", response_model=PlaylistResponse)
async def create_playlist(
    playlist_data: PlaylistCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    playlist = Playlist(
        user_id=current_user.id,
        name=playlist_data.name,
        description=playlist_data.description,
        is_public=playlist_data.is_public
    )
    
    db.add(playlist)
    db.commit()
    db.refresh(playlist)
    
    playlist.track_count = 0
    return playlist

@router.get("/{playlist_id}", response_model=PlaylistWithTracks)
async def get_playlist(
    playlist_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    playlist = db.query(Playlist).filter(
        Playlist.id == playlist_id,
        Playlist.user_id == current_user.id
    ).first()
    
    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found"
        )
    
    # Get tracks
    playlist_tracks = db.query(PlaylistTrack).join(Track).filter(
        PlaylistTrack.playlist_id == playlist_id
    ).order_by(PlaylistTrack.position).all()
    
    tracks = [pt.track for pt in playlist_tracks]
    
    return {
        **playlist.__dict__,
        "tracks": tracks,
        "track_count": len(tracks)
    }

@router.put("/{playlist_id}", response_model=PlaylistResponse)
async def update_playlist(
    playlist_id: int,
    playlist_update: PlaylistUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    playlist = db.query(Playlist).filter(
        Playlist.id == playlist_id,
        Playlist.user_id == current_user.id
    ).first()
    
    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found"
        )
    
    for field, value in playlist_update.dict(exclude_unset=True).items():
        setattr(playlist, field, value)
    
    db.commit()
    db.refresh(playlist)
    
    track_count = db.query(PlaylistTrack).filter(PlaylistTrack.playlist_id == playlist.id).count()
    playlist.track_count = track_count
    
    return playlist

@router.delete("/{playlist_id}")
async def delete_playlist(
    playlist_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    playlist = db.query(Playlist).filter(
        Playlist.id == playlist_id,
        Playlist.user_id == current_user.id
    ).first()
    
    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found"
        )
    
    # Delete playlist tracks first
    db.query(PlaylistTrack).filter(PlaylistTrack.playlist_id == playlist_id).delete()
    
    # Delete playlist
    db.delete(playlist)
    db.commit()
    
    return {"message": "Playlist deleted successfully"}

@router.post("/{playlist_id}/tracks")
async def add_track_to_playlist(
    playlist_id: int,
    track_data: PlaylistTrackAdd,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    playlist = db.query(Playlist).filter(
        Playlist.id == playlist_id,
        Playlist.user_id == current_user.id
    ).first()
    
    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found"
        )
    
    # Check if track exists
    track = db.query(Track).filter(Track.id == track_data.track_id).first()
    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Track not found"
        )
    
    # Check if track already in playlist
    existing = db.query(PlaylistTrack).filter(
        PlaylistTrack.playlist_id == playlist_id,
        PlaylistTrack.track_id == track_data.track_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Track already in playlist"
        )
    
    # Get position
    if track_data.position is None:
        max_position = db.query(PlaylistTrack).filter(
            PlaylistTrack.playlist_id == playlist_id
        ).count()
        position = max_position + 1
    else:
        position = track_data.position
    
    playlist_track = PlaylistTrack(
        playlist_id=playlist_id,
        track_id=track_data.track_id,
        position=position,
        added_by_user_id=current_user.id
    )
    
    db.add(playlist_track)
    db.commit()
    
    return {"message": "Track added to playlist"}

@router.delete("/{playlist_id}/tracks/{track_id}")
async def remove_track_from_playlist(
    playlist_id: int,
    track_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    playlist = db.query(Playlist).filter(
        Playlist.id == playlist_id,
        Playlist.user_id == current_user.id
    ).first()
    
    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found"
        )
    
    playlist_track = db.query(PlaylistTrack).filter(
        PlaylistTrack.playlist_id == playlist_id,
        PlaylistTrack.track_id == track_id
    ).first()
    
    if not playlist_track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Track not in playlist"
        )
    
    db.delete(playlist_track)
    db.commit()
    
    return {"message": "Track removed from playlist"}

@router.post("/{playlist_id}/sync", response_model=SyncResponse)
async def sync_playlist(
    playlist_id: int,
    sync_request: SyncRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    playlist = db.query(Playlist).filter(
        Playlist.id == playlist_id,
        Playlist.user_id == current_user.id
    ).first()
    
    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found"
        )
    
    sync_service = PlaylistSyncService(db)
    result = await sync_service.sync_playlist(current_user.id, playlist_id, sync_request.platforms)
    
    return result