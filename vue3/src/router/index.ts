import {createRouter, createWebHistory} from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'root',
      component: () => import('../views/PresentationsPage.vue'),
      meta: {requiresAuth: true},
      children: [
        {
          path: 'home',  // 实际路径为 /home
          name: 'home',
          component: () => import('../views/Home.vue'),
          meta: {requiresAuth: true},
        },
        {
          path: 'presentations',  // 实际路径为 /presentations
          name: 'presentations',
          component: () => import('../views/PresentationsView.vue'),
          meta: {requiresAuth: true},
        }
      ]
    },

    {
      path: '/quiz',
      name: 'quiz',
      meta: {requiresAuth: true},
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/QuizPage.vue'),
    },


{
  path: '/presentation/:uuid',
  name: 'presentationDetail',
  component: () => import('../views/PresenterPage.vue'),
  props: true,
  children: [
    {
      path: 'edit',
      name: 'EditView',
      component: () => import('../views/EditView.vue')
    },
    {
      path: 'result',
      name: 'ResultView',
      component: () => import('../views/ResultView.vue')
    }
  ],
    redirect: to => {
    return {
      name: 'PresentationEdit',
      params: { uuid: to.params.uuid }
    }
  },
},

    {
      path: '/login',
      name: 'login',
      meta: {hideNavbar: true},
      component: () => import('../views/LoginPage.vue'),
    },

    {
      path: '/register',
      name: 'Register',
      meta: {hideNavbar: true},
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
