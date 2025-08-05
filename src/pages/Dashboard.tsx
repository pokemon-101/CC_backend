import { useState, useEffect } from 'react'
import { Music, Users, List, TrendingUp, Play, Heart } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { Track } from '../types'

export function Dashboard() {
  const { user } = useAuth()
  const [recentTracks, setRecentTracks] = useState<Track[]>([])

  useEffect(() => {
    // Mock recent tracks data
    setRecentTracks([
      {
        id: '1',
        name: 'Blinding Lights',
        artist: 'The Weeknd',
        album: 'After Hours',
        duration: 200,
        image: 'https://via.placeholder.com/60x60/1DB954/ffffff?text=BL'
      },
      {
        id: '2',
        name: 'Watermelon Sugar',
        artist: 'Harry Styles',
        album: 'Fine Line',
        duration: 174,
        image: 'https://via.placeholder.com/60x60/1DB954/ffffff?text=WS'
      },
      {
        id: '3',
        name: 'Levitating',
        artist: 'Dua Lipa',
        album: 'Future Nostalgia',
        duration: 203,
        image: 'https://via.placeholder.com/60x60/1DB954/ffffff?text=LV'
      }
    ])
  }, [])

  const stats = [
    { label: 'Playlists', value: '12', icon: List, color: 'bg-blue-500' },
    { label: 'Friends', value: '48', icon: Users, color: 'bg-green-500' },
    { label: 'Tracks', value: '1,234', icon: Music, color: 'bg-purple-500' },
    { label: 'Hours Listened', value: '156', icon: TrendingUp, color: 'bg-orange-500' },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-900 to-green-900 pt-20 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">
            Welcome back, {user?.name}! 👋
          </h1>
          <p className="text-gray-300">
            Here's what's happening with your music today
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat) => (
            <div key={stat.label} className="glass rounded-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-300 text-sm">{stat.label}</p>
                  <p className="text-2xl font-bold text-white">{stat.value}</p>
                </div>
                <div className={`w-12 h-12 ${stat.color} rounded-lg flex items-center justify-center`}>
                  <stat.icon className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Recent Activity */}
          <div className="lg:col-span-2">
            <div className="glass rounded-xl p-6">
              <h2 className="text-xl font-bold text-white mb-6 flex items-center">
                <Music className="w-5 h-5 mr-2" />
                Recently Played
              </h2>
              <div className="space-y-4">
                {recentTracks.map((track) => (
                  <div key={track.id} className="flex items-center space-x-4 p-3 rounded-lg hover:bg-white/5 transition-colors">
                    <img
                      src={track.image}
                      alt={track.name}
                      className="w-12 h-12 rounded-lg"
                    />
                    <div className="flex-1 min-w-0">
                      <p className="text-white font-medium truncate">{track.name}</p>
                      <p className="text-gray-300 text-sm truncate">{track.artist}</p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <button className="text-gray-400 hover:text-white transition-colors">
                        <Heart className="w-4 h-4" />
                      </button>
                      <button className="text-gray-400 hover:text-green-500 transition-colors">
                        <Play className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="space-y-6">
            <div className="glass rounded-xl p-6">
              <h2 className="text-xl font-bold text-white mb-4">Quick Actions</h2>
              <div className="space-y-3">
                <button className="w-full bg-green-500 text-white py-3 rounded-lg hover:bg-green-600 transition-colors flex items-center justify-center space-x-2">
                  <List className="w-4 h-4" />
                  <span>Create Playlist</span>
                </button>
                <button className="w-full bg-blue-500 text-white py-3 rounded-lg hover:bg-blue-600 transition-colors flex items-center justify-center space-x-2">
                  <Users className="w-4 h-4" />
                  <span>Find Friends</span>
                </button>
                <button className="w-full bg-purple-500 text-white py-3 rounded-lg hover:bg-purple-600 transition-colors flex items-center justify-center space-x-2">
                  <Music className="w-4 h-4" />
                  <span>Sync Music</span>
                </button>
              </div>
            </div>

            {/* Friend Activity */}
            <div className="glass rounded-xl p-6">
              <h2 className="text-xl font-bold text-white mb-4">Friend Activity</h2>
              <div className="space-y-3">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-bold">J</span>
                  </div>
                  <div className="flex-1">
                    <p className="text-white text-sm">John added 3 songs</p>
                    <p className="text-gray-400 text-xs">2 hours ago</p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-bold">S</span>
                  </div>
                  <div className="flex-1">
                    <p className="text-white text-sm">Sarah created a playlist</p>
                    <p className="text-gray-400 text-xs">5 hours ago</p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-bold">M</span>
                  </div>
                  <div className="flex-1">
                    <p className="text-white text-sm">Mike liked your playlist</p>
                    <p className="text-gray-400 text-xs">1 day ago</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}