import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import TravelView from '@/views/TravelView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/travel',
      name: 'travel',
      component: TravelView
    }
  ]
})

export default router