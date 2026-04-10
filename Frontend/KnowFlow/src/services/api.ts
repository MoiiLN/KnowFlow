import axios from 'axios'

const api = axios.create({
  baseURL: '/api', // Proxied to localhost:8000/api
  withCredentials: true
})

// Request interceptor for auth headers if needed
api.interceptors.request.use((config) => {
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401 - redirect to login
    if (error.response?.status === 401) {
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api

// API Services
export const libraryService = {
  getAll: () => api.get('/libraries/'),
  create: (data: any) => api.post('/libraries/create/', data),
  getById: (id: string) => api.get(`/libraries/${id}/`),
  update: (id: string, data: any) => api.post(`/libraries/edit/${id}/`, data),
  delete: (id: string) => api.post(`/libraries/delete/${id}/`)
}

export const flowcardService = {
  getAll: () => api.get('/flowcards/'),
  create: (data: any) => api.post('/flowcards/add/', data),
  getBySlug: (slug: string) => api.get(`/flowcards/${slug}/`),
  update: (slug: string, data: any) => api.post(`/flowcards/edit/${slug}/`, data)
}

export const noteService = {
  getAll: () => api.get('/notes/'),
  create: (data: any) => api.post('/notes/add/', data),
  getBySlug: (slug: string) => api.get(`/notes/${slug}/`),
  update: (slug: string, data: any) => api.post(`/notes/edit/${slug}/`, data)
}

export const knowtionaryService = {
  getAll: () => api.get('/knowtionaries/'),
  create: (data: any) => api.post('/knowtionaries/add/', data),
  getById: (id: string) => api.get(`/knowtionaries/${id}/`),
  update: (id: string, data: any) => api.post(`/knowtionaries/edit/${id}/`, data)
}

export const taskService = {
  getAll: () => api.get('/tasks/'),
  create: (data: any) => api.post('/tasks/create/', data),
  update: (id: string, data: any) => api.post(`/tasks/edit/${id}/`, data),
  delete: (id: string) => api.post(`/tasks/delete/${id}/`)
}
