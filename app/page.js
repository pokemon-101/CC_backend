export default function Home() {
  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui' }}>
      <h1>ChordCircle API</h1>
      <p>Backend API for ChordCircle music platform integration</p>
      <div style={{ marginTop: '2rem' }}>
        <h2>Available Endpoints:</h2>
        <ul>
          <li><code>GET /api/health</code> - Health check</li>
          <li><code>GET /api/v1/health</code> - API v1 health check</li>
          <li><code>POST /api/v1/auth/login</code> - User login</li>
          <li><code>GET /api/v1/music/playlists</code> - Get playlists (requires auth)</li>
          <li><code>POST /api/v1/music/playlists</code> - Create playlist (requires auth)</li>
        </ul>
      </div>
      <div style={{ marginTop: '2rem', padding: '1rem', backgroundColor: '#f5f5f5', borderRadius: '4px' }}>
        <h3>Test Login:</h3>
        <p>Email: test@example.com</p>
        <p>Password: password123</p>
      </div>
    </div>
  )
}