import { NextRequest, NextResponse } from 'next/server'
import jwt from 'jsonwebtoken'
import bcrypt from 'bcryptjs'
import type { RegisterRequest, ApiResponse, AuthUser } from '@/types'

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production'

// Mock user database - replace with real database
const mockUsers: any[] = []

export async function POST(request: NextRequest) {
  try {
    const body: RegisterRequest = await request.json()
    const { email, password, name } = body

    if (!email || !password || !name) {
      return NextResponse.json<ApiResponse>({
        success: false,
        error: 'Email, password, and name are required'
      }, { status: 400 })
    }

    // Check if user already exists
    const existingUser = mockUsers.find(u => u.email === email)
    if (existingUser) {
      return NextResponse.json<ApiResponse>({
        success: false,
        error: 'User already exists'
      }, { status: 409 })
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10)

    // Create new user
    const newUser = {
      id: Date.now().toString(),
      email,
      name,
      password: hashedPassword,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }

    mockUsers.push(newUser)

    // Generate JWT token
    const token = jwt.sign(
      { 
        userId: newUser.id, 
        email: newUser.email 
      },
      JWT_SECRET,
      { expiresIn: '24h' }
    )

    const authUser: AuthUser = {
      user: {
        id: newUser.id,
        email: newUser.email,
        name: newUser.name,
        createdAt: newUser.createdAt,
        updatedAt: newUser.updatedAt
      },
      token
    }

    return NextResponse.json<ApiResponse<AuthUser>>({
      success: true,
      data: authUser,
      message: 'Registration successful'
    }, { status: 201 })

  } catch (error) {
    console.error('Registration error:', error)
    return NextResponse.json<ApiResponse>({
      success: false,
      error: 'Internal server error'
    }, { status: 500 })
  }
}

export async function OPTIONS() {
  return new NextResponse(null, { status: 200 })
}