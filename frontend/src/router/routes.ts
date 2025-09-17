const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue') 
  },
  {
    path: '/upload',
    name: 'Upload',
    component: () => import('../views/Upload.vue')  
  },
  {
    path: '/result',
    name: 'Result',
    component: () => import('../views/Result.vue')  
  }
]

export default routes
