import axios from 'axios'

const api = axios.create({
  baseURL: '/api/',
  withCredentials: true
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const url = error.config?.url || ''

    const isAuthEndpoint =
      url.includes('login') ||
      url.includes('signup') ||
      url.includes('me')

    if (error.response?.status === 401 && !isAuthEndpoint) {
      window.location.href = '/login'
    }

    if (error.response?.status === 403) {
      window.dispatchEvent(
        new CustomEvent('subscription-limit', {
          detail: error.response.data.error
        })
      )
    }

    return Promise.reject(error)
  }
)

export default api

export const profileService = {
  update: (data: FormData) =>
    api.post('me/edit/', data, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }),

  deleteAccount: () =>
    api.post('me/delete/', {})
}

export const libraryService = {
  getAll: () =>
    api.get('libraries/'),

  create: (data: FormData | object) =>
    api.post('libraries/create/', data),

  getById: (id: string | number) =>
    api.get(`libraries/${id}/`),

  update: (id: string | number, data: FormData | object) =>
    api.post(`libraries/${id}/edit/`, data),

  delete: (id: string | number) =>
    api.post(`libraries/${id}/delete/`, {})
}

export const flowcardService = {
  getAll: () =>
    api.get('flowcards/'),

  create: (data: FormData | object) =>
    api.post('flowcards/add/', data),

  getBySlug: (slug: string) =>
    api.get(`flowcards/${slug}/`),

  update: (slug: string, data: FormData | object) =>
    api.post(`flowcards/edit/${slug}/`, data)
}

export const noteService = {
  getAll: () =>
    api.get('notes/'),

  create: (data: FormData | object) =>
    api.post('notes/add/', data),

  getBySlug: (slug: string) =>
    api.get(`notes/${slug}/`),

  update: (slug: string, data: FormData | object) =>
    api.post(`notes/edit/${slug}/`, data)
}

export const knowtionaryService = {
  getAll: () =>
    api.get('knowtionaries/'),

  create: (data: FormData | object) =>
    api.post('knowtionaries/add/', data),

  getById: (id: string | number) =>
    api.get(`knowtionaries/${id}/`),

  update: (id: string | number, data: FormData | object) =>
    api.post(`knowtionaries/edit/${id}/`, data)
}

export const timerflowService = {
  getSettings: () =>
    api.get('timerflow/settings/'),

  updateSettings: (data: object) =>
    api.post('timerflow/settings/update/', data),

  getSessions: () =>
    api.get('timerflow/sessions/'),

  getTodayStats: () =>
    api.get('timerflow/sessions/today-stats/'),

  createSession: (data: object) =>
    api.post('timerflow/sessions/create/', data)
}

export const authService = {
  login: (credentials: { username: string; password: string }) =>
    api.post('login/', credentials),

  logout: () =>
    api.post('logout/')
}

export const taskService = {
  getAll: () =>
    api.get('tasks/'),

  create: (data: FormData | object) =>
    api.post('tasks/create/', data),

  update: (id: string | number, data: FormData | object) =>
    api.post(`tasks/edit/${id}/`, data),

  delete: (id: string | number) =>
    api.post(`tasks/${id}/delete/`),

  getMonthly: (month: number, year: number) =>
    api.get(`tasks/planner/?month=${month}&year=${year}`)
}

export const subscriptionService = {
  getUsage: () =>
    api.get('users/subscription/usage/'),

  upgrade: () =>
    api.post('users/upgrade/')
}