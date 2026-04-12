import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import DefaultLayout from '../layouts/DefaultLayout.vue'
import Dashboard from '../pages/Dashboard.vue'
import Libraries from '../pages/Libraries.vue'
import Flowcards from '../pages/Flowcards.vue'
import LibraryDetail from '../pages/LibraryDetail.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/login',
      component: Login
    },
    {
      path: '/',
      component: DefaultLayout,
      children: [
        {
          path: 'dashboard',
          component: Dashboard
        },
        {
          path: 'libraries',
          component: Libraries
        },
        {
          path: 'flowcards',
          component: Flowcards
        },
        {
          path: 'libraries/:id',
          component: LibraryDetail
        }
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ]
})

export default router

