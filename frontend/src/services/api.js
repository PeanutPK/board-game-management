import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
})

export const gamesApi = {
  list: () => api.get('/games/'),
  get: (id) => api.get(`/games/${id}`),
  create: (data) => api.post('/games/', data),
  update: (id, data) => api.put(`/games/${id}`, data),
  remove: (id) => api.delete(`/games/${id}`),
}

export const storesApi = {
  list: () => api.get('/stores/'),
  get: (id) => api.get(`/stores/${id}`),
  create: (data) => api.post('/stores/', data),
  update: (id, data) => api.put(`/stores/${id}`, data),
  remove: (id) => api.delete(`/stores/${id}`),
}

export default api
