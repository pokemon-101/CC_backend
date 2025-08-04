# ChordCircle Backend API

FastAPI backend for the ChordCircle music platform integration project.

## Features

- **User Authentication**: JWT-based authentication with refresh tokens
- **Music Platform Integration**: Spotify and Apple Music OAuth integration
- **Playlist Management**: Create, update, delete, and sync playlists
- **Social Features**: Friend system with requests and connections
- **Music Discovery**: Trending tracks, top songs, and favorites
- **Real-time Sync**: Cross-platform playlist synchronization

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Tokens for authentication
- **SQLite/PostgreSQL**: Database options
- **Spotify Web API**: Music streaming integration
- **Apple Music API**: Music streaming integration

## Quick Start

### Prerequisites

- Python 3.8+
- pip or poetry

### Installation

1. **Clone and navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment setup**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run the server**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/spotify/login` - Spotify OAuth login
- `GET /api/v1/auth/spotify/callback` - Spotify OAuth callback

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update user profile
- `GET /api/v1/users/me/music-accounts` - Get connected music accounts
- `DELETE /api/v1/users/me/music-accounts/{platform}` - Disconnect music account

### Music
- `GET /api/v1/music/trending` - Get trending tracks
- `GET /api/v1/music/top-songs` - Get top songs
- `GET /api/v1/music/favorites` - Get user favorites
- `POST /api/v1/music/favorites/{track_id}` - Add to favorites
- `DELETE /api/v1/music/favorites/{track_id}` - Remove from favorites
- `GET /api/v1/music/search` - Search tracks

### Playlists
- `GET /api/v1/playlists/` - Get user playlists
- `POST /api/v1/playlists/` - Create playlist
- `GET /api/v1/playlists/{playlist_id}` - Get playlist with tracks
- `PUT /api/v1/playlists/{playlist_id}` - Update playlist
- `DELETE /api/v1/playlists/{playlist_id}` - Delete playlist
- `POST /api/v1/playlists/{playlist_id}/tracks` - Add track to playlist
- `DELETE /api/v1/playlists/{playlist_id}/tracks/{track_id}` - Remove track
- `POST /api/v1/playlists/{playlist_id}/sync` - Sync playlist across platforms

### Friends
- `GET /api/v1/friends/` - Get friends list
- `GET /api/v1/friends/requests` - Get friend requests
- `POST /api/v1/friends/request` - Send friend request
- `POST /api/v1/friends/accept/{friendship_id}` - Accept friend request
- `POST /api/v1/friends/decline/{friendship_id}` - Decline friend request
- `DELETE /api/v1/friends/{friend_id}` - Remove friend

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Required
SECRET_KEY=your-super-secret-key
DATABASE_URL=sqlite:///./chordcircle.db

# Spotify Integration
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret

# Apple Music Integration (optional)
APPLE_MUSIC_TEAM_ID=your_team_id
APPLE_MUSIC_KEY_ID=your_key_id
APPLE_MUSIC_PRIVATE_KEY=your_private_key
```

### Database Setup

The application uses SQLite by default. For production, consider PostgreSQL:

```env
DATABASE_URL=postgresql://user:password@localhost/chordcircle
```

### Spotify API Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Add redirect URI: `http://localhost:8000/api/v1/auth/spotify/callback`
4. Copy Client ID and Client Secret to `.env`

### Apple Music API Setup (Optional)

1. Join Apple Developer Program
2. Create MusicKit identifier
3. Generate private key
4. Add credentials to `.env`

## Development

### Project Structure

```
backend/
├── app/
│   ├── api/v1/endpoints/    # API route handlers
│   ├── core/                # Core functionality (config, security, db)
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   └── services/            # External service integrations
├── main.py                  # FastAPI application entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

### Running Tests

```bash
pytest
```

### Code Style

The project uses:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting

```bash
black .
isort .
flake8 .
```

## Deployment

### Docker (Recommended)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations

1. **Use PostgreSQL** instead of SQLite
2. **Set strong SECRET_KEY**
3. **Configure CORS** properly
4. **Use HTTPS** in production
5. **Set up monitoring** and logging
6. **Use environment variables** for sensitive data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details