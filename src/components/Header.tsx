import { useState } from 'react'
import { Music, Menu, X, User, LogOut, Settings, Home, Users, List } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'

interface HeaderProps {
  currentPage: string
  onPageChange: (page: string) => void
  onAuthClick: () => void
}

export function Header({ currentPage, onPageChange, onAuthClick }: HeaderProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const { user, logout } = useAuth()

  const navItems = user ? [
    { id: 'dashboard', name: 'Dashboard', icon: Home },
    { id: 'playlists', name: 'Playlists', icon: List },
    { id: 'friends', name: 'Friends', icon: Users },
    { id: 'profile', name: 'Profile', icon: User },
    { id: 'link-account', name: 'Link Accounts', icon: Settings },
  ] : [
    { id: 'home', name: 'Home', icon: Home },
    { id: 'features', name: 'Features', icon: List },
    { id: 'about', name: 'About', icon: User },
  ]

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-black/20 backdrop-blur-md border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <button
            onClick={() => onPageChange(user ? 'dashboard' : 'home')}
            className="flex items-center space-x-2"
          >
            <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
              <Music className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-white">ChordCircle</span>
          </button>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => onPageChange(item.id)}
                className={`text-gray-300 hover:text-white transition-colors flex items-center space-x-1 ${
                  currentPage === item.id ? 'text-white' : ''
                }`}
              >
                <item.icon className="w-4 h-4" />
                <span>{item.name}</span>
              </button>
            ))}
          </nav>

          {/* Desktop Auth */}
          <div className="hidden md:flex items-center space-x-4">
            {user ? (
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2 text-white">
                  <User className="w-4 h-4" />
                  <span className="text-sm">{user.name}</span>
                </div>
                <button
                  onClick={logout}
                  className="text-white hover:text-gray-300 transition-colors flex items-center space-x-1"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Logout</span>
                </button>
              </div>
            ) : (
              <button
                onClick={onAuthClick}
                className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors"
              >
                Sign In
              </button>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            className="md:hidden text-white"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-white/10">
            <div className="flex flex-col space-y-4">
              {navItems.map((item) => (
                <button
                  key={item.id}
                  onClick={() => {
                    onPageChange(item.id)
                    setMobileMenuOpen(false)
                  }}
                  className={`text-gray-300 hover:text-white transition-colors flex items-center space-x-2 ${
                    currentPage === item.id ? 'text-white' : ''
                  }`}
                >
                  <item.icon className="w-4 h-4" />
                  <span>{item.name}</span>
                </button>
              ))}
              
              <div className="pt-4 border-t border-white/10">
                {user ? (
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2 text-white">
                      <User className="w-4 h-4" />
                      <span className="text-sm">{user.name}</span>
                    </div>
                    <button
                      onClick={() => {
                        logout()
                        setMobileMenuOpen(false)
                      }}
                      className="text-white hover:text-gray-300 transition-colors flex items-center space-x-2 w-full"
                    >
                      <LogOut className="w-4 h-4" />
                      <span>Logout</span>
                    </button>
                  </div>
                ) : (
                  <button
                    onClick={() => {
                      onAuthClick()
                      setMobileMenuOpen(false)
                    }}
                    className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors w-full"
                  >
                    Sign In
                  </button>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </header>
  )
}