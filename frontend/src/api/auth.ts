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
  username: string
  user_role: string
}

export async function register(data: UserRegister): Promise<TokenResponse> {
  const response = await axios.post(`${API_URL}/auth/register`, data)
  return response.data
}

export async function login(credentials: UserLogin): Promise<TokenResponse> {
  const response = await axios.post(`${API_URL}/auth/login`, credentials)
  return response.data
}

export async function saveUserData(tokenResponse: TokenResponse): Promise<void> {
  saveToken(tokenResponse.access_token)
  saveUsername(tokenResponse.username)
  saveRole(tokenResponse.user_role)
}

export function saveToken(token: string): void {
  localStorage.setItem('access_token', token)
}

export function getToken(): string | null {
  return localStorage.getItem('access_token')
}

export function saveRole(role: string): void {
  localStorage.setItem('user_role', role)
}

export function getRole(): string | null {
  return localStorage.getItem('user_role')
}

export function saveUsername(username: string): void {
  localStorage.setItem('username', username)
}

export function getUsername(): string | null {
  return localStorage.getItem('username')
}

export function clearToken(): void {
  localStorage.removeItem('access_token')
}

export function logout(): void {
  clearToken()
  localStorage.removeItem('user_role')
  localStorage.removeItem('username')
}
