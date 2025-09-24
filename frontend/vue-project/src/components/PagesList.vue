<template>
  <div class="pages-dashboard">
    <HeaderBar />

    <!-- Main Content -->
    <div class="dashboard-content">
      <main class="main-panel">
        <div class="panel-header">
          <h1>Documents & Pages</h1>
          <p>Create, edit, and organize your documents with intelligent chapters and linking.</p>
        </div>

        <!-- Intelligent Vector Search -->
        <div class="intelligent-search-section">
          <div class="search-container">
            <div class="search-background">
              <div class="search-particles"></div>
              <div class="search-waves"></div>
            </div>
            
            <div class="search-box-wrapper">
              <div class="search-icon-container">
                <div class="magnifying-glass" :class="{ searching: isSearching }">
                  <div class="glass-body"></div>
                  <div class="glass-handle"></div>
                  <div class="search-rays"></div>
                </div>
              </div>
              
              <input 
                v-model="vectorQuery" 
                @input="onSearchInput"
                @keyup.enter="performVectorSearch"
                class="intelligent-search-input" 
                placeholder="🔍 Intelligent Search"
                :disabled="isSearching"
              />
              
              <div class="search-actions">
                <button 
                  @click="performVectorSearch" 
                  :disabled="!vectorQuery.trim() || isSearching"
                  class="vector-search-btn"
                >
                  <span v-if="!isSearching">🔍 Search</span>
                  <span v-else class="searching-text">
                    <span class="loading-dots">●●●</span> Analyzing
                  </span>
                </button>
                <button 
                  v-if="vectorResults.length > 0" 
                  @click="clearVectorSearch"
                  class="clear-search-btn"
                >
                  ✕ Clear
                </button>
              </div>
            </div>
            
            <!-- Floating Vector Embeddings Animation -->
            <div v-if="isSearching" class="vector-embeddings-animation">
              <div v-for="i in 20" :key="i" class="floating-vector" :style="getVectorStyle(i)">
                <div class="vector-dot"></div>
                <div class="vector-connections"></div>
              </div>
              
              <div class="ai-brain-center">
                <div class="brain-core">
                  <div class="neural-pulse"></div>
                  <div class="processing-ring"></div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Vector Search Results -->
          <div v-if="vectorResults.length > 0" class="vector-results-section">
            <div class="results-header">
              <h3>🎯 Most Relevant Results</h3>
              <div class="search-stats">
                Found {{ vectorResults.length }} matches
              </div>
            </div>
            
            <div class="vector-results-grid">
              <div 
                v-for="(result, index) in vectorResults" 
                :key="result.id"
                class="vector-result-card"
                :style="{ animationDelay: `${index * 0.1}s` }"
                @click="router.push({ name: 'pages.view', params: { id: result.id } })"
              >
                <div class="result-header">
                  <div class="result-rank">#{{ index + 1 }}</div>
                </div>
                
                <h4 class="result-title">{{ result.title }}</h4>
                <p class="result-preview" v-html="highlightSearchTerms(result.content_preview)"></p>
                
                <div class="result-meta">
                  <span class="result-date">{{ formatDate(result.updated_at) }}</span>
                  <span class="result-links">{{ result.link_count }} links</span>
                </div>
                
                <div class="result-glow"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Stats -->
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">📄</div>
            <div class="stat-content">
              <div class="stat-number">{{ pages.length }}</div>
              <div class="stat-label">Total Documents</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">🔍</div>
            <div class="stat-content">
              <div class="stat-number">{{ visiblePages.length }}</div>
              <div class="stat-label">Search Results</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">📝</div>
            <div class="stat-content">
              <div class="stat-number">{{ recentPages.length }}</div>
              <div class="stat-label">Recent Updates</div>
            </div>
          </div>
        </div>

        <!-- Error Display -->
        <div v-if="error" class="error-card">
          <div class="error-icon">{{ error.icon }}</div>
          <div class="error-content">
            <h3>{{ error.title }}</h3>
            <p>{{ error.message }}</p>
            <div class="error-action">
              <code>{{ error.action }}</code>
            </div>
            <div class="error-buttons">
              <button class="retry-btn" @click="retryConnection" :disabled="loading">
                {{ loading ? 'Checking...' : 'Retry Connection' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading && !error" class="loading-card">
          <div class="loading-spinner"></div>
          <p>Loading documents...</p>
        </div>

        <!-- Pages Grid -->
        <div class="pages-section" v-if="!error">
          <h2>Your Documents</h2>
            <div v-if="pages.length === 0 && !loading" class="empty-state">
            <div class="empty-icon">📄</div>
            <h3>No documents yet</h3>
            <p>Create your first page to get started!</p>
            <button class="create-btn" @click="router.push({ name: 'pages.create' })">
              ✏️ Create First Page
            </button>
          </div>
          <div v-else class="pages-grid">
            <div v-for="page in visiblePages" :key="page.id" class="page-card clickable" @click="router.push({ name: 'pages.view', params: { id: page.id } })">
              <div class="page-header">
                <div class="page-icon">📄</div>
                <h3>{{ page.title || 'Untitled' }}</h3>
              </div>
              <div class="page-preview" v-html="renderPreview(page.content)"></div>
              <div class="page-meta">
                <span class="page-date">{{ formatDate(page.created_at) }}</span>
                <div class="page-actions" @click.stop>
                  <button class="action-btn" @click="router.push({ name: 'pages.edit', params: { id: page.id } })">Edit</button>
                  <button class="action-btn danger" @click="deletePage(page.id)">Delete</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Create Modal -->
    <div v-if="showCreate" class="modal-backdrop" @click.self="showCreate = false">
      <div class="modal">
        <div class="modal-header">
          <h3>Create New Page</h3>
          <button class="close-btn" @click="showCreate = false">×</button>
        </div>
        <div class="modal-body">
          <input v-model="newTitle" placeholder="Page title" class="title-input" />
          <textarea v-model="newContent" rows="8" placeholder="Start writing your content..." class="content-input"></textarea>
        </div>
        <div class="modal-footer">
          <button class="btn-primary" @click="createPage" :disabled="loading">
            {{ loading ? 'Creating...' : 'Create Page' }}
          </button>
          <button class="btn-secondary" @click="showCreate = false" :disabled="loading">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { marked } from 'marked'

const route = useRoute()
const router = useRouter()
const pages = ref([])
const q = ref('')
const showCreate = ref(false)
const newTitle = ref('')
const newContent = ref('')
const loading = ref(false)
const error = ref(null)
const retryCount = ref(0)

// Vector Search State
const vectorQuery = ref('')
const vectorResults = ref([])
const isSearching = ref(false)
const searchTimeout = ref(null)

function getVectorStyle(index) {
  const angle = (index * 360 / 20) * Math.PI / 180
  const radius = 120 + Math.random() * 80
  const x = Math.cos(angle) * radius
  const y = Math.sin(angle) * radius
  
  return {
    '--x': `${x}px`,
    '--y': `${y}px`,
    '--delay': `${index * 0.1}s`,
    '--duration': `${2 + Math.random() * 2}s`
  }
}

function highlightSearchTerms(text) {
  if (!vectorQuery.value || !text) return text
  const terms = vectorQuery.value.split(' ').filter(term => term.length > 2)
  let highlighted = text
  
  terms.forEach(term => {
    const regex = new RegExp(`(${term})`, 'gi')
    highlighted = highlighted.replace(regex, '<mark class="search-highlight">$1</mark>')
  })
  
  return highlighted
}

function onSearchInput() {
  // Clear previous timeout
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }
  
  // Auto-search after 500ms of no typing
  searchTimeout.value = setTimeout(() => {
    if (vectorQuery.value.trim().length > 2) {
      performVectorSearch()
    }
  }, 500)
}

async function performVectorSearch() {
  if (!vectorQuery.value.trim()) return
  
  isSearching.value = true
  
  try {
    const response = await fetch('http://127.0.0.1:8000/api/vector-search/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: vectorQuery.value,
        top_k: 3
      })
    })
    
    if (!response.ok) {
      throw new Error(`Search failed: ${response.status}`)
    }
    
    const data = await response.json()
    vectorResults.value = data.results || []
    
    // Simulate processing time for animation
    await new Promise(resolve => setTimeout(resolve, 1500))
    
  } catch (e) {
    console.error('Vector search failed:', e)
    alert(`Search failed: ${e.message}`)
    vectorResults.value = []
  } finally {
    isSearching.value = false
  }
}

