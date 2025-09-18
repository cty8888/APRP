// 组件统一导出
// 布局组件
export { default as Navbar } from './layout/Navbar.vue'
export { default as PageLayout } from './layout/PageLayout.vue'

// 表单组件
export { default as LoginForm } from './forms/LoginForm.vue'
export { default as RegisterForm } from './forms/RegisterForm.vue'

// 通用组件
export { default as Alert } from './common/Alert.vue'
export { default as LoadingSpinner } from './common/LoadingSpinner.vue'
export { default as BaseButton } from './common/BaseButton.vue'
export { default as BaseInput } from './common/BaseInput.vue'

// 班级管理组件
export { default as CreateClassForm } from './class/CreateClassForm.vue'
export { default as JoinClassForm } from './class/JoinClassForm.vue'
export { default as ClassList } from './class/ClassList.vue'

// 任务管理组件
export { default as CreateAssignmentForm } from './assignment/CreateAssignmentForm.vue'
export { default as AssignmentList } from './assignment/AssignmentList.vue'

// 提交管理组件
export { default as SubmitAssignmentForm } from './submission/SubmitAssignmentForm.vue'
export { default as SubmissionList } from './submission/SubmissionList.vue'
export { default as GradeSubmissionForm } from './submission/GradeSubmissionForm.vue'
