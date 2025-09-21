<template>
  <div id="app">
    <Navbar />
    <main class="page">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { Navbar } from './components'
import { useAuth } from './store/auth'
import './styles'

const authStore = useAuth()
authStore.initAuth()
</script>