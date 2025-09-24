<template>
  <header class="dashboard-header">
    <div class="header-left">
      <div class="logo">doc.doc</div>
      <nav class="main-nav">
        <router-link :to="{ name: 'dashboard' }" class="nav-item" :class="{ active: active === 'dashboard' }">Dashboard</router-link>
        <router-link :to="{ name: 'pages.list' }" class="nav-item" :class="{ active: active === 'pages.list' }">Documents</router-link>
        <router-link :to="{ name: 'graph' }" class="nav-item" :class="{ active: active === 'graph' }">Graph</router-link>
        <router-link :to="{ name: 'version-history' }" class="nav-item" :class="{ active: active === 'version-history' }">Version History</router-link>
        <a href="#" class="nav-item">Analytics</a>
        <a href="#" class="nav-item">Settings</a>
      </nav>
    </div>
    <div class="header-right">
      <div class="search-box">
        <input v-model="q" @keyup.enter="onSearch" placeholder="Search pages..." class="search-input" />
      </div>
      <button class="create-btn" @click="goCreate">
        ✏️ New Page
      </button>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const q = ref('')

const active = computed(() => {
  const n = route.name || ''
  // Treat any pages.* route as the Documents section so the nav stays highlighted
  if (typeof n === 'string' && n.startsWith('pages.')) return 'pages.list'
  return n
})

function goCreate() {
  router.push({ name: 'pages.create' })
}

function onSearch() {
  if (!q.value) return router.push({ name: 'pages.list' })
  router.push({ name: 'pages.list', query: { q: q.value } })
}
</script>

<style scoped>
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 32px;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(96, 165, 250, 0.2);
  position: sticky;
  top: 0;
  z-index: 100;
}
.header-left { display:flex; align-items:center; gap:40px }
.logo { font-size:24px; font-weight:900; color:#60a5fa; text-shadow:0 0 20px #60a5fa }
.main-nav { display:flex; gap:24px }
.nav-item { color: rgba(255,255,255,0.7); text-decoration:none; padding:8px 16px; border-radius:8px }
.nav-item.active, .nav-item:hover { color:white; background: rgba(96,165,250,0.2) }
.header-right { display:flex; align-items:center; gap:16px }
.search-input { padding:8px 16px; border-radius:8px; border:1px solid rgba(96,165,250,0.3); background: rgba(255,255,255,0.03); color:white }
.create-btn { background: linear-gradient(135deg,#60a5fa,#7dd3fc); border:none; color:white; padding:8px 16px; border-radius:8px; cursor:pointer }
</style>
