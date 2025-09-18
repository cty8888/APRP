import type { RouteRecordRaw } from 'vue-router'
import { 
  Home, 
  Dashboard, 
  Login, 
  Register, 
  NotFound,
  ClassManagement,
  AssignmentManagement,
  SubmissionManagement
} from '../views'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  
  // 教师路由
  {
    path: '/classes',
    name: 'ClassManagement',
    component: ClassManagement,
    meta: { requiresAuth: true, roles: ['teacher'] }
  },
  {
    path: '/classes/:classId/assignments',
    name: 'ClassAssignments',
    component: AssignmentManagement,
    meta: { requiresAuth: true, roles: ['teacher'] }
  },
  {
    path: '/classes/:classId/assignments/:assignmentId/submissions',
    name: 'AssignmentSubmissions',
    component: SubmissionManagement,
    meta: { requiresAuth: true, roles: ['teacher'] }
  },
  
  // 学生路由
  {
    path: '/my-classes',
    name: 'StudentClasses',
    component: ClassManagement,
    meta: { requiresAuth: true, roles: ['student'] }
  },
  {
    path: '/my-classes/:classId',
    name: 'StudentClassDetail',
    component: AssignmentManagement,
    meta: { requiresAuth: true, roles: ['student'] }
  },
  {
    path: '/my-classes/:classId/assignments/:assignmentId',
    name: 'StudentAssignmentDetail',
    component: SubmissionManagement,
    meta: { requiresAuth: true, roles: ['student'] }
  },
  
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound
  }
]

export default routes