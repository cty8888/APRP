<template>
  <div id="app">
    <nav>
      <h1>APRP - 论文评审平台</h1>
      <div class="nav-links">
        <router-link to="/">首页</router-link>
        <router-link to="/test">连接测试</router-link>
      </div>
    </nav>
    <main>
      <router-view />
    </main>
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  font-family: Avenir, Helvetica, Arial, sans-serif;
}

nav {
  background-color: #2c3e50;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

nav h1 {
  margin: 0;
  font-size: 1.5rem;
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.nav-links a {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  background-color: #34495e;
}

main {
  padding: 2rem;
}
</style>
