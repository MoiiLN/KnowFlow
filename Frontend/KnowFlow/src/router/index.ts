import { createRouter, createWebHistory } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import Login from '@/pages/Login.vue'
import Dashboard from '@/pages/Dashboard.vue'
import Libraries from '@/pages/Libraries.vue'
import Flowcards from '@/pages/Flowcards.vue'
import LibraryDetail from '@/pages/LibraryDetail.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/login',
      name: 'login',
      component: Login
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
      path: '/flowcards',
      name: 'flowcards',
      component: Flowcards,
      meta: { requiresAuth: true }
    },
    {
      path: '/libraries/:id',
      name: 'library-detail',
      component: LibraryDetail,
      meta: { requiresAuth: true }
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/dashboard'
    }
  ]
})

export default router

