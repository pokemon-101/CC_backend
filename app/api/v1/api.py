from fastapi import APIRouter
from .endpoints import auth, users, music, playlists, friends, websocket

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(music.router, prefix="/music", tags=["music"])
api_router.include_router(playlists.router, prefix="/playlists", tags=["playlists"])
api_router.include_router(friends.router, prefix="/friends", tags=["friends"])
api_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])