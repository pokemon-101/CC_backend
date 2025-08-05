'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Music, Users, Zap, Shield, Menu, X } from 'lucide-react'

export default function HomePage() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

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
    <div className="min-h-screen bg-gradient-to-br from-secondary-900 via-secondary-900 to-primary-500">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-40 bg-black/20 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
                <Music className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white">ChordCircle</span>
            </div>

            <nav className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-gray-300 hover:text-white transition-colors">Features</a>
              <a href="#about" className="text-gray-300 hover:text-white transition-colors">About</a>
              <a href="#contact" className="text-gray-300 hover:text-white transition-colors">Contact</a>
            </nav>

            <div className="hidden md:flex items-center space-x-4">
              <button className="bg-primary-500 text-white px-4 py-2 rounded-lg hover:bg-primary-600 transition-colors">
                Get Started
              </button>
            </div>

            <button
              className="md:hidden text-white"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

          {mobileMenuOpen && (
            <div className="md:hidden py-4 border-t border-white/10">
              <div className="flex flex-col space-y-4">
                <a href="#features" className="text-gray-300 hover:text-white transition-colors">Features</a>
                <a href="#about" className="text-gray-300 hover:text-white transition-colors">About</a>
                <a href="#contact" className="text-gray-300 hover:text-white transition-colors">Contact</a>
                <button className="bg-primary-500 text-white px-4 py-2 rounded-lg hover:bg-primary-600 transition-colors w-full">
                  Get Started
                </button>
              </div>
            </div>
          )}
        </div>
      </header>
      
      {/* Hero Section */}
      <section className="relative pt-32 pb-20 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
              Connect Your{' '}
              <span className="gradient-text">Music</span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Seamlessly sync and share your music across Spotify and Apple Music. 
              Discover new tracks with friends and never lose your favorite playlists again.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-primary-500 text-white px-8 py-4 rounded-lg text-lg hover:bg-primary-600 transition-colors">
                Get Started Free
              </button>
              <button className="border border-white text-white px-8 py-4 rounded-lg text-lg hover:bg-white hover:text-secondary-900 transition-colors">
                Watch Demo
              </button>
            </div>
          </motion.div>
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
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="glass rounded-2xl p-6 text-center hover:scale-105 transition-transform duration-300"
              >
                <div className="w-16 h-16 bg-primary-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <feature.icon className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-300">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="glass rounded-3xl p-12">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Ready to Connect?
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              Join thousands of music lovers who have already connected their accounts
            </p>
            <button className="bg-primary-500 text-white px-12 py-4 rounded-lg text-lg hover:bg-primary-600 transition-colors">
              Start Your Journey
            </button>
          </div>
        </div>
      </section>
    </div>
  )
}