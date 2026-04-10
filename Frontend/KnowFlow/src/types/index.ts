export interface User {
  id: number
  username: string
  email: string | null
}

export interface Library {
  id: number
  name: string
  description?: string
  contents: number
  created_at: string
}

export interface Flowcard {
  slug: string
  term: string
  definition: string
  library?: number
}

export interface Note {
  slug: string
  title: string
  content: string
  library?: number
}

export interface Knowtionary {
  id: number
  title: string
  questions: Array<{
    question: string
    answer: string
    type: 'text' | 'multiple'
  }>
}

export interface Task {
  id: number
  title: string
  description?: string
  completed: boolean
}
