from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
        self.user_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """Connect a user's WebSocket"""
        await websocket.accept()
        
        if user_id not in self.user_connections:
            self.user_connections[user_id] = []
        
        self.user_connections[user_id].append(websocket)
        self.active_connections[id(websocket)] = websocket
        
        # Send welcome message
        await self.send_personal_message({
            "type": "connection",
            "message": "Connected to ChordCircle real-time updates"
        }, websocket)
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        """Disconnect a user's WebSocket"""
        if id(websocket) in self.active_connections:
            del self.active_connections[id(websocket)]
        
        if user_id in self.user_connections:
            if websocket in self.user_connections[user_id]:
                self.user_connections[user_id].remove(websocket)
            
            # Clean up empty user connections
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific WebSocket"""
        try:
            await websocket.send_text(json.dumps(message))
        except:
            pass  # Connection might be closed
    
    async def send_message_to_user(self, message: dict, user_id: int):
        """Send message to all connections of a specific user"""
        if user_id in self.user_connections:
            disconnected = []
            for websocket in self.user_connections[user_id]:
                try:
                    await websocket.send_text(json.dumps(message))
                except:
                    disconnected.append(websocket)
            
            # Clean up disconnected sockets
            for ws in disconnected:
                self.user_connections[user_id].remove(ws)
    
    async def broadcast_to_friends(self, message: dict, user_id: int, friend_ids: List[int]):
        """Broadcast message to user's friends"""
        for friend_id in friend_ids:
            await self.send_message_to_user(message, friend_id)
    
    async def notify_playlist_sync(self, user_id: int, playlist_name: str, platforms: List[str]):
        """Notify user about playlist sync completion"""
        message = {
            "type": "playlist_sync",
            "playlist_name": playlist_name,
            "platforms": platforms,
            "message": f"Playlist '{playlist_name}' synced to {', '.join(platforms)}"
        }
        await self.send_message_to_user(message, user_id)
    
    async def notify_friend_request(self, user_id: int, requester_name: str):
        """Notify user about new friend request"""
        message = {
            "type": "friend_request",
            "requester_name": requester_name,
            "message": f"{requester_name} sent you a friend request"
        }
        await self.send_message_to_user(message, user_id)
    
    async def notify_friend_accepted(self, user_id: int, friend_name: str):
        """Notify user that friend request was accepted"""
        message = {
            "type": "friend_accepted",
            "friend_name": friend_name,
            "message": f"{friend_name} accepted your friend request"
        }
        await self.send_message_to_user(message, user_id)

manager = ConnectionManager()