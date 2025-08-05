// User types
export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  createdAt: string;
}

export interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

// Music types
export interface Track {
  id: string;
  name: string;
  artist: string;
  album: string;
  duration: number;
  preview_url?: string;
  image?: string;
}

export interface Playlist {
  id: string;
  name: string;
  description?: string;
  tracks: Track[];
  owner: User;
  isPublic: boolean;
  createdAt: string;
}

// Account types
export interface AccountContextType {
  spotifyConnected: boolean;
  appleMusicConnected: boolean;
  connectSpotify: () => Promise<void>;
  connectAppleMusic: () => Promise<void>;
  disconnectSpotify: () => Promise<void>;
  disconnectAppleMusic: () => Promise<void>;
}