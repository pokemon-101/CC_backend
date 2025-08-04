from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User, Friendship
from app.schemas.user import FriendshipRequest, FriendshipResponse
from app.api.v1.endpoints.users import get_current_user

router = APIRouter()
security = HTTPBearer()

@router.get("/", response_model=List[FriendshipResponse])
async def get_friends(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    friendships = db.query(Friendship).join(
        User, Friendship.friend_id == User.id
    ).filter(
        Friendship.user_id == current_user.id,
        Friendship.status == "accepted"
    ).all()
    
    friends = []
    for friendship in friendships:
        friend = db.query(User).filter(User.id == friendship.friend_id).first()
        friends.append({
            "id": friendship.id,
            "friend_id": friend.id,
            "friend_username": friend.username,
            "friend_full_name": friend.full_name,
            "friend_avatar_url": friend.avatar_url,
            "status": friendship.status,
            "created_at": friendship.created_at
        })
    
    return friends

@router.get("/requests", response_model=List[FriendshipResponse])
async def get_friend_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get pending requests sent to current user
    requests = db.query(Friendship).join(
        User, Friendship.user_id == User.id
    ).filter(
        Friendship.friend_id == current_user.id,
        Friendship.status == "pending"
    ).all()
    
    friend_requests = []
    for request in requests:
        requester = db.query(User).filter(User.id == request.user_id).first()
        friend_requests.append({
            "id": request.id,
            "friend_id": requester.id,
            "friend_username": requester.username,
            "friend_full_name": requester.full_name,
            "friend_avatar_url": requester.avatar_url,
            "status": request.status,
            "created_at": request.created_at
        })
    
    return friend_requests

@router.post("/request")
async def send_friend_request(
    request_data: FriendshipRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Find user by email
    friend = db.query(User).filter(User.email == request_data.friend_email).first()
    if not friend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if friend.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot send friend request to yourself"
        )
    
    # Check if friendship already exists
    existing_friendship = db.query(Friendship).filter(
        ((Friendship.user_id == current_user.id) & (Friendship.friend_id == friend.id)) |
        ((Friendship.user_id == friend.id) & (Friendship.friend_id == current_user.id))
    ).first()
    
    if existing_friendship:
        if existing_friendship.status == "accepted":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already friends with this user"
            )
        elif existing_friendship.status == "pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Friend request already sent"
            )
    
    # Create friend request
    friendship = Friendship(
        user_id=current_user.id,
        friend_id=friend.id,
        status="pending"
    )
    
    db.add(friendship)
    db.commit()
    
    return {"message": f"Friend request sent to {friend.username}"}

@router.post("/accept/{friendship_id}")
async def accept_friend_request(
    friendship_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    friendship = db.query(Friendship).filter(
        Friendship.id == friendship_id,
        Friendship.friend_id == current_user.id,
        Friendship.status == "pending"
    ).first()
    
    if not friendship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Friend request not found"
        )
    
    # Update status
    friendship.status = "accepted"
    
    # Create reciprocal friendship
    reciprocal_friendship = Friendship(
        user_id=current_user.id,
        friend_id=friendship.user_id,
        status="accepted"
    )
    
    db.add(reciprocal_friendship)
    db.commit()
    
    return {"message": "Friend request accepted"}

@router.post("/decline/{friendship_id}")
async def decline_friend_request(
    friendship_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    friendship = db.query(Friendship).filter(
        Friendship.id == friendship_id,
        Friendship.friend_id == current_user.id,
        Friendship.status == "pending"
    ).first()
    
    if not friendship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Friend request not found"
        )
    
    db.delete(friendship)
    db.commit()
    
    return {"message": "Friend request declined"}

@router.delete("/{friend_id}")
async def remove_friend(
    friend_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Remove both directions of friendship
    friendships = db.query(Friendship).filter(
        ((Friendship.user_id == current_user.id) & (Friendship.friend_id == friend_id)) |
        ((Friendship.user_id == friend_id) & (Friendship.friend_id == current_user.id))
    ).all()
    
    if not friendships:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Friendship not found"
        )
    
    for friendship in friendships:
        db.delete(friendship)
    
    db.commit()
    
    return {"message": "Friend removed successfully"}