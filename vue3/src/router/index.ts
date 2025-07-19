import {createRouter, createWebHistory} from 'vue-router'
import PresenterPage from "@/views/PresenterPage.vue";
import Home from "@/views/Home.vue";
import PresentationsView from "@/views/PresentationsView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/quiz',
      name: 'quiz',
      meta: { requiresAuth: true },
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/QuizPage.vue'),
    },

    {
      path: '/presenter',
      name: 'presenter',
      meta: { requiresAuth: true },
      component: () => import('../views/PresenterPage.vue'),
    },

    {
      path: '/presenter',
      name: 'presenter',
      meta: { requiresAuth: true },
      component: PresenterPage,
      children: [
        {path: '', redirect: '/presenter/home'},  // 默认跳转
        {path: 'home', component: Home},
        {path: 'presentations', component: PresentationsView},
      ],
    },
    {
      path: '/presentation/:uuid',
      name: 'EditView',
      meta: { requiresAuth: true,},
      component: () => import('../views/EditView.vue'),
      props: true,
    },
    {
      path: '/login',
      name: 'login',
      meta: { hideNavbar: true },
      component: () => import('../views/LoginPage.vue'),
    },

    {
      path: '/register',
      name: 'Register',
      meta: { hideNavbar: true },
      component: () => import('../views/RegisterPage.vue') // 替换为你的注册组件路径
    }
  ],
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('access_token')
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})


export default router
