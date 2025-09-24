
<template>
  <div class="app-shell">
    <div class="main">
      <HeaderBar v-if="!isHome" />
      <main class="content">
        <transition name="fade" mode="out-in">
          <router-view />
        </transition>
      </main>
    </div>
  </div>
</template>

<script setup>
import HeaderBar from './components/HeaderBar.vue'
import { useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()
const isHome = computed(() => {
  return route.name === 'home'
})
</script>

<style>
.app-shell {
  min-height: 100vh;
}
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
}
.content {
  flex: 1;
}
.logo {
  font-weight: 700;
}
</style>
