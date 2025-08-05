import { useState, useEffect } from 'react'
import { Users, UserPlus, Search, Music, MessageCircle, MoreHorizontal } from 'lucide-react'

interface Friend {
  id: string
  name: string
  email: string
  avatar?: string
  isOnline: boolean
  recentActivity: string
  mutualFriends: number
}

export function Friends() {
  const [friends, setFriends] = useState<Friend[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [activeTab, setActiveTab] = useState<'friends' | 'discover'>('friends')

  useEffect(() => {
    // Mock friends data
    setFriends([
      {
        id: '1',
        name: 'John Smith',
        email: 'john@example.com',
        isOnline: true,
        recentActivity: 'Added 3 songs to "Road Trip Vibes"',
        mutualFriends: 5
      },
      {
        id: '2',
        name: 'Sarah Johnson',
        email: 'sarah@example.com',
        isOnline: false,
        recentActivity: 'Created playlist "Study Session"',
        mutualFriends: 8
      },
      {
        id: '3',
        name: 'Mike Wilson',
        email: 'mike@example.com',
        isOnline: true,
        recentActivity: 'Liked your playlist "Workout Mix"',
        mutualFriends: 3
      }
    ])
  }, [])

  const filteredFriends = friends.filter(friend =>
    friend.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    friend.email.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const suggestedFriends = [
    {
      id: '4',
      name: 'Emma Davis',
      email: 'emma@example.com',
      mutualFriends: 12,
      reason: 'Mutual friends with John and Sarah'
    },
    {
      id: '5',
      name: 'Alex Chen',
      email: 'alex@example.com',
      mutualFriends: 7,
      reason: 'Similar music taste'
    },
    {
      id: '6',
      name: 'Lisa Brown',
      email: 'lisa@example.com',
      mutualFriends: 4,
      reason: 'From your contacts'
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-900 to-green-900 pt-20 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Friends</h1>
            <p className="text-gray-300">Connect with friends and discover new music together</p>
          </div>
          <button className="bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition-colors flex items-center space-x-2">
            <UserPlus className="w-5 h-5" />
            <span>Add Friends</span>
          </button>
        </div>

        {/* Search Bar */}
        <div className="relative mb-8">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            placeholder="Search friends..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:ring-2 focus:ring-green-500 focus:border-transparent"
          />
        </div>

        {/* Tabs */}
        <div className="flex space-x-1 mb-8">
          <button
            onClick={() => setActiveTab('friends')}
            className={`px-6 py-3 rounded-lg font-medium transition-colors ${
              activeTab === 'friends'
                ? 'bg-green-500 text-white'
                : 'text-gray-300 hover:text-white hover:bg-white/10'
            }`}
          >
            My Friends ({friends.length})
          </button>
          <button
            onClick={() => setActiveTab('discover')}
            className={`px-6 py-3 rounded-lg font-medium transition-colors ${
              activeTab === 'discover'
                ? 'bg-green-500 text-white'
                : 'text-gray-300 hover:text-white hover:bg-white/10'
            }`}
          >
            Discover People
          </button>
        </div>

        {activeTab === 'friends' ? (
          <div>
            {/* Friends Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="glass rounded-xl p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-300 text-sm">Total Friends</p>
                    <p className="text-2xl font-bold text-white">{friends.length}</p>
                  </div>
                  <Users className="w-8 h-8 text-green-500" />
                </div>
              </div>
              <div className="glass rounded-xl p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-300 text-sm">Online Now</p>
                    <p className="text-2xl font-bold text-white">
                      {friends.filter(f => f.isOnline).length}
                    </p>
                  </div>
                  <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                    <div className="w-3 h-3 bg-white rounded-full"></div>
                  </div>
                </div>
              </div>
              <div className="glass rounded-xl p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-300 text-sm">Shared Playlists</p>
                    <p className="text-2xl font-bold text-white">12</p>
                  </div>
                  <Music className="w-8 h-8 text-purple-500" />
                </div>
              </div>
            </div>

            {/* Friends List */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredFriends.map((friend) => (
                <div key={friend.id} className="glass rounded-xl p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <div className="relative">
                        <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-blue-500 rounded-full flex items-center justify-center">
                          <span className="text-white font-bold">
                            {friend.name.charAt(0)}
                          </span>
                        </div>
                        {friend.isOnline && (
                          <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-gray-900"></div>
                        )}
                      </div>
                      <div>
                        <h3 className="text-white font-bold">{friend.name}</h3>
                        <p className="text-gray-400 text-sm">{friend.email}</p>
                      </div>
                    </div>
                    <button className="text-gray-400 hover:text-white transition-colors">
                      <MoreHorizontal className="w-5 h-5" />
                    </button>
                  </div>

                  <div className="mb-4">
                    <p className="text-gray-300 text-sm">{friend.recentActivity}</p>
                    <p className="text-gray-500 text-xs mt-1">
                      {friend.mutualFriends} mutual friends
                    </p>
                  </div>

                  <div className="flex space-x-2">
                    <button className="flex-1 bg-green-500 text-white py-2 rounded-lg hover:bg-green-600 transition-colors flex items-center justify-center space-x-2">
                      <Music className="w-4 h-4" />
                      <span>View Music</span>
                    </button>
                    <button className="p-2 text-gray-400 hover:text-blue-500 transition-colors">
                      <MessageCircle className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {filteredFriends.length === 0 && (
              <div className="text-center py-16">
                <Users className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                <h3 className="text-xl font-bold text-white mb-2">
                  {searchQuery ? 'No friends found' : 'No friends yet'}
                </h3>
                <p className="text-gray-300 mb-6">
                  {searchQuery 
                    ? 'Try a different search term'
                    : 'Start connecting with friends to share music'
                  }
                </p>
                <button className="bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition-colors">
                  Find Friends
                </button>
              </div>
            )}
          </div>
        ) : (
          <div>
            {/* Suggested Friends */}
            <div className="mb-8">
              <h2 className="text-xl font-bold text-white mb-6">People You May Know</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {suggestedFriends.map((person) => (
                  <div key={person.id} className="glass rounded-xl p-6">
                    <div className="text-center mb-4">
                      <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-3">
                        <span className="text-white font-bold text-xl">
                          {person.name.charAt(0)}
                        </span>
                      </div>
                      <h3 className="text-white font-bold">{person.name}</h3>
                      <p className="text-gray-400 text-sm">{person.email}</p>
                    </div>

                    <div className="text-center mb-4">
                      <p className="text-gray-300 text-sm">{person.reason}</p>
                      <p className="text-gray-500 text-xs mt-1">
                        {person.mutualFriends} mutual friends
                      </p>
                    </div>

                    <div className="flex space-x-2">
                      <button className="flex-1 bg-green-500 text-white py-2 rounded-lg hover:bg-green-600 transition-colors">
                        Add Friend
                      </button>
                      <button className="px-4 py-2 border border-gray-600 text-gray-300 rounded-lg hover:bg-gray-600 hover:text-white transition-colors">
                        View
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}