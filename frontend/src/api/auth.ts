/**
 * Authentication API client
 */
import axios from 'axios'

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
  const response = await axios.post(`${API_URL}/auth/register`, data)
  return response.data
}

export async function login(credentials: UserLogin): Promise<TokenResponse> {
  const response = await axios.post(`${API_URL}/auth/login`, credentials)
  return response.data
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
