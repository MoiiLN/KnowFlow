import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Lazy load pages
const Dashboard = () => import('@/pages/Dashboard.vue')
const Login = () => import('@/pages/Login.vue')
const Signup = () => import('@/pages/Signup.vue')
const Libraries = () => import('@/pages/Libraries.vue')
const LibraryDetail = () => import('@/pages/LibraryDetail.vue')
const Flowcards = () => import('@/pages/Flowcards.vue')
const FlowcardStudy = () => import('@/pages/FlowcardStudy.vue')
const Notes = () => import('@/pages/Notes.vue')
const NoteDetail = () => import('@/pages/NoteDetail.vue')
const Knowtionaries = () => import('@/pages/Knowtionaries.vue')
const KnowtionaryQuiz = () => import('@/pages/KnowtionaryQuiz.vue')
const Tasks = () => import('@/pages/Tasks.vue')
const TimerFlow = () => import('@/pages/TimerFlow.vue')
const PlannerMonth = () => import('@/pages/PlannerMonth.vue')
const Profile = () => import('@/pages/Profile.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { requiresGuest: true }
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup,
      meta: { requiresGuest: true }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard,
      meta: { requiresAuth: true }
    },
    {
      path: '/libraries',
      name: 'libraries',
      component: Libraries,
      meta: { requiresAuth: true }
    },
    {
      path: '/libraries/:id',
      name: 'library-detail',
      component: LibraryDetail,
      meta: { requiresAuth: true }
    },
    {
      path: '/flowcards',
      name: 'flowcards',
      component: Flowcards,
      meta: { requiresAuth: true }
    },
    {
      path: '/flowcards/study/:slug',
      name: 'flowcard-study',
      component: FlowcardStudy,
      meta: { requiresAuth: true }
    },
    {
      path: '/notes',
      name: 'notes',
      component: Notes,
      meta: { requiresAuth: true }
    },
    {
      path: '/notes/:slug',
      name: 'note-detail',
      component: NoteDetail,
      meta: { requiresAuth: true }
    },
    {
      path: '/knowtionaries',
      name: 'knowtionaries',
      component: Knowtionaries,
      meta: { requiresAuth: true }
    },
    {
      path: '/knowtionaries/quiz/:id',
      name: 'knowtionary-quiz',
      component: KnowtionaryQuiz,
      meta: { requiresAuth: true }
    },
    {
      path: '/tasks',
      name: 'tasks',
      component: Tasks,
      meta: { requiresAuth: true }
    },
    {
      path: '/planner',
      name: 'planner',
      component: PlannerMonth,
      meta: { requiresAuth: true }
    },
    {
      path: '/timerflow',
      name: 'timerflow',
      component: TimerFlow,
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
      meta: { requiresAuth: true }
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/dashboard'
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Esperar a que checkAuth() termine antes de decidir
  if (!authStore.initialized) {
    await authStore.checkAuth()
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router