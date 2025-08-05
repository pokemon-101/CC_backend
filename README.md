# ChordCircle - Vite + React + TypeScript

A modern, fast music platform built with Vite, React, and TypeScript. Connect your Spotify and Apple Music accounts to sync playlists and share music with friends.

## ✨ Features

- ⚡ **Lightning Fast** - Built with Vite for instant dev server and fast builds
- 🎵 **Cross-Platform Sync** - Connect Spotify & Apple Music
- 👥 **Social Sharing** - Share music with friends  
- 🔒 **TypeScript** - Full type safety
- 📱 **Responsive** - Works on all devices
- 🎨 **Modern UI** - Tailwind CSS with smooth animations

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

1. **Clone and install:**
   ```bash
   git clone -b vite https://github.com/pokemon-101/CC_backend.git
   cd CC_backend
   npm install
   ```

2. **Run development server:**
   ```bash
   npm run dev
   ```

3. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🛠️ Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 🏗️ Tech Stack

- **Build Tool:** Vite
- **Framework:** React 18
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Icons:** Lucide React
- **Routing:** React Router DOM

## 📁 Project Structure

```
chordcircle-vite/
├── src/
│   ├── App.tsx           # Main app component
│   ├── main.tsx          # App entry point
│   └── index.css         # Global styles
├── index.html            # HTML template
├── vite.config.ts        # Vite configuration
├── tailwind.config.js    # Tailwind configuration
└── package.json          # Dependencies
```

## 🚀 Deployment

### Vercel
```bash
npm install -g vercel
vercel
```

### Netlify
```bash
npm run build
# Upload dist/ folder to Netlify
```

### Other Platforms
The `dist/` folder contains all static files ready for deployment.

## 🎯 Why Vite?

- ✅ **No webpack complexity** - Simple, fast bundling
- ✅ **Instant hot reload** - Changes appear immediately
- ✅ **Fast builds** - Optimized for speed
- ✅ **Modern tooling** - ESM, TypeScript out of the box
- ✅ **No hydration issues** - Pure client-side rendering

---

**Ready to deploy in under 1 minute!** 🚀