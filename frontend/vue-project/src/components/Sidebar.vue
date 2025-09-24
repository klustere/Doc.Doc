<template>
  <aside class="sidebar">
  <h2>doc.doc</h2>
    <nav class="nav-bar">
      <router-link class="nav-item" :to="{ name: 'home' }">
        <span class="label">Home</span>
      </router-link>
      <router-link class="nav-item" :to="{ name: 'pages.list' }">
        <span class="label">Pages</span>
      </router-link>
      <router-link class="nav-item" :to="{ name: 'pages.create' }">
        <span class="label">Add Page</span>
      </router-link>
    </nav>
    <div class="search">
      <input 
        v-model="q" 
        placeholder="Search pages..." 
        @keyup.enter="onTextSearch" />
      <div class="search-actions">
        <button class="btn" @click="onTextSearch">Text Search</button>
        <button 
          class="btn primary" 
          :disabled="!q.trim() || searching"
          @click="performSemanticSearch">
          Semantic Search
        </button>
        <button v-if="semResults.length" class="btn clear" @click="clearSemanticSearch">Clear</button>
      </div>
      <div v-if="searching" class="searching-note">Searching…</div>
      <div v-if="semError" class="error-note">{{ semError }}</div>
    </div>

    <!-- Semantic Results -->
    <div v-if="semResults.length" class="quick-list card" style="margin-top:12px">
      <h4>Semantic Results</h4>
      <ul class="recent-list">
        <li v-for="r in semResults" :key="r.id">
          <router-link :to="{ name: 'pages.view', params: { id: r.id } }" class="recent-bar">
            <span class="title">{{ r.title || 'Untitled' }}</span>
          </router-link>
        </li>
      </ul>
    </div>
    <div class="quick-list card" style="margin-top:12px">
      <h4>Recent Pages</h4>
      <ul class="recent-list">
          <li v-for="p in filtered" :key="p.id">
          <router-link :to="{ name: 'pages.view', params: { id: p.id } }" class="recent-bar">
            <span class="title">{{ p.title || 'Untitled' }}</span>
            <span class="meta">{{ p.updated_at ? new Date(p.updated_at).toLocaleDateString() : '' }}</span>
          </router-link>
        </li>
        <li v-if="filtered.length === 0" style="color:var(--muted)">No pages yet</li>
      </ul>
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { usePageStore } from '../stores/pageStore'
// Gemini moved to editor
// import GeminiPanel from './GeminiPanel.vue'

const store = usePageStore()
const q = ref('')
const pages = ref([])
const searching = ref(false)
const semResults = ref([])
const semError = ref('')

onMounted(async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/pages/')
    if (res.ok) pages.value = await res.json()
    else pages.value = []
  } catch (err) {
    console.error('Failed to load pages in Sidebar:', err)
    pages.value = []
  }
})

const filtered = computed(() => {
  if (!q.value) return pages.value
  return pages.value.filter(p => p.title.toLowerCase().includes(q.value.toLowerCase()))
})

function onTextSearch() {
  // No-op: filtered list updates reactively; this exists to match the explicit button UX
}

async function performSemanticSearch() {
  if (!q.value.trim()) return
  searching.value = true
  semError.value = ''
  try {
    const res = await fetch('http://127.0.0.1:8000/api/vector-search/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: q.value, top_k: 3 })
    })
    if (!res.ok) {
      const txt = await res.text().catch(() => '')
      throw new Error(`Search failed (${res.status}): ${txt}`)
    }
    const data = await res.json()
    semResults.value = Array.isArray(data.results) ? data.results : []
  } catch (e) {
    console.error('Semantic search error:', e)
    semError.value = e.message || 'Semantic search failed'
    semResults.value = []
  } finally {
    searching.value = false
  }
}

function clearSemanticSearch() {
  semResults.value = []
  semError.value = ''
  searching.value = false
}
</script>

<style scoped>
.sidebar {
  width: 100%;
  padding: 8px 12px;
  min-height: calc(100vh - 0px);
}
nav ul { list-style: none; padding: 0 }
nav li { margin-bottom: 12px }
.gemini { margin-top: 16px }

.search-actions {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}
.btn {
  background: rgba(96, 165, 250, 0.1);
  border: 1px solid rgba(96, 165, 250, 0.3);
  color: #e2e8f0;
  padding: 6px 10px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
}
.btn.primary {
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  border: none;
}
.btn.clear {
  border-color: rgba(239, 68, 68, 0.4);
  color: #fecaca;
}
.searching-note { font-size: 12px; color: #93c5fd; margin-top: 6px; }
.error-note { font-size: 12px; color: #fecaca; margin-top: 6px; }
</style>
