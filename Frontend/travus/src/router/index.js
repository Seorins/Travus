import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import About from '@/views/About.vue'
import TravelView from '@/views/TravelView.vue'
import TravelDetailView from '@/views/TravelDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/about',
      name: 'about',
      component: About
    },
    {
      path: '/travel',
      name: 'travel',
      component: TravelView
    },
    {
      path: '/travel/:id',
      name: 'travel-detail',
      component: TravelDetailView
    }
  ]
})

export default router