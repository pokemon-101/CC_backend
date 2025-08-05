import jwt from 'jsonwebtoken'

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key'

function verifyToken(request) {
  const authHeader = request.headers.get('authorization')
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return null
  }
  
  const token = authHeader.substring(7)
  try {
    return jwt.verify(token, JWT_SECRET)
  } catch {
    return null
  }
}

export async function GET(request) {
  const user = verifyToken(request)
  if (!user) {
    return Response.json(
      { error: 'Unauthorized' },
      { status: 401 }
    )
  }
  
  // Mock playlists data
  const playlists = [
    {
      id: 1,
      name: 'My Favorites',
      description: 'My favorite songs',
      tracks_count: 25,
      created_at: '2025-01-01T00:00:00Z'
    },
    {
      id: 2,
      name: 'Workout Mix',
      description: 'High energy songs for workouts',
      tracks_count: 18,
      created_at: '2025-01-15T00:00:00Z'
    }
  ]
  
  return Response.json({
    playlists,
    total: playlists.length
  })
}

export async function POST(request) {
  const user = verifyToken(request)
  if (!user) {
    return Response.json(
      { error: 'Unauthorized' },
      { status: 401 }
    )
  }
  
  try {
    const { name, description } = await request.json()
    
    if (!name) {
      return Response.json(
        { error: 'Playlist name is required' },
        { status: 400 }
      )
    }
    
    // Mock playlist creation
    const newPlaylist = {
      id: Date.now(),
      name,
      description: description || '',
      tracks_count: 0,
      created_at: new Date().toISOString(),
      user_id: user.userId
    }
    
    return Response.json({
      message: 'Playlist created successfully',
      playlist: newPlaylist
    }, { status: 201 })
    
  } catch (error) {
    return Response.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

export async function OPTIONS() {
  return new Response(null, { status: 200 })
}