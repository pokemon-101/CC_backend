export default function HomePage() {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-black p-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-green-500 rounded"></div>
            <span className="text-xl font-bold">ChordCircle</span>
          </div>
          <button className="bg-green-500 text-white px-4 py-2 rounded">
            Get Started
          </button>
        </div>
      </header>
      
      {/* Hero Section */}
      <section className="py-20 px-4 text-center">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-6xl font-bold mb-6">
            Connect Your <span className="text-green-500">Music</span>
          </h1>
          <p className="text-xl text-gray-300 mb-8">
            Seamlessly sync and share your music across Spotify and Apple Music.
          </p>
          <div className="space-x-4">
            <button className="bg-green-500 text-white px-8 py-4 rounded text-lg">
              Get Started Free
            </button>
            <button className="border border-white text-white px-8 py-4 rounded text-lg">
              Watch Demo
            </button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-gray-800">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-6">Why Choose ChordCircle?</h2>
            <p className="text-xl text-gray-300">
              Experience the future of music sharing
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="bg-gray-700 rounded-lg p-6 text-center">
              <div className="w-16 h-16 bg-green-500 rounded-full mx-auto mb-4"></div>
              <h3 className="text-xl font-semibold mb-3">Cross-Platform Sync</h3>
              <p className="text-gray-300">
                Sync playlists between Spotify and Apple Music
              </p>
            </div>
            
            <div className="bg-gray-700 rounded-lg p-6 text-center">
              <div className="w-16 h-16 bg-green-500 rounded-full mx-auto mb-4"></div>
              <h3 className="text-xl font-semibold mb-3">Social Sharing</h3>
              <p className="text-gray-300">
                Share tracks and discover new music with friends
              </p>
            </div>
            
            <div className="bg-gray-700 rounded-lg p-6 text-center">
              <div className="w-16 h-16 bg-green-500 rounded-full mx-auto mb-4"></div>
              <h3 className="text-xl font-semibold mb-3">Real-time Updates</h3>
              <p className="text-gray-300">
                Get instant notifications when friends add music
              </p>
            </div>
            
            <div className="bg-gray-700 rounded-lg p-6 text-center">
              <div className="w-16 h-16 bg-green-500 rounded-full mx-auto mb-4"></div>
              <h3 className="text-xl font-semibold mb-3">Secure & Private</h3>
              <p className="text-gray-300">
                Your data is encrypted and never shared
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="bg-gray-800 rounded-lg p-12">
            <h2 className="text-4xl font-bold mb-6">Ready to Connect?</h2>
            <p className="text-xl text-gray-300 mb-8">
              Join thousands of music lovers who have connected their accounts
            </p>
            <button className="bg-green-500 text-white px-12 py-4 rounded text-lg">
              Start Your Journey
            </button>
          </div>
        </div>
      </section>
    </div>
  )
}