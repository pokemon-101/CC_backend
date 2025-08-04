from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, verify_token
from app.core.config import settings
from app.models.user import User, MusicAccount
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse
from app.services.spotify import SpotifyService
from app.services.apple_music import AppleMusicService

router = APIRouter()
security = HTTPBearer()

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        bio=user_data.bio,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    user_id = verify_token(credentials.credentials)
    user = db.query(User).filter(User.id == int(user_id)).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.get("/spotify/login")
async def spotify_login(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        # Verify user is authenticated
        user_id = verify_token(credentials.credentials)
        user = db.query(User).filter(User.id == int(user_id)).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        spotify_service = SpotifyService()
        auth_url = spotify_service.get_auth_url(state=str(user.id))
        return {"auth_url": auth_url}
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Spotify configuration error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate Spotify auth URL"
        )

@router.get("/spotify/callback")
async def spotify_callback(
    code: str,
    state: str = None,
    error: str = None,
    db: Session = Depends(get_db)
):
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Spotify authorization failed: {error}"
        )
    
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization code not provided"
        )
    
    try:
        # Get user from state parameter
        if not state:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="State parameter missing"
            )
        
        user = db.query(User).filter(User.id == int(state)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        spotify_service = SpotifyService()
        token_info = await spotify_service.get_access_token(code)
        user_info = await spotify_service.get_user_info(token_info["access_token"])
        
        # Calculate token expiration
        expires_at = None
        if "expires_in" in token_info:
            from datetime import datetime, timedelta
            expires_at = datetime.utcnow() + timedelta(seconds=token_info["expires_in"])
        
        # Save or update Spotify account
        existing_account = db.query(MusicAccount).filter(
            MusicAccount.user_id == user.id,
            MusicAccount.platform == "spotify"
        ).first()
        
        if existing_account:
            existing_account.access_token = token_info["access_token"]
            existing_account.refresh_token = token_info.get("refresh_token")
            existing_account.platform_username = user_info.get("display_name")
            existing_account.platform_data = user_info
            existing_account.token_expires_at = expires_at
            existing_account.is_active = True
        else:
            music_account = MusicAccount(
                user_id=user.id,
                platform="spotify",
                platform_user_id=user_info["id"],
                platform_username=user_info.get("display_name"),
                access_token=token_info["access_token"],
                refresh_token=token_info.get("refresh_token"),
                token_expires_at=expires_at,
                platform_data=user_info,
                is_active=True
            )
            db.add(music_account)
        
        db.commit()
        
        # Redirect to frontend with success message
        return {
            "message": "Spotify account connected successfully",
            "user_info": {
                "display_name": user_info.get("display_name"),
                "email": user_info.get("email"),
                "followers": user_info.get("followers", {}).get("total", 0),
                "country": user_info.get("country")
            }
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Spotify service error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to connect Spotify account: {str(e)}"
        )

@router.get("/apple-music/login")
async def apple_music_login(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        # Verify user is authenticated
        user_id = verify_token(credentials.credentials)
        user = db.query(User).filter(User.id == int(user_id)).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        apple_service = AppleMusicService()
        
        # Generate developer token for the frontend to use
        developer_token = apple_service.generate_developer_token()
        
        return {
            "developer_token": developer_token,
            "team_id": apple_service.team_id,
            "message": "Use MusicKit JS on frontend to get user token"
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Apple Music configuration error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate Apple Music developer token"
        )

@router.post("/apple-music/callback")
async def apple_music_callback(
    user_token: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    try:
        user_id = verify_token(credentials.credentials)
        user = db.query(User).filter(User.id == int(user_id)).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        apple_service = AppleMusicService()
        
        # Validate the user token
        if not apple_service.validate_user_token(user_token):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Apple Music user token"
            )
        
        # Get user info
        user_info = await apple_service.get_user_info(user_token)
        storefront_data = user_info.get("data", [{}])[0]
        storefront_id = storefront_data.get("id", "us")
        
        # Save or update Apple Music account
        existing_account = db.query(MusicAccount).filter(
            MusicAccount.user_id == user.id,
            MusicAccount.platform == "apple_music"
        ).first()
        
        if existing_account:
            existing_account.access_token = user_token
            existing_account.platform_data = user_info
            existing_account.is_active = True
        else:
            music_account = MusicAccount(
                user_id=user.id,
                platform="apple_music",
                platform_user_id=storefront_id,
                access_token=user_token,
                platform_data=user_info,
                is_active=True
            )
            db.add(music_account)
        
        db.commit()
        
        return {
            "message": "Apple Music account connected successfully",
            "storefront": storefront_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to connect Apple Music account: {str(e)}"
        )

@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # In a real implementation, you might want to blacklist the token
    return {"message": "Successfully logged out"}