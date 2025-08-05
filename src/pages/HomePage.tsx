import { useState, useEffect } from 'react'
import { Music, Users, Zap, Shield } from 'lucide-react'

interface HomePageProps {
  onGetStarted: () => void
}

export function HomePage({ onGetStarted }: HomePageProps) {
  const [isLoaded, setIsLoaded] = useState(false)

  useEffect(() => {
    setIsLoaded(true)
  }, [])

  const features = [
    {
      icon: Music,
      title: 'Cross-Platform Sync',
      description: 'Seamlessly sync your playlists between Spotify and Apple Music'
    },
    {
      icon: Users,
      title: 'Social Sharing',
      description: 'Share your favorite tracks and discover new music with friends'
    },
    {
      icon: Zap,
      title: 'Real-time Updates',
      description: 'Get instant notifications when friends add new music'
    },
    {
      icon: Shield,
      title: 'Secure & Private',
      description: 'Your music data is encrypted and never shared without permission'
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-900 to-green-900">
      {/* Hero Section */}
      <section className="relative pt-32 pb-20 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <div className={`transition-all duration-1000 ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
            <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
              Connect Your{' '}
              <span className="gradient-text">Music</span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Seamlessly sync and share your music across Spotify and Apple Music. 
              Discover new tracks with friends and never lose your favorite playlists again.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button 
                onClick={onGetStarted}
                className="bg-green-500 text-white px-8 py-4 rounded-lg text-lg hover:bg-green-600 transition-colors transform hover:scale-105"
              >
                Get Started Free
              </button>
              <button className="border border-white text-white px-8 py-4 rounded-lg text-lg hover:bg-white hover:text-gray-900 transition-colors transform hover:scale-105">
                Watch Demo
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Why Choose ChordCircle?
            </h2>
            <p className="text-xl text-gray-300 max-w-2xl mx-auto">
              Experience the future of music sharing with our cutting-edge platform
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div
                key={feature.title}
                className={`glass rounded-2xl p-6 text-center hover:scale-105 transition-all duration-500 opacity-0 translate-y-8 ${
                  isLoaded ? 'animate-fade-in-up' : ''
                }`}
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <feature.icon className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-300">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className={`glass rounded-3xl p-12 transition-all duration-1000 ${
            isLoaded ? 'opacity-100 scale-100' : 'opacity-0 scale-95'
          }`}>
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Ready to Connect?
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              Join thousands of music lovers who have already connected their accounts
            </p>
            <button 
              onClick={onGetStarted}
              className="bg-green-500 text-white px-12 py-4 rounded-lg text-lg hover:bg-green-600 transition-colors transform hover:scale-105"
            >
              Start Your Journey
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-black/50 py-8 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <div className="w-6 h-6 bg-green-500 rounded flex items-center justify-center">
              <Music className="w-4 h-4 text-white" />
            </div>
            <span className="text-lg font-bold text-white">ChordCircle</span>
          </div>
          <p className="text-gray-400">
            © 2025 ChordCircle. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  )
}