'use client'

import { createContext, useContext, useState, ReactNode } from 'react'
import type { AccountContextType } from '@/types'
import { toast } from '@/components/ui/Toaster'

const AccountContext = createContext<AccountContextType | undefined>(undefined)

export function AccountProvider({ children }: { children: ReactNode }) {
  const [spotifyConnected, setSpotifyConnected] = useState(false)
  const [appleMusicConnected, setAppleMusicConnected] = useState(false)

  const connectSpotify = async () => {
    try {
      // Mock Spotify connection - replace with real OAuth flow
      await new Promise(resolve => setTimeout(resolve, 1000))
      setSpotifyConnected(true)
      toast.success('Spotify account connected successfully!')
    } catch (error) {
      toast.error('Failed to connect Spotify account')
      throw error
    }
  }

  const connectAppleMusic = async () => {
    try {
      // Mock Apple Music connection - replace with real OAuth flow
      await new Promise(resolve => setTimeout(resolve, 1000))
      setAppleMusicConnected(true)
      toast.success('Apple Music account connected successfully!')
    } catch (error) {
      toast.error('Failed to connect Apple Music account')
      throw error
    }
  }

  const disconnectSpotify = async () => {
    try {
      await new Promise(resolve => setTimeout(resolve, 500))
      setSpotifyConnected(false)
      toast.success('Spotify account disconnected')
    } catch (error) {
      toast.error('Failed to disconnect Spotify account')
      throw error
    }
  }

  const disconnectAppleMusic = async () => {
    try {
      await new Promise(resolve => setTimeout(resolve, 500))
      setAppleMusicConnected(false)
      toast.success('Apple Music account disconnected')
    } catch (error) {
      toast.error('Failed to disconnect Apple Music account')
      throw error
    }
  }

  const value: AccountContextType = {
    spotifyConnected,
    appleMusicConnected,
    connectSpotify,
    connectAppleMusic,
    disconnectSpotify,
    disconnectAppleMusic
  }

  return (
    <AccountContext.Provider value={value}>
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