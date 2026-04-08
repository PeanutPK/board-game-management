/**
 * Games API client
 */

import axios from 'axios'
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
    ...(token && { Authorization: `Bearer ${token}` }),
  }
}

export async function getGames(skip: number = 0, limit: number = 10): Promise<Game[]> {
  const response = await axios
    .get(`${API_URL}/games/?skip=${skip}&limit=${limit}`, {
      headers: getHeaders(),
    })
    .catch(function (error) {
      throw new Error('Failed to fetch games')
    })

  return response.data
}

export async function getGame(id: number): Promise<Game> {
  const response = await axios
    .get(`${API_URL}/games/${id}`, {
      headers: getHeaders(),
    })
    .catch(function (error) {
      throw new Error('Failed to fetch game')
    })

  return response.data
}

export async function createGame(game: GameCreate): Promise<Game> {
  const response = await axios
    .post(`${API_URL}/games/`, game, {
      headers: getHeaders(),
    })
    .catch(function (error) {
      throw new Error('Failed to create game')
    })

  return response.data
}

export async function updateGame(id: number, game: Partial<GameCreate>): Promise<Game> {
  const response = await axios
    .put(`${API_URL}/games/${id}`, game, {
      headers: getHeaders(),
    })
    .catch(function (error) {
      throw new Error('Failed to update game')
    })

  return response.data
}

export async function deleteGame(id: number): Promise<void> {
  const response = await axios
    .delete(`${API_URL}/games/${id}`, {
      headers: getHeaders(),
    })
    .catch(function (error) {
      throw new Error('Failed to delete game')
    })
}
