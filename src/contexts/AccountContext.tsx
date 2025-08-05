import { createContext, useContext, useState, ReactNode } from 'react'
import { AccountContextType } from '../types'

const AccountContext = createContext<AccountContextType | undefined>(undefined)

export function AccountProvider({ children }: { children: ReactNode }) {
  const [spotifyConnected, setSpotifyConnected] = useState(false)
  const [appleMusicConnected, setAppleMusicConnected] = useState(false)

  const connectSpotify = async () => {
    // Mock Spotify connection - replace with real OAuth
    await new Promise(resolve => setTimeout(resolve, 1000))
    setSpotifyConnected(true)
  }

  const connectAppleMusic = async () => {
    // Mock Apple Music connection - replace with real OAuth
    await new Promise(resolve => setTimeout(resolve, 1000))
    setAppleMusicConnected(true)
  }

  const disconnectSpotify = async () => {
    await new Promise(resolve => setTimeout(resolve, 500))
    setSpotifyConnected(false)
  }

  const disconnectAppleMusic = async () => {
    await new Promise(resolve => setTimeout(resolve, 500))
    setAppleMusicConnected(false)
  }

  return (
    <AccountContext.Provider value={{
      spotifyConnected,
      appleMusicConnected,
      connectSpotify,
      connectAppleMusic,
      disconnectSpotify,
      disconnectAppleMusic
    }}>
      {children}
    </AccountContext.Provider>
  )
}

export function useAccount() {
  const context = useContext(AccountContext)
  if (context === undefined) {
    throw new Error('useAccount must be used within an AccountProvider')
  }
  return context
}