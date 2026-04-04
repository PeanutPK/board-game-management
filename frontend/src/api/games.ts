/**
 * Games API client
 */

import { getToken } from './auth'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export interface Game {
  id: number
  title: string
  description: string
  price: number
  stock: number
  is_available: boolean
}

export interface GameCreate {
  title: string
  description: string
  price: number
  stock: number
}

function getHeaders() {
  const token = getToken()
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` })
  }
}

export async function getGames(skip: number = 0, limit: number = 10): Promise<Game[]> {
  const response = await fetch(`${API_URL}/games/?skip=${skip}&limit=${limit}`, {
    headers: getHeaders()
  })

  if (!response.ok) {
    throw new Error('Failed to fetch games')
  }

  return response.json()
}

export async function getGame(id: number): Promise<Game> {
  const response = await fetch(`${API_URL}/games/${id}`, {
    headers: getHeaders()
  })

  if (!response.ok) {
    throw new Error('Failed to fetch game')
  }

  return response.json()
}

export async function createGame(game: GameCreate): Promise<Game> {
  const response = await fetch(`${API_URL}/games/`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(game)
  })

  if (!response.ok) {
    throw new Error('Failed to create game')
  }

  return response.json()
}

export async function updateGame(id: number, game: Partial<GameCreate>): Promise<Game> {
  const response = await fetch(`${API_URL}/games/${id}`, {
    method: 'PUT',
    headers: getHeaders(),
    body: JSON.stringify(game)
  })

  if (!response.ok) {
    throw new Error('Failed to update game')
  }

  return response.json()
}

export async function deleteGame(id: number): Promise<void> {
  const response = await fetch(`${API_URL}/games/${id}`, {
    method: 'DELETE',
    headers: getHeaders()
  })

  if (!response.ok) {
    throw new Error('Failed to delete game')
  }
}