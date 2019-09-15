
const routes = [
  {
    path: '/',
    component: () => import('layouts/MyLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { path: '/about', component: () => import('pages/About.vue') },
      { path: '/phyo', component: () => import('pages/Phyo.vue') },
      { path: '/jason', component: () => import('pages/Jason.vue') },
      { path: '/antonio', component: () => import('pages/Antonio.vue') },
      { path: '/myles', component: () => import('pages/Myles.vue') },
      { path: '/eduardo', component: () => import('pages/Eduardo.vue') }
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
