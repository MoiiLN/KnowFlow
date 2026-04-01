import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'

// Knowtionaries
import KnowList from '../views/knowtionaries/List.vue'
import KnowCreate from '../views/knowtionaries/Create.vue'
import KnowEdit from '../views/knowtionaries/Edit.vue'

// Flowcards
import FlowList from '../views/flowcards/List.vue'
import FlowCreate from '../views/flowcards/Create.vue'
import FlowEdit from '../views/flowcards/Edit.vue'

const routes = [
  { path: '/', component: Home },

  // Knowtionaries
  { path: '/knowtionaries', component: KnowList },
  { path: '/knowtionaries/create', component: KnowCreate },
  { path: '/knowtionaries/edit/:id', component: KnowEdit },

  // Flowcards
  { path: '/flowcards', component: FlowList },
  { path: '/flowcards/create', component: FlowCreate },
  { path: '/flowcards/edit/:id', component: FlowEdit },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})