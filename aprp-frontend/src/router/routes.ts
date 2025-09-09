import TestConnection from '../views/TestConnection.vue'

const routes = [
    {
      path: '/',
      name: 'Home',
      component: TestConnection
    },
    {
      path: '/test',
      name: 'TestConnection',
      component: TestConnection
    }
  ]

  export default routes