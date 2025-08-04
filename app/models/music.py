from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Playlist(Base):
    __tablename__ = "playlists"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    is_public = Column(Boolean, default=False)
    cover_image_url = Column(String, nullable=True)
    
    # Platform sync info
    spotify_id = Column(String, nullable=True)
    apple_music_id = Column(String, nullable=True)
    sync_enabled = Column(Boolean, default=False)
    last_synced = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="playlists")
    tracks = relationship("PlaylistTrack", back_populates="playlist")

class Track(Base):
    __tablename__ = "tracks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    album = Column(String, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    
    # Platform IDs
    spotify_id = Column(String, nullable=True, unique=True)
    apple_music_id = Column(String, nullable=True, unique=True)
    
    # Additional metadata
    genre = Column(String, nullable=True)
    release_date = Column(String, nullable=True)
    popularity = Column(Integer, nullable=True)
    preview_url = Column(String, nullable=True)
    cover_image_url = Column(String, nullable=True)
    
    # Platform-specific data
    platform_data = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class PlaylistTrack(Base):
    __tablename__ = "playlist_tracks"
    
    id = Column(Integer, primary_key=True, index=True)
    playlist_id = Column(Integer, ForeignKey("playlists.id"), nullable=False)
    track_id = Column(Integer, ForeignKey("tracks.id"), nullable=False)
    position = Column(Integer, nullable=False)
    added_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    playlist = relationship("Playlist", back_populates="tracks")
    track = relationship("Track")
    added_by = relationship("User")

class UserFavorite(Base):
    __tablename__ = "user_favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    track_id = Column(Integer, ForeignKey("tracks.id"), nullable=False)
    rating = Column(Integer, nullable=True)  # 1-5 stars
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    track = relationship("Track")

class TrendingTrack(Base):
    __tablename__ = "trending_tracks"
    
    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(Integer, ForeignKey("tracks.id"), nullable=False)
    rank = Column(Integer, nullable=False)
    plays_count = Column(Integer, default=0)
    growth_percentage = Column(Integer, default=0)
    date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    track = relationship("Track")