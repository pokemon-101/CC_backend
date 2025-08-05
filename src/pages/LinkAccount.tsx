import { useState } from 'react'
import { Music, Check, X, ExternalLink, RefreshCw } from 'lucide-react'
import { useAccount } from '../contexts/AccountContext'

export function LinkAccount() {
  const {
    spotifyConnected,
    appleMusicConnected,
    connectSpotify,
    connectAppleMusic,
    disconnectSpotify,
    disconnectAppleMusic
  } = useAccount()

  const [loading, setLoading] = useState<string | null>(null)

  const handleConnect = async (service: 'spotify' | 'apple') => {
    setLoading(service)
    try {
      if (service === 'spotify') {
        await connectSpotify()
      } else {
        await connectAppleMusic()
      }
    } catch (error) {
      alert('Failed to connect account')
    } finally {
      setLoading(null)
    }
  }

  const handleDisconnect = async (service: 'spotify' | 'apple') => {
    setLoading(service)
    try {
      if (service === 'spotify') {
        await disconnectSpotify()
      } else {
        await disconnectAppleMusic()
      }
    } catch (error) {
      alert('Failed to disconnect account')
    } finally {
      setLoading(null)
    }
  }

  const services = [
    {
      id: 'spotify',
      name: 'Spotify',
      description: 'Connect your Spotify account to sync playlists and discover music',
      color: 'bg-green-500',
      connected: spotifyConnected,
      features: ['Sync playlists', 'Import favorites', 'Real-time updates', 'Friend activity']
    },
    {
      id: 'apple',
      name: 'Apple Music',
      description: 'Connect your Apple Music account to access your library',
      color: 'bg-gray-800',
      connected: appleMusicConnected,
      features: ['Library access', 'Playlist sync', 'Cross-platform sharing', 'Smart recommendations']
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-900 to-green-900 pt-20 pb-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-4">
            Link Your Music Accounts
          </h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Connect your streaming services to sync playlists, share music with friends, 
            and get the most out of ChordCircle
          </p>
        </div>

        {/* Connection Status */}
        <div className="glass rounded-xl p-6 mb-8">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center">
            <Music className="w-5 h-5 mr-2" />
            Connection Status
          </h2>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="flex items-center justify-between p-4 bg-white/5 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-green-500 rounded-lg flex items-center justify-center">
                  <Music className="w-5 h-5 text-white" />
                </div>
                <span className="text-white font-medium">Spotify</span>
              </div>
              <div className="flex items-center space-x-2">
                {spotifyConnected ? (
                  <Check className="w-5 h-5 text-green-500" />
                ) : (
                  <X className="w-5 h-5 text-red-500" />
                )}
                <span className={`text-sm ${spotifyConnected ? 'text-green-500' : 'text-red-500'}`}>
                  {spotifyConnected ? 'Connected' : 'Not Connected'}
                </span>
              </div>
            </div>
            
            <div className="flex items-center justify-between p-4 bg-white/5 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center">
                  <Music className="w-5 h-5 text-white" />
                </div>
                <span className="text-white font-medium">Apple Music</span>
              </div>
              <div className="flex items-center space-x-2">
                {appleMusicConnected ? (
                  <Check className="w-5 h-5 text-green-500" />
                ) : (
                  <X className="w-5 h-5 text-red-500" />
                )}
                <span className={`text-sm ${appleMusicConnected ? 'text-green-500' : 'text-red-500'}`}>
                  {appleMusicConnected ? 'Connected' : 'Not Connected'}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Service Cards */}
        <div className="grid lg:grid-cols-2 gap-8">
          {services.map((service) => (
            <div key={service.id} className="glass rounded-xl p-6">
              <div className="flex items-center space-x-4 mb-6">
                <div className={`w-16 h-16 ${service.color} rounded-xl flex items-center justify-center`}>
                  <Music className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white">{service.name}</h3>
                  <p className="text-gray-300 text-sm">{service.description}</p>
                </div>
              </div>

              {/* Features */}
              <div className="mb-6">
                <h4 className="text-white font-medium mb-3">Features:</h4>
                <div className="grid grid-cols-2 gap-2">
                  {service.features.map((feature) => (
                    <div key={feature} className="flex items-center space-x-2">
                      <Check className="w-4 h-4 text-green-500" />
                      <span className="text-gray-300 text-sm">{feature}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Action Button */}
              <div className="space-y-3">
                {service.connected ? (
                  <>
                    <div className="flex items-center space-x-2 text-green-500 mb-3">
                      <Check className="w-5 h-5" />
                      <span className="font-medium">Connected successfully!</span>
                    </div>
                    <div className="flex space-x-3">
                      <button
                        onClick={() => handleConnect(service.id as 'spotify' | 'apple')}
                        disabled={loading === service.id}
                        className="flex-1 bg-blue-500 text-white py-3 rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50 flex items-center justify-center space-x-2"
                      >
                        {loading === service.id ? (
                          <RefreshCw className="w-4 h-4 animate-spin" />
                        ) : (
                          <RefreshCw className="w-4 h-4" />
                        )}
                        <span>Sync Now</span>
                      </button>
                      <button
                        onClick={() => handleDisconnect(service.id as 'spotify' | 'apple')}
                        disabled={loading === service.id}
                        className="px-6 py-3 border border-red-500 text-red-500 rounded-lg hover:bg-red-500 hover:text-white transition-colors disabled:opacity-50"
                      >
                        Disconnect
                      </button>
                    </div>
                  </>
                ) : (
                  <button
                    onClick={() => handleConnect(service.id as 'spotify' | 'apple')}
                    disabled={loading === service.id}
                    className={`w-full ${service.color} text-white py-3 rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50 flex items-center justify-center space-x-2`}
                  >
                    {loading === service.id ? (
                      <RefreshCw className="w-4 h-4 animate-spin" />
                    ) : (
                      <ExternalLink className="w-4 h-4" />
                    )}
                    <span>Connect {service.name}</span>
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Help Section */}
        <div className="glass rounded-xl p-6 mt-8">
          <h2 className="text-xl font-bold text-white mb-4">Need Help?</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-white font-medium mb-2">Connection Issues?</h3>
              <p className="text-gray-300 text-sm mb-3">
                Make sure you're logged into your music service and have granted the necessary permissions.
              </p>
              <button className="text-green-500 hover:text-green-400 text-sm flex items-center space-x-1">
                <ExternalLink className="w-4 h-4" />
                <span>View Troubleshooting Guide</span>
              </button>
            </div>
            <div>
              <h3 className="text-white font-medium mb-2">Privacy & Security</h3>
              <p className="text-gray-300 text-sm mb-3">
                We only access your public playlists and never store your login credentials.
              </p>
              <button className="text-green-500 hover:text-green-400 text-sm flex items-center space-x-1">
                <ExternalLink className="w-4 h-4" />
                <span>Read Privacy Policy</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}