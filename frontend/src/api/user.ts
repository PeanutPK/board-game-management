/**
 * User management API
 */
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export interface User {
  id: number
  username: string
  email: string
  is_staff: boolean
  is_admin: boolean
}

export interface UserCreateInput {
  email: string
  username: string
  password: string
  is_staff?: boolean
  is_admin?: boolean
}

export interface UserUpdateInput {
  email?: string
  username?: string
  password?: string
  is_staff?: boolean
  is_admin?: boolean
}

export async function getUserProfiles(): Promise<User[]> {
  const token = localStorage.getItem('access_token')
  if (!token) {
    throw new Error('No access token found')
  }

  const response = await axios.get(`${API_URL}/users`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  return response.data
}

export async function createUser(data: UserCreateInput): Promise<User> {
  const token = localStorage.getItem('access_token')
  if (!token) {
    throw new Error('No access token found')
  }

  const response = await axios.post(`${API_URL}/users`, data, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  return response.data
}

export async function updateUser(userId: number, data: UserUpdateInput): Promise<User> {
  const token = localStorage.getItem('access_token')
  if (!token) {
    throw new Error('No access token found')
  }

  const response = await axios.put(`${API_URL}/users/${userId}`, data, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  return response.data
}

export async function deleteUser(userId: number): Promise<void> {
  const token = localStorage.getItem('access_token')
  if (!token) {
    throw new Error('No access token found')
  }

  await axios.delete(`${API_URL}/users/${userId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
}

export async function updateUserProfile(data: Partial<UserUpdateInput>): Promise<User> {
  return updateUser(0, data)
}

export async function deleteUserAccount(): Promise<void> {
  return deleteUser(0)
}
