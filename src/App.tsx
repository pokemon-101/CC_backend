import { useState } from 'react'
import { AuthProvider } from './contexts/AuthContext'
import { AccountProvider } from './contexts/AccountContext'
import { Header } from './components/Header'
import { AuthModal } from './components/AuthModal'
import { Dashboard } from './pages/Dashboard'
import { LinkAccount } from './pages/LinkAccount'
import { HomePage } from './pages/HomePage'
import { Playlists } from './pages/Playlists'
import { Friends } from './pages/Friends'
import { Profile } from './pages/Profile'

function App() {
  const [currentPage, setCurrentPage] = useState('home')
  const [authModalOpen, setAuthModalOpen] = useState(false)

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />
      case 'playlists':
        return <Playlists />
      case 'friends':
        return <Friends />
      case 'profile':
        return <Profile />
      case 'link-account':
        return <LinkAccount />
      default:
        return <HomePage onGetStarted={() => setAuthModalOpen(true)} />
    }
  }

  return (
    <AuthProvider>
      <AccountProvider>
        <div className="min-h-screen">
          <Header
            currentPage={currentPage}
            onPageChange={setCurrentPage}
            onAuthClick={() => setAuthModalOpen(true)}
          />
          
          {renderPage()}

          <AuthModal
            isOpen={authModalOpen}
            onClose={() => setAuthModalOpen(false)}
          />
        </div>
      </AccountProvider>
    </AuthProvider>
  )
}

export default App