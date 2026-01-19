import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Notes API
export const notesAPI = {
  getAll: () => api.get('/notes/'),
  getById: (id) => api.get(`/notes/${id}`),
  create: (data) => api.post('/notes/', data),
  update: (id, data) => api.put(`/notes/${id}`, data),
  delete: (id) => api.delete(`/notes/${id}`),
}

// Action Items API
export const actionItemsAPI = {
  getAll: () => api.get('/action-items/'),
  getById: (id) => api.get(`/action-items/${id}`),
  create: (data) => api.post('/action-items/', data),
  update: (id, data) => api.put(`/action-items/${id}`, data),
  delete: (id) => api.delete(`/action-items/${id}`),
}

// Tags API
export const tagsAPI = {
  getAll: () => api.get('/tags/'),
  getById: (id) => api.get(`/tags/${id}`),
  create: (data) => api.post('/tags/', data),
  update: (id, data) => api.put(`/tags/${id}`, data),
  delete: (id) => api.delete(`/tags/${id}`),
}

// Moods API
export const moodsAPI = {
  getAll: () => api.get('/moods/'),
  getWeekly: () => api.get('/moods/weekly'),
  getWeeklyStats: () => api.get('/moods/stats/weekly'),
  getById: (id) => api.get(`/moods/${id}`),
  create: (data) => api.post('/moods/', data),
  update: (id, data) => api.put(`/moods/${id}`, data),
  delete: (id) => api.delete(`/moods/${id}`),
}

export default api
