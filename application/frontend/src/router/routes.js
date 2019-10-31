
const routes = [
  {
    path: '/',
    component: () => import('layouts/MyLayout.vue'),
    children: [
      {
        path: '',
        name: 'rootHome',
        component: () => import('pages/Index.vue')
      },
      { path: 'hot', component: () => import('pages/Index.vue') },
      { path: 'new', component: () => import('pages/Index.vue') },
      { path: '?title:query', component: () => import('pages/Index.vue') }
    ]
  },
  {
    path: '/register',
    component: () => import('layouts/MyLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Register.vue') }
    ]
  },
  {
    path: '/tutorial',
    component: () => import('layouts/MyLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Tutorial.vue') }
    ]
  },
  {
    path: '/forgot',
    component: () => import('layouts/MyLayout.vue'),
    children: [
      { path: '', component: () => import('pages/ForgetPassword.vue') }
    ]
  },
  {
    path: '/about',
    component: () => import('layouts/MyLayout.vue'),
    children: [
      {
        path: '',
        name: 'rootAbout',
        component: () => import('pages/About.vue')
      },
      { path: ':name', component: () => import('pages/Intro.vue') }
    ]
  },
  {
    path: '/post',
    component: () => import('layouts/MyLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Post.vue') }
    ]
  }
]

// Always leave this as last one
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '*',
    component: () => import('pages/Error404.vue')
  })
}

export default routes
