import { createRouter, createWebHistory } from 'vue-router'
import PresenterPage from "@/views/PresenterPage.vue";
import Home from "@/views/Home.vue";
import Presentation from "@/views/Presentation.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/quiz',
      name: 'quiz',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/QuizPage.vue'),
    },

    {
      path: '/presenter',
      name: 'presenter',
      component: () => import('../views/PresenterPage.vue'),
    },

      {
    path: '/presenter',
    component: PresenterPage,
    children: [
      { path: '', redirect: '/presenter/home' },  // 默认跳转
      { path: 'home', component: Home },
      { path: 'presentation', component: Presentation },
    ],
  },
  ],
})

export default router
