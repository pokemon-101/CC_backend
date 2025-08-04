from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_token
from app.models.user import User
from app.websocket.manager import manager
import json

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    """WebSocket endpoint for real-time updates"""
    try:
        # Verify token
        token_user_id = verify_token(token)
        if int(token_user_id) != user_id:
            await websocket.close(code=1008, reason="Invalid token")
            return
        
        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            await websocket.close(code=1008, reason="User not found")
            return
        
        # Connect user
        await manager.connect(websocket, user_id)
        
        try:
            while True:
                # Listen for messages from client
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle different message types
                if message.get("type") == "ping":
                    await manager.send_personal_message({
                        "type": "pong",
                        "message": "Connection alive"
                    }, websocket)
                
                elif message.get("type") == "status":
                    # Update user status or handle status messages
                    await manager.send_personal_message({
                        "type": "status_update",
                        "message": "Status updated"
                    }, websocket)
                
        except WebSocketDisconnect:
            manager.disconnect(websocket, user_id)
            
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.close(code=1011, reason="Internal error")
        except:
            pass