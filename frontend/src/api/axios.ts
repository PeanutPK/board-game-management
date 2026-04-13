import axios from 'axios'

const api = axios.create({
  baseURL: '/api', // adjust to your backend URL
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Remove token
      localStorage.removeItem('token')
      localStorage.removeItem('user_role')
      localStorage.removeItem('username')

      // Redirect to login
      window.location.href = '/auth'
    }
    return Promise.reject(error)
  },
)

export default api