function clearVectorSearch() {
  vectorQuery.value = ''
  vectorResults.value = []
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }
}

function renderPreview(md) {
  if (!md) return '<em class="muted">(no content)</em>'
  const plain = md.replace(/[#*_`]/g, '')
  const trimmed = plain.length > 150 ? plain.slice(0, 150) + '...' : plain
  return marked.parse(trimmed)
}

function formatDate(dateStr) {
  if (!dateStr) return 'No date'
  return new Date(dateStr).toLocaleDateString()
}

const visiblePages = computed(() => {
  if (!q.value) return pages.value
  const s = q.value.toLowerCase()
  return pages.value.filter(p => (p.title || '').toLowerCase().includes(s) || (p.content || '').toLowerCase().includes(s))
})

const recentPages = computed(() => {
  return pages.value.filter(p => {
    if (!p.updated_at) return false
    const daysSince = (Date.now() - new Date(p.updated_at)) / (1000 * 60 * 60 * 24)
    return daysSince <= 7
  })
})

function filterPages() {
  // triggers computed update
}

onMounted(async () => {
  await refresh()
})

async function refresh() {
  loading.value = true
  error.value = null
  
  let url = 'http://127.0.0.1:8000/api/pages/'
  if (route.query.chapter) url += '?chapter=' + encodeURIComponent(route.query.chapter)
  
  try {
    const res = await fetch(url)
    if (!res.ok) {
      const errorText = await res.text()
      throw new Error(`HTTP ${res.status}: ${errorText}`)
    }
    const data = await res.json()
    pages.value = Array.isArray(data) ? data : []
    retryCount.value = 0
  } catch (e) {
    console.error('Failed to fetch pages:', e)
    pages.value = []
    
    // Set user-friendly error messages
    if (e.message.includes('500')) {
      error.value = {
        type: 'database',
        title: 'Database Not Ready',
        message: 'The database tables need to be created. Please run migrations in the backend.',
        action: 'Run: python manage.py migrate',
        icon: '🗄️'
      }
    } else if (e.message.includes('fetch')) {
      error.value = {
        type: 'connection',
        title: 'Backend Server Not Running',
        message: 'Cannot connect to the Django backend server.',
        action: 'Run: python manage.py runserver 127.0.0.1:8000',
        icon: '🔌'
      }
    } else {
      error.value = {
        type: 'unknown',
        title: 'Unknown Error',
        message: e.message,
        action: 'Check console for details',
        icon: '❌'
      }
    }
  } finally {
    loading.value = false
  }
}

async function deletePage(id) {
  if (!confirm('Delete this page?')) return
  
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/pages/${id}/`, { method: 'DELETE' })
    if (!res.ok) throw new Error(`Failed to delete: ${res.status}`)
    await refresh()
  } catch (e) {
    alert(`Failed to delete page: ${e.message}`)
  }
}

async function createPage() {
  if (!newTitle.value) return alert('Title required')
  
  loading.value = true
  try {
    const res = await fetch('http://127.0.0.1:8000/api/pages/', {
      method: 'POST', 
      headers: { 'Content-Type': 'application/json' }, 
      body: JSON.stringify({ title: newTitle.value, content: newContent.value })
    })
    
    if (!res.ok) {
      const errorText = await res.text()
      throw new Error(`HTTP ${res.status}: ${errorText}`)
    }
    
  const data = await res.json()
  showCreate.value = false
    newTitle.value = ''
    newContent.value = ''
    await refresh()
  router.push({ name: 'pages.view', params: { id: data.id } })
  } catch (e) {
    console.error('Failed to create page:', e)
    if (e.message.includes('500')) {
      alert('Database error: Please run migrations first (python manage.py migrate)')
    } else {
      alert(`Failed to create page: ${e.message}`)
    }
  } finally {
    loading.value = false
  }
}

async function retryConnection() {
  retryCount.value++
  await refresh()
}
</script>

<style scoped>
.pages-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: white;
}

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

.header-left {
  display: flex;
  align-items: center;
  gap: 40px;
}

.logo {
  font-size: 24px;
  font-weight: 900;
  color: #60a5fa;
  text-shadow: 0 0 20px #60a5fa;
}

.main-nav {
  display: flex;
  gap: 24px;
}

.nav-item {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.nav-item:hover,
.nav-item.active {
  color: white;
  background: rgba(96, 165, 250, 0.2);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.search-box {
  position: relative;
}

.search-input {
  padding: 8px 16px;
  border: 1px solid rgba(96, 165, 250, 0.3);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  color: white;
  width: 300px;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.create-btn {
  background: linear-gradient(135deg, #60a5fa 0%, #7dd3fc 100%);
  border: none;
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
}

.create-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(96, 165, 250, 0.4);
}

.dashboard-content {
  min-height: calc(100vh - 70px);
}

.main-panel {
  padding: 32px;
  overflow-y: auto;
}

.panel-header h1 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 8px;
  color: white;
}

.panel-header p {
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 32px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
  margin-bottom: 48px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(96, 165, 250, 0.2);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  font-size: 32px;
}

.stat-number {
  font-size: 28px;
  font-weight: 700;
  color: white;
}

.stat-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
}

.pages-section h2 {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 24px;
  color: white;
}

.pages-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
}

.page-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(96, 165, 250, 0.2);
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.page-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(96, 165, 250, 0.2);
  border-color: rgba(96, 165, 250, 0.4);
}

.page-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.page-icon {
  font-size: 24px;
}

.page-card h3 {
  font-size: 18px;
  font-weight: 600;
  color: white;
  margin: 0;
}

.page-preview {
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.5;
  margin-bottom: 16px;
  min-height: 60px;
}

.page-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-date {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
}

.page-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 4px 12px;
  border: 1px solid rgba(96, 165, 250, 0.3);
  background: transparent;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: rgba(96, 165, 250, 0.1);
}

.action-btn.danger {
  border-color: rgba(239, 68, 68, 0.5);
  color: rgba(239, 68, 68, 0.8);
}

.action-btn.danger:hover {
  background: rgba(239, 68, 68, 0.1);
}

/* Intelligent Vector Search Styles */
.intelligent-search-section {
  margin-bottom: 48px;
}

.search-container {
  position: relative;
  max-width: 800px;
  margin: 0 auto 32px auto;
}

.search-background {
  position: absolute;
  inset: 0;
  border-radius: 24px;
  overflow: hidden;
  z-index: 1;
}

.search-particles {
  position: absolute;
  inset: 0;
  background: 
    radial-gradient(circle at 20% 80%, rgba(96, 165, 250, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(167, 243, 208, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(196, 181, 253, 0.1) 0%, transparent 50%);
  animation: particleFloat 6s ease-in-out infinite;
}

.search-waves {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(96, 165, 250, 0.05) 25%, 
    rgba(167, 243, 208, 0.05) 50%, 
    rgba(196, 181, 253, 0.05) 75%, 
    transparent 100%);
  animation: waveFlow 4s linear infinite;
}

@keyframes particleFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(-10px, -10px) scale(1.05); }
  66% { transform: translate(10px, -5px) scale(0.95); }
}

@keyframes waveFlow {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.search-box-wrapper {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  border: 2px solid rgba(96, 165, 250, 0.3);
  border-radius: 24px;
  padding: 8px;
  transition: all 0.4s ease;
}

.search-box-wrapper:focus-within {
  border-color: rgba(96, 165, 250, 0.6);
  box-shadow: 
    0 0 30px rgba(96, 165, 250, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.search-icon-container {
  padding: 12px 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.magnifying-glass {
  position: relative;
  width: 32px;
  height: 32px;
  transition: all 0.3s ease;
}

.magnifying-glass.searching {
  animation: searchPulse 1.5s ease-in-out infinite;
}

@keyframes searchPulse {
  0%, 100% { transform: scale(1) rotate(0deg); }
  50% { transform: scale(1.1) rotate(5deg); }
}

.glass-body {
  width: 20px;
  height: 20px;
  border: 3px solid #60a5fa;
  border-radius: 50%;
  position: absolute;
  top: 2px;
  left: 2px;
  background: rgba(96, 165, 250, 0.1);
}

.glass-handle {
  width: 2px;
  height: 12px;
  background: #60a5fa;
  position: absolute;
  bottom: 2px;
  right: 4px;
  transform: rotate(45deg);
  border-radius: 2px;
}

.search-rays {
  position: absolute;
  inset: -8px;
  border-radius: 50%;
  background: conic-gradient(
    from 0deg,
    transparent 0deg,
    rgba(96, 165, 250, 0.2) 45deg,
    transparent 90deg,
    rgba(96, 165, 250, 0.2) 135deg,
    transparent 180deg,
    rgba(96, 165, 250, 0.2) 225deg,
    transparent 270deg,
    rgba(96, 165, 250, 0.2) 315deg,
    transparent 360deg
  );
  animation: rayRotate 3s linear infinite;
  opacity: 0;
}

.magnifying-glass.searching .search-rays {
  opacity: 1;
}

@keyframes rayRotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.intelligent-search-input {
  flex: 1;
  background: transparent;
  border: none;
  color: white;
  font-size: 18px;
  font-weight: 500;
  padding: 16px 20px;
  outline: none;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.intelligent-search-input::placeholder {
  color: rgba(255, 255, 255, 0.6);
  font-style: italic;
}

.search-actions {
  display: flex;
  gap: 8px;
  padding-right: 8px;
}

.vector-search-btn,
.clear-search-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.vector-search-btn {
  background: linear-gradient(135deg, #60a5fa 0%, #7dd3fc 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(96, 165, 250, 0.3);
}

.vector-search-btn:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(96, 165, 250, 0.4);
}

.vector-search-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.clear-search-btn {
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
}

.clear-search-btn:hover {
  background: rgba(239, 68, 68, 0.3);
  transform: translateY(-1px);
}

.searching-text {
  display: flex;
  align-items: center;
  gap: 8px;
}

.loading-dots {
  animation: loadingPulse 1.5s ease-in-out infinite;
}

@keyframes loadingPulse {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 1; }
}

/* Vector Embeddings Animation */
.vector-embeddings-animation {
  position: absolute;
  inset: -100px;
  z-index: 0;
  pointer-events: none;
}

.floating-vector {
  position: absolute;
  left: 50%;
  top: 50%;
  animation: vectorFloat var(--duration, 3s) ease-in-out infinite;
  animation-delay: var(--delay, 0s);
}

@keyframes vectorFloat {
  0%, 100% {
    transform: translate(calc(var(--x, 0px) * 0.8), calc(var(--y, 0px) * 0.8)) scale(0.8);
    opacity: 0.4;
  }
  50% {
    transform: translate(var(--x, 0px), var(--y, 0px)) scale(1.2);
    opacity: 1;
  }
}

.vector-dot {
  width: 8px;
  height: 8px;
  background: radial-gradient(circle, #60a5fa 0%, #7dd3fc 100%);
  border-radius: 50%;
  box-shadow: 0 0 10px rgba(96, 165, 250, 0.6);
}

.vector-connections {
  position: absolute;
  inset: -20px;
  border: 1px solid rgba(96, 165, 250, 0.2);
  border-radius: 50%;
  animation: connectionPulse 2s ease-in-out infinite;
}

@keyframes connectionPulse {
  0%, 100% { transform: scale(0.5); opacity: 0; }
  50% { transform: scale(1.5); opacity: 0.3; }
}

.ai-brain-center {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

.brain-core {
  width: 60px;
  height: 60px;
  position: relative;
  animation: brainPulse 2s ease-in-out infinite;
}

@keyframes brainPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.neural-pulse {
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(96, 165, 250, 0.6) 0%, rgba(96, 165, 250, 0.1) 70%, transparent 100%);
  border-radius: 50%;
  animation: neuralExpand 1.5s ease-out infinite;
}

@keyframes neuralExpand {
  0% { transform: scale(0.8); opacity: 1; }
  100% { transform: scale(2); opacity: 0; }
}

.processing-ring {
  position: absolute;
  inset: -10px;
  border: 2px solid transparent;
  border-top-color: #60a5fa;
  border-right-color: #7dd3fc;
  border-radius: 50%;
  animation: ringRotate 1s linear infinite;
}

@keyframes ringRotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Vector Results Section */
.vector-results-section {
  margin-top: 32px;
  padding: 32px;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(96, 165, 250, 0.2);
  border-radius: 24px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.results-header h3 {
  font-size: 24px;
  font-weight: 700;
  color: white;
  margin: 0;
}

.search-stats {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  background: rgba(96, 165, 250, 0.1);
  padding: 8px 16px;
  border-radius: 12px;
  border: 1px solid rgba(96, 165, 250, 0.2);
}

.vector-results-grid {
  display: grid;
  gap: 24px;
}

.vector-result-card {
  position: relative;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(96, 165, 250, 0.2);
  border-radius: 16px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.4s ease;
  animation: resultSlideIn 0.6s ease-out forwards;
  opacity: 0;
  transform: translateY(20px);
  overflow: hidden;
}

@keyframes resultSlideIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.vector-result-card:hover {
  transform: translateY(-4px);
  border-color: rgba(96, 165, 250, 0.4);
  box-shadow: 0 12px 32px rgba(96, 165, 250, 0.2);
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.result-rank {
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, #60a5fa 0%, #7dd3fc 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: white;
}

.result-title {
  font-size: 20px;
  font-weight: 600;
  color: white;
  margin: 0 0 12px 0;
  line-height: 1.3;
}

.result-preview {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.search-highlight {
  background: rgba(96, 165, 250, 0.3);
  color: #93c5fd;
  padding: 2px 4px;
  border-radius: 4px;
  font-weight: 600;
}

.result-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}

.result-glow {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(96, 165, 250, 0.1) 0%, rgba(167, 243, 208, 0.1) 100%);
  border-radius: 16px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.vector-result-card:hover .result-glow {
  opacity: 1;
}

@media (max-width: 768px) {
  .search-container {
    max-width: 100%;
    margin: 0 0 24px 0;
  }
  
  .search-box-wrapper {
    flex-direction: column;
    gap: 12px;
    padding: 16px;
  }
  
  .intelligent-search-input {
    text-align: center;
    padding: 12px;
  }
  
  .results-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .vector-results-grid {
    gap: 16px;
  }
}

/* Error & Loading States */
.error-card {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 32px;
  display: flex;
  align-items: center;
  gap: 24px;
}

.error-icon {
  font-size: 48px;
  flex-shrink: 0;
}

.error-content h3 {
  color: #fca5a5;
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.error-content p {
  color: rgba(255, 255, 255, 0.8);
  margin: 0 0 16px 0;
  line-height: 1.5;
}

.error-action {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 8px;
  padding: 12px 16px;
  margin-bottom: 16px;
}

.error-action code {
  color: #fca5a5;
  font-family: 'Courier New', monospace;
  font-size: 14px;
}

.error-buttons {
  display: flex;
  gap: 12px;
}

.retry-btn {
  background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
}

.retry-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.retry-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(96, 165, 250, 0.2);
  border-radius: 16px;
  padding: 48px;
  text-align: center;
  margin-bottom: 32px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(96, 165, 250, 0.2);
  border-top: 4px solid #60a5fa;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-card p {
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
}

.empty-state {
  text-align: center;
  padding: 64px 32px;
  color: rgba(255, 255, 255, 0.7);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 24px;
  font-weight: 600;
  color: white;
  margin: 0 0 8px 0;
}

.empty-state p {
  margin: 0 0 24px 0;
}

/* Modal Styles */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(2, 6, 23, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
  backdrop-filter: blur(8px);
}

.modal {
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95));
  border: 1px solid rgba(96, 165, 250, 0.2);
  border-radius: 16px;
  width: 600px;
  max-width: 90vw;
  max-height: 80vh;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid rgba(96, 165, 250, 0.2);
}

.modal-header h3 {
  font-size: 20px;
  font-weight: 600;
  color: white;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  font-size: 24px;
  cursor: pointer;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.modal-body {
  padding: 24px;
}

.title-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid rgba(96, 165, 250, 0.3);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  color: white;
  font-size: 16px;
  margin-bottom: 16px;
}

.content-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid rgba(96, 165, 250, 0.3);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  color: white;
  font-size: 14px;
  resize: vertical;
  min-height: 120px;
}

.title-input::placeholder,
.content-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.modal-footer {
  padding: 24px;
  border-top: 1px solid rgba(96, 165, 250, 0.2);
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-primary {
  background: linear-gradient(135deg, #60a5fa 0%, #7dd3fc 100%);
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(96, 165, 250, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background: transparent;
  border: 1px solid rgba(96, 165, 250, 0.3);
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover:not(:disabled) {
  background: rgba(96, 165, 250, 0.1);
}

.btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .main-nav {
    display: none;
  }
  
  .search-input {
    width: 200px;
  }
  
  .pages-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .modal {
    width: 95vw;
    margin: 20px;
  }
}
</style>
