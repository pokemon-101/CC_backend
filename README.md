# ChordCircle - Connect Your Music

A modern music platform built with Next.js 14 and TypeScript. Connect your Spotify and Apple Music accounts to sync playlists and share music with friends.

## 🚀 Quick Deploy

### Vercel (1-Click Deploy)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/pokemon-101/CC_backend/tree/clean)

### Manual Deploy
1. **Clone & Install:**
   ```bash
   git clone -b clean https://github.com/pokemon-101/CC_backend.git
   cd CC_backend
   npm install
   ```

2. **Environment Setup:**
   ```bash
   cp .env.example .env.local
   # Add your JWT_SECRET
   ```

3. **Deploy:**
   ```bash
   npm run build
   npm start
   ```

## ✨ Features

- 🎵 **Cross-Platform Sync** - Connect Spotify & Apple Music
- 👥 **Social Sharing** - Share music with friends  
- ⚡ **Real-time Updates** - Live notifications
- 🔒 **Secure** - JWT authentication with bcrypt
- 📱 **Responsive** - Works on all devices
- 🎨 **Modern UI** - Tailwind CSS + Framer Motion

## 🧪 Demo

**Test Login:**
- Email: `test@example.com`
- Password: `password123`

## 📁 Structure

```
chordcircle-clean/
├── app/
│   ├── api/auth/login/     # Authentication API
│   ├── api/health/         # Health check
│   ├── globals.css         # Global styles
│   ├── layout.tsx          # Root layout
│   └── page.tsx            # Home page
├── package.json            # Dependencies
├── tailwind.config.js      # Tailwind config
└── tsconfig.json           # TypeScript config
```

## 🔧 Environment Variables

```env
JWT_SECRET=your-super-secret-jwt-key
NODE_ENV=production
NEXT_PUBLIC_APP_URL=https://your-app.vercel.app
```

## 🛠️ Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Animations:** Framer Motion
- **Auth:** JWT + bcrypt
- **Icons:** Lucide React

## 📝 License

MIT License - see LICENSE file for details.

---

**Ready to deploy in under 2 minutes!** 🚀