import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import GamesView from '../views/GamesView.vue'
import StoresView from '../views/StoresView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/games', name: 'games', component: GamesView },
  { path: '/stores', name: 'stores', component: StoresView },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
