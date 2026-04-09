import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export interface StatusResponse {
  status: string
  version?: string
}

export async function getStatus(): Promise<StatusResponse> {
  const response = await axios.get(`${API_URL}/health`)
  return response.data
}