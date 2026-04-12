const api = {
  post: async (endpoint, data) => {
    console.log(`API POST ${endpoint}`, data)
    return { data: 'mock-success' }
  },
  get: async (endpoint) => {
    console.log(`API GET ${endpoint}`)
    return { data: [] }
  }
}

export default api

