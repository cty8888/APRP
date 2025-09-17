<template>
  <div id="app">
    <main>
      <router-view />
    </main>
  </div>
</template>

<style scoped>
#app {
  font-family: Arial, sans-serif;
}

nav {
  background: #f8f9fa;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ddd;
}

nav a {
  color: #333;
  text-decoration: none;
  padding: 0.5rem 1rem;
  margin: 0 0.25rem;
  border-radius: 4px;
}

nav a:hover {
  background: #e9ecef;
}

nav a.router-link-active {
  background: #007bff;
  color: white;
}

main {
  padding: 0;
}
</style>
