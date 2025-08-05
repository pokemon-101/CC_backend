// User types
export interface User {
  id: string;
  email: string;
  name?: string;
  avatar?: string;
  createdAt: string;
  updatedAt: string;
}

export interface AuthUser {
  user: User;
  token: string;
}

// Music types
export interface Track {
  id: string;
  name: string;
  artist: string;
  album: string;
  duration: number;
  preview_url?: string;
  external_urls: {
    spotify?: string;
    apple_music?: string;
  };
}

export interface Playlist {
  id: string;
  name: string;
  description?: string;
  tracks: Track[];
  tracks_count: number;
  owner: User;
  created_at: string;
  updated_at: string;
  is_public: boolean;
}

// API Response types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  name: string;
}

// Music Service types
export interface SpotifyAuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  refresh_token?: string;
}

export interface AppleMusicAuthResponse {
  token: string;
  expires_at: string;
}

// WebSocket types
export interface WebSocketMessage {
  type: 'PLAYLIST_UPDATE' | 'FRIEND_ACTIVITY' | 'NOTIFICATION';
  payload: any;
  timestamp: string;
}

// Context types
export interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

export interface AccountContextType {
  spotifyConnected: boolean;
  appleMusicConnected: boolean;
  connectSpotify: () => Promise<void>;
  connectAppleMusic: () => Promise<void>;
  disconnectSpotify: () => Promise<void>;
  disconnectAppleMusic: () => Promise<void>;
}

// Component Props types
export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}

export interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  className?: string;
}