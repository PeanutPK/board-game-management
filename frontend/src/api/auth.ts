/**
 * Authentication API client
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export interface UserLogin {
  username: string
  password: string
}

export interface UserRegister {
  email: string
  username: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export async function register(data: UserRegister): Promise<TokenResponse> {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })

  if (!response.ok) {
    throw new Error('Registration failed')
  }

  return response.json()
}

export async function login(credentials: UserLogin): Promise<TokenResponse> {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
  })

  if (!response.ok) {
    throw new Error('Login failed')
  }

  return response.json()
}

export function saveToken(token: string): void {
  localStorage.setItem('access_token', token)
}

export function getToken(): string | null {
  return localStorage.getItem('access_token')
}

export function clearToken(): void {
  localStorage.removeItem('access_token')
}

export function logout(): void {
  clearToken()
}