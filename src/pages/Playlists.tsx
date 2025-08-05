import { useState, useEffect } from 'react'
import { List, Plus, Play, Heart, Share, MoreHorizontal, Music } from 'lucide-react'
import { Playlist } from '../types'
import { useAuth } from '../contexts/AuthContext'

export function Playlists() {
  const { user } = useAuth()
  const [playlists, setPlaylists] = useState<Playlist[]>([])
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [newPlaylistName, setNewPlaylistName] = useState('')

  useEffect(() => {
    // Mock playlists data
    setPlaylists([
      {
        id: '1',
        name: 'My Favorites',
        description: 'All my favorite songs in one place',
        tracks: [],
        owner: user!,
        isPublic: true,
        createdAt: '2025-01-01T00:00:00Z'
      },
      {
        id: '2',
        name: 'Workout Mix',
        description: 'High energy songs for the gym',
        tracks: [],
        owner: user!,
        isPublic: false,
        createdAt: '2025-01-02T00:00:00Z'
      },
      {
        id: '3',
        name: 'Chill Vibes',
        description: 'Relaxing music for studying',
        tracks: [],
        owner: user!,
        isPublic: true,
        createdAt: '2025-01-03T00:00:00Z'
      }
    ])
  }, [user])

  const handleCreatePlaylist = () => {
    if (newPlaylistName.trim()) {
      const newPlaylist: Playlist = {
        id: Date.now().toString(),
        name: newPlaylistName,
        description: '',
        tracks: [],
        owner: user!,
        isPublic: false,
        createdAt: new Date().toISOString()
      }
      setPlaylists(prev => [newPlaylist, ...prev])
      setNewPlaylistName('')
      setShowCreateModal(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-900 to-green-900 pt-20 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Your Playlists</h1>
            <p className="text-gray-300">Manage and organize your music collections</p>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition-colors flex items-center space-x-2"
          >
            <Plus className="w-5 h-5" />
            <span>Create Playlist</span>
          </button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="glass rounded-xl p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-300 text-sm">Total Playlists</p>
                <p className="text-2xl font-bold text-white">{playlists.length}</p>
              </div>
              <List className="w-8 h-8 text-green-500" />
            </div>
          </div>
          <div className="glass rounded-xl p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-300 text-sm">Public Playlists</p>
                <p className="text-2xl font-bold text-white">
                  {playlists.filter(p => p.isPublic).length}
                </p>
              </div>
              <Share className="w-8 h-8 text-blue-500" />
            </div>
          </div>
          <div className="glass rounded-xl p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-300 text-sm">Total Tracks</p>
                <p className="text-2xl font-bold text-white">
                  {playlists.reduce((acc, p) => acc + p.tracks.length, 0)}
                </p>
              </div>
              <Music className="w-8 h-8 text-purple-500" />
            </div>
          </div>
        </div>

        {/* Playlists Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {playlists.map((playlist) => (
            <div key={playlist.id} className="glass rounded-xl p-6 hover:scale-105 transition-transform">
              <div className="flex items-start justify-between mb-4">
                <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-blue-500 rounded-xl flex items-center justify-center">
                  <List className="w-8 h-8 text-white" />
                </div>
                <button className="text-gray-400 hover:text-white transition-colors">
                  <MoreHorizontal className="w-5 h-5" />
                </button>
              </div>
              
              <h3 className="text-xl font-bold text-white mb-2">{playlist.name}</h3>
              <p className="text-gray-300 text-sm mb-4 line-clamp-2">
                {playlist.description || 'No description'}
              </p>
              
              <div className="flex items-center justify-between text-sm text-gray-400 mb-4">
                <span>{playlist.tracks.length} tracks</span>
                <span className={`px-2 py-1 rounded-full text-xs ${
                  playlist.isPublic 
                    ? 'bg-green-500/20 text-green-400' 
                    : 'bg-gray-500/20 text-gray-400'
                }`}>
                  {playlist.isPublic ? 'Public' : 'Private'}
                </span>
              </div>
              
              <div className="flex items-center space-x-3">
                <button className="flex-1 bg-green-500 text-white py-2 rounded-lg hover:bg-green-600 transition-colors flex items-center justify-center space-x-2">
                  <Play className="w-4 h-4" />
                  <span>Play</span>
                </button>
                <button className="p-2 text-gray-400 hover:text-red-500 transition-colors">
                  <Heart className="w-5 h-5" />
                </button>
                <button className="p-2 text-gray-400 hover:text-blue-500 transition-colors">
                  <Share className="w-5 h-5" />
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Empty State */}
        {playlists.length === 0 && (
          <div className="text-center py-16">
            <List className="w-16 h-16 text-gray-600 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-white mb-2">No playlists yet</h3>
            <p className="text-gray-300 mb-6">Create your first playlist to get started</p>
            <button
              onClick={() => setShowCreateModal(true)}
              className="bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition-colors"
            >
              Create Your First Playlist
            </button>
          </div>
        )}
      </div>

      {/* Create Playlist Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={() => setShowCreateModal(false)} />
          <div className="relative bg-white rounded-2xl p-6 w-full max-w-md">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Create New Playlist</h2>
            <input
              type="text"
              placeholder="Playlist name"
              value={newPlaylistName}
              onChange={(e) => setNewPlaylistName(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent mb-4"
              autoFocus
            />
            <div className="flex space-x-3">
              <button
                onClick={() => setShowCreateModal(false)}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleCreatePlaylist}
                className="flex-1 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
              >
                Create
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}