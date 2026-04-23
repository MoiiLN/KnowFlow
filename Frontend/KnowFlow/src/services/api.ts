import axios from 'axios'

// Axios instance
const api = axios.create({
  baseURL: '/api', // Proxied to localhost:8000/api
  withCredentials: true // Django session cookies
})

// Response interceptor for 401 redirect
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api

// Library Service
export const libraryService = {
  getAll: () => api.get('/libraries/'),
  create: (data: FormData | object) => api.post('/libraries/create/', data),
  getById: (id: string | number) => api.get(`/libraries/${id}/`),
  update: (id: string | number, data: FormData | object) => api.post(`/libraries/${id}/edit/`, data),
  delete: (id: string | number) => api.post(`/libraries/${id}/delete/`, {})
}


// Flowcard Service
export const flowcardService = {
  getAll: () => api.get('/flowcards/'),
  create: (data: FormData | object) => api.post('/flowcards/add/', data),
  getBySlug: (slug: string) => api.get(`/flowcards/${slug}/`),
  update: (slug: string, data: FormData | object) => api.post(`/flowcards/edit/${slug}/`, data)
}

// Note Service
export const noteService = {
  getAll: () => api.get('/notes/'),
  create: (data: FormData | object) => api.post('/notes/add/', data),
  getBySlug: (slug: string) => api.get(`/notes/${slug}/`),
  update: (slug: string, data: FormData | object) => api.post('/notes/edit/${slug}/', data)
}

// Knowtionary Service
export const knowtionaryService = {
  getAll: () => api.get('/knowtionaries/'),
  create: (data: FormData | object) => api.post('/knowtionaries/add/', data),
  getById: (id: string | number) => api.get(`/knowtionaries/${id}/`),
  update: (id: string | number, data: FormData | object) => api.post(`/knowtionaries/edit/${id}/`, data)
}

// Task Service
export const taskService = {
  getAll: () => api.get('/tasks/'),
  create: (data: FormData | object) => api.post('/tasks/create/', data),
  update: (id: string | number, data: FormData | object) => api.post(`/tasks/edit/${id}/`, data),
  delete: (id: string | number) => api.post(`/tasks/delete/${id}/`)
}

// Auth helpers
export const authService = {
  login: (credentials: {username: string, password: string}) => api.post('/accounts/login/', credentials),
  logout: () => api.post('/accounts/logout/')
}

