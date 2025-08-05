'use client'

import { useState } from 'react'
import { Header } from '@/components/Header'
import { ParallaxBackground } from '@/components/ParallaxBackground'
import { AuthModal } from '@/components/AuthModal'
import { ConnectionStatus } from '@/components/ConnectionStatus'
import { NotificationCenter } from '@/components/NotificationCenter'
import { Button } from '@/components/ui/Button'
import { Music, Users, Zap, Shield } from 'lucide-react'
import { motion } from 'framer-motion'

export default function HomePage() {
  const [authModalOpen, setAuthModalOpen] = useState(false)

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
    <div className="min-h-screen bg-gradient-to-br from-secondary-900 via-secondary-900 to-primary-900">
      <ParallaxBackground />
      <Header onAuthClick={() => setAuthModalOpen(true)} />
      
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
              <Button
                size="lg"
                onClick={() => setAuthModalOpen(true)}
                className="text-lg px-8 py-4"
              >
                Get Started Free
              </Button>
              <Button
                variant="outline"
                size="lg"
                className="text-lg px-8 py-4 text-white border-white hover:bg-white hover:text-secondary-900"
              >
                Watch Demo
              </Button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Why Choose ChordCircle?
            </h2>
            <p className="text-xl text-gray-300 max-w-2xl mx-auto">
              Experience the future of music sharing with our cutting-edge platform
            </p>
          </motion.div>

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
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="glass rounded-3xl p-12"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Ready to Connect?
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              Join thousands of music lovers who have already connected their accounts
            </p>
            <Button
              size="lg"
              onClick={() => setAuthModalOpen(true)}
              className="text-lg px-12 py-4"
            >
              Start Your Journey
            </Button>
          </motion.div>
        </div>
      </section>

      {/* Status Components */}
      <ConnectionStatus />
      <NotificationCenter />

      {/* Auth Modal */}
      <AuthModal
        isOpen={authModalOpen}
        onClose={() => setAuthModalOpen(false)}
      />
    </div>
  )
}