import { useState } from 'react'
import { User, Edit, Settings, Music, Users, Calendar, Mail, MapPin, Link } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'

export function Profile() {
  const { user } = useAuth()
  const [isEditing, setIsEditing] = useState(false)
  const [profileData, setProfileData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    bio: 'Music lover and playlist curator. Always discovering new sounds!',
    location: 'San Francisco, CA',
    website: 'https://mymusic.blog'
  })

  const handleSave = () => {
    // Here you would typically save to your backend
    setIsEditing(false)
  }

  const stats = [
    { label: 'Playlists Created', value: '24', icon: Music },
    { label: 'Friends', value: '156', icon: Users },
    { label: 'Songs Shared', value: '1,234', icon: Music },
    { label: 'Days Active', value: '89', icon: Calendar },
  ]

  const recentActivity = [
    {
      id: '1',
      action: 'Created playlist "Summer Vibes 2025"',
      time: '2 hours ago',
      type: 'playlist'
    },
    {
      id: '2',
      action: 'Added 5 songs to "Workout Mix"',
      time: '1 day ago',
      type: 'music'
    },
    {
      id: '3',
      action: 'Connected with Sarah Johnson',
      time: '3 days ago',
      type: 'friend'
    },
    {
      id: '4',
      action: 'Shared "Chill Beats" with 12 friends',
      time: '1 week ago',
      type: 'share'
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-900 to-green-900 pt-20 pb-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Profile Header */}
        <div className="glass rounded-xl p-8 mb-8">
          <div className="flex flex-col md:flex-row items-start md:items-center space-y-6 md:space-y-0 md:space-x-8">
            {/* Avatar */}
            <div className="relative">
              <div className="w-32 h-32 bg-gradient-to-br from-green-500 to-blue-500 rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-4xl">
                  {user?.name?.charAt(0) || 'U'}
                </span>
              </div>
              <button className="absolute bottom-2 right-2 w-8 h-8 bg-green-500 rounded-full flex items-center justify-center text-white hover:bg-green-600 transition-colors">
                <Edit className="w-4 h-4" />
              </button>
            </div>

            {/* Profile Info */}
            <div className="flex-1">
              {isEditing ? (
                <div className="space-y-4">
                  <input
                    type="text"
                    value={profileData.name}
                    onChange={(e) => setProfileData(prev => ({ ...prev, name: e.target.value }))}
                    className="w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    placeholder="Your name"
                  />
                  <textarea
                    value={profileData.bio}
                    onChange={(e) => setProfileData(prev => ({ ...prev, bio: e.target.value }))}
                    className="w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none"
                    rows={3}
                    placeholder="Tell us about yourself..."
                  />
                  <input
                    type="text"
                    value={profileData.location}
                    onChange={(e) => setProfileData(prev => ({ ...prev, location: e.target.value }))}
                    className="w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    placeholder="Location"
                  />
                  <input
                    type="url"
                    value={profileData.website}
                    onChange={(e) => setProfileData(prev => ({ ...prev, website: e.target.value }))}
                    className="w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    placeholder="Website"
                  />
                  <div className="flex space-x-3">
                    <button
                      onClick={handleSave}
                      className="bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600 transition-colors"
                    >
                      Save Changes
                    </button>
                    <button
                      onClick={() => setIsEditing(false)}
                      className="px-6 py-2 border border-gray-600 text-gray-300 rounded-lg hover:bg-gray-600 hover:text-white transition-colors"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <h1 className="text-3xl font-bold text-white">{profileData.name}</h1>
                    <button
                      onClick={() => setIsEditing(true)}
                      className="text-gray-400 hover:text-white transition-colors"
                    >
                      <Edit className="w-5 h-5" />
                    </button>
                  </div>
                  <p className="text-gray-300 mb-4">{profileData.bio}</p>
                  <div className="flex flex-wrap gap-4 text-sm text-gray-400">
                    <div className="flex items-center space-x-1">
                      <Mail className="w-4 h-4" />
                      <span>{profileData.email}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <MapPin className="w-4 h-4" />
                      <span>{profileData.location}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Link className="w-4 h-4" />
                      <a href={profileData.website} className="text-green-400 hover:text-green-300 transition-colors">
                        {profileData.website}
                      </a>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Calendar className="w-4 h-4" />
                      <span>Joined January 2025</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
          {stats.map((stat) => (
            <div key={stat.label} className="glass rounded-xl p-6 text-center">
              <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-3">
                <stat.icon className="w-6 h-6 text-white" />
              </div>
              <p className="text-2xl font-bold text-white mb-1">{stat.value}</p>
              <p className="text-gray-300 text-sm">{stat.label}</p>
            </div>
          ))}
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Recent Activity */}
          <div className="lg:col-span-2">
            <div className="glass rounded-xl p-6">
              <h2 className="text-xl font-bold text-white mb-6">Recent Activity</h2>
              <div className="space-y-4">
                {recentActivity.map((activity) => (
                  <div key={activity.id} className="flex items-center space-x-4 p-3 rounded-lg hover:bg-white/5 transition-colors">
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                      activity.type === 'playlist' ? 'bg-green-500' :
                      activity.type === 'music' ? 'bg-purple-500' :
                      activity.type === 'friend' ? 'bg-blue-500' : 'bg-orange-500'
                    }`}>
                      {activity.type === 'playlist' && <Music className="w-5 h-5 text-white" />}
                      {activity.type === 'music' && <Music className="w-5 h-5 text-white" />}
                      {activity.type === 'friend' && <Users className="w-5 h-5 text-white" />}
                      {activity.type === 'share' && <Link className="w-5 h-5 text-white" />}
                    </div>
                    <div className="flex-1">
                      <p className="text-white">{activity.action}</p>
                      <p className="text-gray-400 text-sm">{activity.time}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Settings & Preferences */}
          <div className="space-y-6">
            <div className="glass rounded-xl p-6">
              <h2 className="text-xl font-bold text-white mb-4 flex items-center">
                <Settings className="w-5 h-5 mr-2" />
                Settings
              </h2>
              <div className="space-y-3">
                <button className="w-full text-left text-gray-300 hover:text-white transition-colors py-2">
                  Privacy Settings
                </button>
                <button className="w-full text-left text-gray-300 hover:text-white transition-colors py-2">
                  Notification Preferences
                </button>
                <button className="w-full text-left text-gray-300 hover:text-white transition-colors py-2">
                  Connected Accounts
                </button>
                <button className="w-full text-left text-gray-300 hover:text-white transition-colors py-2">
                  Data & Privacy
                </button>
              </div>
            </div>

            <div className="glass rounded-xl p-6">
              <h2 className="text-xl font-bold text-white mb-4">Music Preferences</h2>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-gray-300">Auto-sync playlists</span>
                  <div className="w-12 h-6 bg-green-500 rounded-full relative">
                    <div className="w-5 h-5 bg-white rounded-full absolute top-0.5 right-0.5"></div>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-300">Share activity</span>
                  <div className="w-12 h-6 bg-gray-600 rounded-full relative">
                    <div className="w-5 h-5 bg-white rounded-full absolute top-0.5 left-0.5"></div>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-300">Friend notifications</span>
                  <div className="w-12 h-6 bg-green-500 rounded-full relative">
                    <div className="w-5 h-5 bg-white rounded-full absolute top-0.5 right-0.5"></div>
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