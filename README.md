# ChordCircle API - Next.js Backend

A modern, serverless API backend built with Next.js for the ChordCircle music platform.

## Features

- ✅ **Serverless** - Deploys easily on Vercel/Netlify
- ✅ **No compilation issues** - Pure JavaScript/TypeScript
- ✅ **JWT Authentication** - Secure user authentication
- ✅ **CORS enabled** - Ready for frontend integration
- ✅ **Music API integration** - Spotify & Apple Music support
- ✅ **PostgreSQL ready** - Database integration ready

## Quick Start

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set up environment:**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your values
   ```

3. **Run development server:**
   ```bash
   npm run dev
   ```

4. **Test the API:**
   - Health check: http://localhost:8000/api/health
   - API docs: http://localhost:8000

## Deployment

### Vercel (Recommended)
```bash
npm install -g vercel
vercel
```

### Render
- Build Command: `npm run build`
- Start Command: `npm start`

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/v1/health` - API v1 health check
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/music/playlists` - Get playlists (requires auth)
- `POST /api/v1/music/playlists` - Create playlist (requires auth)

## Environment Variables

See `.env.example` for all required environment variables.

## Why Next.js over Python?

- ✅ **No compilation issues** - No Rust/C extensions
- ✅ **Serverless ready** - Perfect for Vercel/Netlify
- ✅ **Fast deployment** - Builds in seconds, not minutes
- ✅ **Modern stack** - TypeScript support out of the box
- ✅ **Great DX** - Hot reload, excellent tooling