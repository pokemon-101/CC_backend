import jwt from 'jsonwebtoken'
import bcrypt from 'bcryptjs'

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key'

export async function POST(request) {
  try {
    const { email, password } = await request.json()
    
    // TODO: Replace with actual database lookup
    const mockUser = {
      id: 1,
      email: 'test@example.com',
      password: await bcrypt.hash('password123', 10) // hashed 'password123'
    }
    
    if (email !== mockUser.email) {
      return Response.json(
        { error: 'Invalid credentials' },
        { status: 401 }
      )
    }
    
    const isValidPassword = await bcrypt.compare(password, mockUser.password)
    if (!isValidPassword) {
      return Response.json(
        { error: 'Invalid credentials' },
        { status: 401 }
      )
    }
    
    const token = jwt.sign(
      { userId: mockUser.id, email: mockUser.email },
      JWT_SECRET,
      { expiresIn: '24h' }
    )
    
    return Response.json({
      message: 'Login successful',
      token,
      user: {
        id: mockUser.id,
        email: mockUser.email
      }
    })
    
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