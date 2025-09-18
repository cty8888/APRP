<template>
  <div class="dashboard">
    <div class="container">
      <div class="dashboard-header">
        <h1>仪表板</h1>
        <p class="dashboard-subtitle">欢迎回来，{{ user?.name }}！</p>
      </div>
      
      <div class="dashboard-content">
        <!-- 教师仪表板 -->
        <template v-if="user?.role === 'teacher'">
          <div class="dashboard-grid">
            <div class="dashboard-card primary-card">
              <h2>班级管理</h2>
              <p>管理您的班级，创建和组织学习班级</p>
              <router-link to="/classes" class="btn btn-primary">管理班级</router-link>
            </div>
            
            <div class="stats-grid">
              <div class="stat-card">
                <h3>我的班级</h3>
                <p class="stat-number">0</p>
              </div>
              <div class="stat-card">
                <h3>总任务数</h3>
                <p class="stat-number">0</p>
              </div>
              <div class="stat-card">
                <h3>待评分</h3>
                <p class="stat-number">0</p>
              </div>
            </div>
          </div>
        </template>
        
        <!-- 学生仪表板 -->
        <template v-else>
          <div class="dashboard-grid">
            <div class="dashboard-card primary-card">
              <h2>我的班级</h2>
              <p>查看您加入的班级和相关任务</p>
              <router-link to="/my-classes" class="btn btn-primary">查看班级</router-link>
            </div>
            
            <div class="stats-grid">
              <div class="stat-card">
                <h3>加入的班级</h3>
                <p class="stat-number">0</p>
              </div>
              <div class="stat-card">
                <h3>待完成任务</h3>
                <p class="stat-number">0</p>
              </div>
              <div class="stat-card">
                <h3>已提交任务</h3>
                <p class="stat-number">0</p>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuth } from '../store/auth'

const { user } = useAuth()
</script>