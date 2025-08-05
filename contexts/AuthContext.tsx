'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import axios from 'axios'
import type { User, AuthContextType, ApiResponse, AuthUser } from '@/types'
import { toast } from '@/components/ui/Toaster'

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check for stored auth data on mount
    const storedToken = localStorage.getItem('auth_token')
    const storedUser = localStorage.getItem('auth_user')
    
    if (storedToken && storedUser) {
      try {
        setToken(storedToken)
        setUser(JSON.parse(storedUser))
      } catch (error) {
        console.error('Error parsing stored user data:', error)
        localStorage.removeItem('auth_token')
        localStorage.removeItem('auth_user')
      }
    }
    
    setLoading(false)
  }, [])

  const login = async (email: string, password: string) => {
    try {
      setLoading(true)
      const response = await axios.post<ApiResponse<AuthUser>>('/api/v1/auth/login', {
        email,
        password
      })

      if (response.data.success && response.data.data) {
        const { user: userData, token: userToken } = response.data.data
        
        setUser(userData)
        setToken(userToken)
        
        localStorage.setItem('auth_token', userToken)
        localStorage.setItem('auth_user', JSON.stringify(userData))
        
        toast.success('Login successful!')
      } else {
        throw new Error(response.data.error || 'Login failed')
      }
    } catch (error: any) {
      const message = error.response?.data?.error || error.message || 'Login failed'
      toast.error(message)
      throw error
    } finally {
      setLoading(false)
    }
  }

  const register = async (email: string, password: string, name: string) => {
    try {
      setLoading(true)
      const response = await axios.post<ApiResponse<AuthUser>>('/api/v1/auth/register', {
        email,
        password,
        name
      })

      if (response.data.success && response.data.data) {
        const { user: userData, token: userToken } = response.data.data
        
        setUser(userData)
        setToken(userToken)
        
        localStorage.setItem('auth_token', userToken)
        localStorage.setItem('auth_user', JSON.stringify(userData))
        
        toast.success('Registration successful!')
      } else {
        throw new Error(response.data.error || 'Registration failed')
      }
    } catch (error: any) {
      const message = error.response?.data?.error || error.message || 'Registration failed'
      toast.error(message)
      throw error
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    localStorage.removeItem('auth_token')
    localStorage.removeItem('auth_user')
    toast.success('Logged out successfully')
  }

  const value: AuthContextType = {
    user,
    token,
    login,
    register,
    logout,
    loading
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}