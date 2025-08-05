# ChordCircle - Full-Stack Next.js Application

A modern, full-stack music platform built with Next.js 14, TypeScript, and Tailwind CSS. Connect your Spotify and Apple Music accounts to sync playlists and share music with friends.

## ✨ Features

- 🎵 **Cross-Platform Sync** - Seamlessly sync playlists between Spotify and Apple Music
- 👥 **Social Sharing** - Share music and discover new tracks with friends
- 🔐 **Secure Authentication** - JWT-based auth with bcrypt password hashing
- 📱 **Responsive Design** - Beautiful UI that works on all devices
- ⚡ **Real-time Updates** - Live notifications and status updates
- 🎨 **Modern UI** - Framer Motion animations and Tailwind CSS styling
- 🔒 **TypeScript** - Full type safety throughout the application

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pokemon-101/CC_backend.git
   cd chordcircle-nextjs
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your configuration
   ```

4. **Run the development server:**
   ```bash
   npm run dev
   ```

5. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🛠️ Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Animations:** Framer Motion
- **Authentication:** JWT + bcrypt
- **Icons:** Lucide React
- **HTTP Client:** Axios

## 📁 Project Structure

```
chordcircle-nextjs/
├── app/                    # Next.js App Router
│   ├── api/               # API routes
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ui/               # Reusable UI components
│   ├── AuthModal.tsx     # Authentication modal
│   ├── Header.tsx        # Navigation header
│   └── ...
├── contexts/             # React contexts
├── hooks/                # Custom hooks
├── types/                # TypeScript type definitions
└── ...
```

## 🔧 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration

### Health Checks
- `GET /api/health` - Basic health check
- `GET /api/v1/health` - API v1 health check

### Music (Coming Soon)
- `GET /api/v1/music/playlists` - Get user playlists
- `POST /api/v1/music/playlists` - Create new playlist
- `GET /api/v1/music/sync` - Sync playlists across platforms

## 🚀 Deployment

### Vercel (Recommended)

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   ```bash
   vercel
   ```

3. **Set environment variables in Vercel dashboard**

### Other Platforms

The app can also be deployed on:
- Netlify
- Railway
- Render
- Any Node.js hosting platform

## 🔐 Environment Variables

Copy `.env.example` to `.env.local` and configure:

```env
# Required
JWT_SECRET=your-super-secret-jwt-key
NODE_ENV=production

# Optional (for music API integration)
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
APPLE_MUSIC_TEAM_ID=your_apple_music_team_id
# ... see .env.example for full list
```

## 🧪 Demo Credentials

For testing the authentication:
- **Email:** test@example.com
- **Password:** password123

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you have any questions or need help:

1. Check the [Issues](https://github.com/pokemon-101/CC_backend/issues) page
2. Create a new issue if your problem isn't already reported
3. Provide as much detail as possible

## 🎯 Roadmap

- [ ] Real Spotify/Apple Music OAuth integration
- [ ] PostgreSQL database integration
- [ ] WebSocket real-time features
- [ ] Playlist collaboration features
- [ ] Mobile app (React Native)
- [ ] Advanced music recommendations

---

Built with ❤️ using Next.js and TypeScript