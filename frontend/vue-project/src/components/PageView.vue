<template>
  <div>
    <HeaderBar />
    <div class="page-view-container">
      <!-- Main Content -->
      <div class="main-content">
        <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:16px">
          <h2>{{ page.title }}</h2>
          <div style="display:flex;gap:8px">
            <button class="button ghost" @click="toggleVersionPanel">
              {{ showVersionPanel ? 'Hide' : 'Show' }} History
            </button>
            <button class="button ghost" @click="editPage">Edit</button>
            <button class="button secondary" @click="deletePage">Delete</button>
            <button class="button" @click="zoomOut">Zoom Out</button>
          </div>
        </div>
        <div style="margin-top:16px">
          <span v-html="renderWithLinks(page.content, links)"></span>
        </div>
        
        <div style="margin-top:20px">
          <button class="button ghost" @click="loadDescendants">Show descendants</button>
          <div v-if="descendants" style="margin-top:12px">
            <h4>Descendants tree</h4>
            <pre style="white-space:pre-wrap">{{ JSON.stringify(descendants, null, 2) }}</pre>
          </div>
        </div>
      </div>

      <!-- Gemini Assistant Side Panel -->
      <div class="gemini-side-panel" :class="{ expanded: geminiPanelExpanded }">
        <div class="gemini-panel-header">
          <h3>🤖 AI Assistant</h3>
        </div>
        
        <div class="gemini-panel-content">
          <div class="action-buttons">
            <button @click="summarizePage" :disabled="geminiLoading" class="gemini-btn primary">
              📋 Summarize
            </button>
            <button @click="showQuestionInput = !showQuestionInput" :disabled="geminiLoading" class="gemini-btn secondary">
              ❓ Ask Question
            </button>
          </div>
          
          <div v-if="showQuestionInput" class="question-input">
            <textarea 
              v-model="userQuestion" 
              placeholder="Ask about this page..."
              rows="3"
              class="question-textarea"
            ></textarea>
            <div class="question-actions">
              <button @click="askQuestion" :disabled="!userQuestion.trim() || geminiLoading" class="gemini-btn primary small">
                Send
              </button>
              <button @click="performDeepSearch" :disabled="!userQuestion.trim() || geminiLoading" class="gemini-btn deep-search small">
                🔍 Deep Search
              </button>
              <button @click="showQuestionInput = false" class="gemini-btn ghost small">
                Cancel
              </button>
            </div>
          </div>
          
          <div v-if="geminiLoading" class="gemini-loading-container">
            <div class="loading-glow-border">
              <div class="vector-background">
                <div class="vector-grid"></div>
                <div class="vector-dots"></div>
                <div class="vector-connections"></div>
                <div class="vector-particles"></div>
              </div>
              <div class="loading-content">
                <div class="ai-icon">🤖</div>
                <div class="loading-text-animation">
                  <span class="loading-stage">{{ loadingMessage }}</span>
                  <div class="typing-dots">
                    <span></span><span></span><span></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Response Area with Enhanced Animation -->
          <div class="response-container" :class="{ 'has-response': geminiResponse }">
            <transition name="response-slide" mode="out-in">
              <div v-if="geminiResponse" class="gemini-response" key="response">
                <div class="response-header">
                  <span class="response-type">
                    {{ lastAction === 'summarize' ? '📋 Summary' : 
                       lastAction === 'deep_search' ? '🔍 Deep Search' : '❓ Answer' }}
                  </span>
                  <div class="response-actions">
                    <button @click="copyResponse" class="action-btn" title="Copy">📋</button>
                    <button @click="clearResponse" class="action-btn" title="Clear">✕</button>
                  </div>
                </div>
                
                <!-- Search Statistics (for deep search) -->
                <transition name="stats-slide" appear>
                  <div v-if="searchStats && lastAction === 'deep_search'" class="search-stats">
                    <h4 class="stats-title">Search Statistics</h4>
                    <div class="stats-grid">
                      <div class="stat-item stat-animate" v-for="(stat, index) in statsItems" :key="stat.label" 
                           :style="{ animationDelay: `${index * 0.1}s` }">
                        <span :class="['stat-label', stat.class]">{{ stat.label }}:</span>
                        <span class="stat-value">{{ stat.value }}</span>
                      </div>
                      <div v-if="searchStats.search_depth" class="stat-item depth stat-animate" 
                           :style="{ animationDelay: '0.5s' }">
                        <span class="stat-label depth">Total Searched:</span>
                        <span class="stat-value">{{ searchStats.search_depth }}</span>
                      </div>
                    </div>
                  </div>
                </transition>
                
                <transition name="content-reveal" appear>
                  <div class="response-content" v-html="formatGeminiResponse(geminiResponse.response)"></div>
                </transition>
                
                <transition name="notice-fade" appear>
                  <div v-if="geminiResponse.mock" class="mock-notice">
                    💡 Demo mode - Set GEMINI_API_KEY for real AI responses
                  </div>
                </transition>
              </div>
            </transition>
          </div>
        </div>
      </div>

      <!-- Version History Panel -->
      <div v-if="showVersionPanel" class="version-history-panel">
        <div class="panel-header">
          <h3>Version History</h3>
          <button @click="toggleVersionPanel" class="close-btn">×</button>
        </div>
        
        <div class="panel-content">
          <div v-if="loadingVersions" class="loading">
            Loading version history...
          </div>
          
          <div v-else-if="pageVersions.length === 0" class="no-versions">
            <p>No version history available</p>
            <button @click="createMockVersions" class="button ghost">Generate Demo Versions</button>
          </div>
          
          <div v-else class="version-timeline">
            <div 
              v-for="version in pageVersions" 
              :key="version.id"
              class="timeline-item"
              @click="selectVersion(version)"
              :class="{ active: selectedVersion?.id === version.id }"
            >
              <div class="timeline-marker" :class="version.change_magnitude"></div>
              <div class="timeline-content">
                <div class="timeline-header">
                  <span class="version-number">v{{ version.version_number }}</span>
                  <span class="version-date">{{ formatDate(version.timestamp) }}</span>
                </div>
                <div class="timeline-time">{{ formatTime(version.timestamp) }}</div>
                <div class="timeline-summary">{{ version.summary }}</div>
                <div class="timeline-badges">
                  <span class="change-badge" :class="version.change_magnitude">
                    {{ version.change_magnitude }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { usePageStore } from '../stores/pageStore'
import { useRouter, useRoute } from 'vue-router'
import { marked } from 'marked'

const router = useRouter()
const route = useRoute()
const page = ref({ title: '', content: '' })
const store = usePageStore()
const links = ref([])
const descendants = ref(null)

// Version history data
const showVersionPanel = ref(false)
const pageVersions = ref([])
const selectedVersion = ref(null)
const loadingVersions = ref(false)

// Gemini assistant data
const showGeminiPanel = ref(false)
const showQuestionInput = ref(false)
const userQuestion = ref('')
const geminiResponse = ref(null)
const geminiLoading = ref(false)
const loadingMessage = ref('')
const loadingPhase = ref(0)

// Dynamic loading messages for different AI processes
const getLoadingMessage = (action, phase = 0) => {
  const messages = {
    summarize: [
      '🔍 Analyzing page content...',
      '🧠 Processing information...',
      '📝 Generating summary...',
      '✨ Finalizing response...'
    ],
    question: [
      '🤔 Understanding your question...',
      '🔍 Searching knowledge base...',
      '🧠 Formulating answer...',
      '💡 Preparing response...'
    ],
    deep_search: [
      '🌐 Scanning immediate neighbors (BFS)...',
      '🤖 AI classifying relevant pages...',
      '🔬 Exploring deeper connections (DFS)...',
      '🧠 Synthesizing comprehensive answer...',
      '✨ Finalizing deep search results...'
    ]
  }
  
  const actionMessages = messages[action] || messages.question
  return actionMessages[phase % actionMessages.length]
}
const lastAction = ref('')
const geminiPanelExpanded = ref(false)
const searchStats = ref(null)

// Computed property for animated stats items
const statsItems = computed(() => {
  if (!searchStats.value) return []
  return [
    { label: 'BFS Pages', value: searchStats.value.bfs_pages_found || 0, class: 'bfs' },
    { label: 'Relevant', value: searchStats.value.relevant_pages || 0, class: 'relevant' },
    { label: 'DFS Pages', value: searchStats.value.dfs_pages_found || 0, class: 'dfs' },
    { label: 'Total Context', value: searchStats.value.total_pages_analyzed || 0, class: 'total' }
  ]
})

function renderMarkdown(md) {
  return marked.parse(md || '')
}

function renderWithLinks(md, links) {
  let html = marked.parse(md || '')
  // Replace Confluence-style [Page Title] links with router-links if they match linked pages
  if (Array.isArray(links)) {
    links.forEach(l => {
      if (l.title) {
        // Replace [Page Title] with a router-link
        const linkHtml = `<a href="/pages/${l.id}" class="confluence-link" style="color: #60a5fa; text-decoration: underline;">${l.title}</a>`
        // Use regex to replace [Page Title] patterns
        const regex = new RegExp(`\\[${escapeRegExp(l.title)}\\]`, 'g')
        html = html.replace(regex, linkHtml)
      }
    })
  }
  return html
}

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

onMounted(async () => {
  const res = await fetch(`http://127.0.0.1:8000/api/pages/${route.params.id}/`)
  page.value = await res.json()
  links.value = page.value.links || []
  store.setPage(page.value)
})

function editPage() {
  router.push({ name: 'pages.edit', params: { id: route.params.id } })
}

async function deletePage() {
  if (!confirm('Delete this page?')) return
  await fetch(`http://127.0.0.1:8000/api/pages/${route.params.id}/`, { method: 'DELETE' })
  router.push({ name: 'pages.list' })
}

function zoomOut() {
  router.push({ name: 'graph', query: { focus: route.params.id } })
}

async function loadDescendants() {
  const res = await fetch(`http://127.0.0.1:8000/api/pages/${route.params.id}/descendants/`)
  if (res.ok) descendants.value = await res.json()
}

// Version history functions
async function toggleVersionPanel() {
  showVersionPanel.value = !showVersionPanel.value
  
  if (showVersionPanel.value && pageVersions.value.length === 0) {
    await loadVersionHistory()
  }
}

async function loadVersionHistory() {
  loadingVersions.value = true
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/pages/${route.params.id}/history/`)
    if (response.ok) {
      const data = await response.json()
      pageVersions.value = data.history || []
    } else {
      // If no version history endpoint, create mock data
      createMockVersions()
    }
  } catch (error) {
    console.error('Error loading version history:', error)
    // Create mock versions for demo
    createMockVersions()
  }
  loadingVersions.value = false
}

function createMockVersions() {
  const versions = []
  const versionCount = Math.floor(Math.random() * 8) + 3 // 3-10 versions
  
  for (let i = versionCount; i >= 1; i--) {
    const daysAgo = Math.floor(Math.random() * 90) + 1 // Last 90 days
    const date = new Date()
    date.setDate(date.getDate() - daysAgo)
    
    const summaries = [
      'Initial creation',
      'Added more details',
      'Fixed typos and formatting',
      'Updated content structure',
      'Added examples',
      'Improved explanations',
      'Added references',
      'Content reorganization',
      'Enhanced with diagrams',
      'Updated for accuracy'
    ]
    
    versions.push({
      id: `${route.params.id}_v${i}`,
      version_number: i,
      timestamp: date.toISOString(),
      summary: summaries[Math.floor(Math.random() * summaries.length)],
      change_magnitude: ['minor', 'medium', 'major'][Math.floor(Math.random() * 3)]
    })
  }
  
  pageVersions.value = versions.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
}

function selectVersion(version) {
  selectedVersion.value = selectedVersion.value?.id === version.id ? null : version
}

function formatDate(timestamp) {
  const date = new Date(timestamp)
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric' 
  })
}

function formatTime(timestamp) {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('en-US', { 
    hour: 'numeric', 
    minute: '2-digit',
    hour12: true 
  })
}

// Gemini assistant functions
function toggleGeminiPanel() {
  showGeminiPanel.value = !showGeminiPanel.value
  if (!showGeminiPanel.value) {
    showQuestionInput.value = false
    userQuestion.value = ''
  }
}

async function summarizePage() {
  lastAction.value = 'summarize'
  geminiLoading.value = true
  loadingPhase.value = 0
  loadingMessage.value = getLoadingMessage('summarize', 0)
  geminiPanelExpanded.value = true
  searchStats.value = null
  
  // Animate through loading phases
  const phaseInterval = setInterval(() => {
    loadingPhase.value = (loadingPhase.value + 1) % 4
    loadingMessage.value = getLoadingMessage('summarize', loadingPhase.value)
  }, 1200)
  
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/pages/${route.params.id}/gemini/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        action: 'summarize'
      })
    })
    
    clearInterval(phaseInterval)
    
    if (response.ok) {
      geminiResponse.value = await response.json()
    } else {
      throw new Error('Failed to get summary')
    }
  } catch (error) {
    clearInterval(phaseInterval)
    console.error('Error getting summary:', error)
    geminiResponse.value = {
      mock: true,
      response: 'Error: Could not connect to AI assistant. Please check your connection and try again.',
      action: 'summarize'
    }
  }
  
  geminiLoading.value = false
}

async function askQuestion() {
  if (!userQuestion.value.trim()) return
  
  lastAction.value = 'question'
  geminiLoading.value = true
  loadingPhase.value = 0
  loadingMessage.value = getLoadingMessage('question', 0)
  geminiPanelExpanded.value = true
  searchStats.value = null
  
  // Animate through loading phases
  const phaseInterval = setInterval(() => {
    loadingPhase.value = (loadingPhase.value + 1) % 4
    loadingMessage.value = getLoadingMessage('question', loadingPhase.value)
  }, 1000)
  
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/pages/${route.params.id}/gemini/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        action: 'question',
        question: userQuestion.value
      })
    })
    
    clearInterval(phaseInterval)
    
    if (response.ok) {
      geminiResponse.value = await response.json()
      showQuestionInput.value = false
      userQuestion.value = ''
    } else {
      throw new Error('Failed to get answer')
    }
  } catch (error) {
    clearInterval(phaseInterval)
    console.error('Error getting answer:', error)
    geminiResponse.value = {
      mock: true,
      response: 'Error: Could not connect to AI assistant. Please check your connection and try again.',
      action: 'question'
    }
  }
  
  geminiLoading.value = false
}

async function performDeepSearch() {
  if (!userQuestion.value.trim()) return
  
  lastAction.value = 'deep_search'
  geminiLoading.value = true
  loadingPhase.value = 0
  loadingMessage.value = getLoadingMessage('deep_search', 0)
  geminiPanelExpanded.value = true
  
  // Enhanced multi-stage loading with dynamic messages
  const phaseInterval = setInterval(() => {
    loadingPhase.value = (loadingPhase.value + 1) % 5
    loadingMessage.value = getLoadingMessage('deep_search', loadingPhase.value)
  }, 1800)
  
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/pages/${route.params.id}/gemini/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        action: 'deep_search',
        question: userQuestion.value
      })
    })
    
    clearInterval(phaseInterval)
    
    if (response.ok) {
      const result = await response.json()
      geminiResponse.value = result
      searchStats.value = result.search_stats || null
      showQuestionInput.value = false
      userQuestion.value = ''
    } else {
      throw new Error('Failed to perform deep search')
    }
  } catch (error) {
    clearInterval(phaseInterval)
    console.error('Error performing deep search:', error)
    geminiResponse.value = {
      mock: true,
      response: 'Error: Could not perform deep search. Please check your connection and try again.',
      action: 'deep_search'
    }
    searchStats.value = null
  }
  
  geminiLoading.value = false
}

function formatGeminiResponse(response) {
  // Convert markdown to HTML with proper formatting
  let html = response
    // Headers (## to h2, ### to h3, etc.)
    .replace(/^### (.*$)/gm, '<h3>$1</h3>')
    .replace(/^## (.*$)/gm, '<h2>$1</h2>')
    .replace(/^# (.*$)/gm, '<h1>$1</h1>')
    
    // Bold and italic
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    
    // Code blocks (```code```)
    .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
    
    // Inline code (`code`)
    .replace(/`(.*?)`/g, '<code>$1</code>')
    
    // Bullet points (- item or * item)
    .replace(/^[•\-\*] (.*)$/gm, '<li>$1</li>')
    
    // Line breaks and paragraphs
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br>')
  
  // Wrap lists properly
  html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
  
  // Wrap in paragraph if not already wrapped
  if (!html.startsWith('<h1>') && !html.startsWith('<h2>') && !html.startsWith('<h3>') && !html.startsWith('<ul>') && !html.startsWith('<pre>')) {
    html = '<p>' + html + '</p>'
  }
  
  return html
}

function copyResponse() {
  if (geminiResponse.value?.response) {
    navigator.clipboard.writeText(geminiResponse.value.response)
    // Could add a toast notification here
  }
}

function clearResponse() {
  geminiResponse.value = null
  lastAction.value = ''
  searchStats.value = null
  geminiPanelExpanded.value = false
}
</script>

<style scoped>
.page-view-container {
  display: flex;
  min-height: calc(100vh - 70px);
}

.main-content {
  flex: 1;
  padding: 0 20px;
  transition: margin-right 0.3s ease;
}

.version-history-panel {
  width: 400px;
  min-width: 400px;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: white;
  border-left: 1px solid rgba(96, 165, 250, 0.2);
  overflow-y: auto;
  animation: slideInFromRight 0.3s ease-out;
}

@keyframes slideInFromRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.panel-header {
  padding: 20px;
  border-bottom: 1px solid rgba(96, 165, 250, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 10;
}

.panel-header h3 {
  margin: 0;
  color: #60a5fa;
  font-size: 1.2rem;
}

.close-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.close-btn:hover {
  color: white;
  background: rgba(96, 165, 250, 0.2);
}

.panel-content {
  padding: 20px;
}

.loading {
  text-align: center;
  padding: 40px;
  color: rgba(255, 255, 255, 0.6);
}

.no-versions {
  text-align: center;
  padding: 40px;
  color: rgba(255, 255, 255, 0.6);
}

.no-versions p {
  margin-bottom: 16px;
}

.version-timeline {
  position: relative;
}

.timeline-item {
  display: flex;
  margin-bottom: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  border-radius: 8px;
  padding: 12px;
  position: relative;
}

.timeline-item:hover {
  background: rgba(96, 165, 250, 0.1);
  transform: translateX(4px);
}

.timeline-item.active {
  background: rgba(96, 165, 250, 0.2);
  border: 1px solid rgba(96, 165, 250, 0.4);
}

.timeline-item:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 22px;
  top: 36px;
  width: 2px;
  height: calc(100% + 8px);
  background: rgba(96, 165, 250, 0.3);
}

.timeline-marker {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  margin-right: 15px;
  margin-top: 4px;
  flex-shrink: 0;
  z-index: 1;
  border: 2px solid rgba(15, 23, 42, 1);
}

.timeline-marker.minor { background: #4CAF50; }
.timeline-marker.medium { background: #2196F3; }
.timeline-marker.major { background: #F44336; }

.timeline-content {
  flex: 1;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.version-number {
  font-weight: bold;
  color: #60a5fa;
  font-size: 1rem;
}

.version-date {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

.timeline-time {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 8px;
}

.timeline-summary {
  margin-bottom: 8px;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.4;
  font-size: 0.9rem;
}

.timeline-badges {
  display: flex;
  gap: 6px;
}

.change-badge {
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: bold;
  display: inline-block;
  text-transform: uppercase;
}

.change-badge.minor { 
  background: rgba(76, 175, 80, 0.3); 
  color: #81C784;
  border: 1px solid rgba(76, 175, 80, 0.5);
}
.change-badge.medium { 
  background: rgba(33, 150, 243, 0.3); 
  color: #64B5F6;
  border: 1px solid rgba(33, 150, 243, 0.5);
}
.change-badge.major { 
  background: rgba(244, 67, 54, 0.3); 
  color: #E57373;
  border: 1px solid rgba(244, 67, 54, 0.5);
}

/* Gemini Assistant Side Panel */
.gemini-side-panel {
  width: 320px;
  min-width: 320px;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: white;
  border-left: 1px solid rgba(96, 165, 250, 0.2);
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
}

.gemini-side-panel.expanded {
  width: 480px;
  min-width: 480px;
}

.gemini-panel-header {
  padding: 20px;
  border-bottom: 1px solid rgba(96, 165, 250, 0.2);
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 10;
}

.gemini-panel-header h3 {
  margin: 0;
  color: #60a5fa;
  font-size: 1.2rem;
  font-weight: 600;
}

.gemini-panel-content {
  padding: 20px;
  flex: 1;
  overflow-y: auto;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.gemini-btn {
  padding: 12px 16px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 0.9rem;
}

.gemini-btn.primary {
  background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
  color: white;
}

.gemini-btn.primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(96, 165, 250, 0.4);
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.gemini-btn.secondary {
  background: rgba(96, 165, 250, 0.2);
  color: #60a5fa;
  border: 1px solid rgba(96, 165, 250, 0.3);
}

.gemini-btn.secondary:hover:not(:disabled) {
  background: rgba(96, 165, 250, 0.3);
  border-color: rgba(96, 165, 250, 0.5);
}

.gemini-btn.ghost {
  background: transparent;
  color: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(96, 165, 250, 0.2);
}

.gemini-btn.ghost:hover:not(:disabled) {
  background: rgba(96, 165, 250, 0.1);
  color: white;
}

.gemini-btn.small {
  padding: 8px 12px;
  font-size: 0.85rem;
}

.gemini-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.question-input {
  margin-bottom: 20px;
  padding: 16px;
  background: rgba(96, 165, 250, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(96, 165, 250, 0.2);
  animation: slideDown 0.3s ease-out;
}

.question-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid rgba(96, 165, 250, 0.3);
  border-radius: 6px;
  font-family: inherit;
  font-size: 0.9rem;
  resize: vertical;
  min-height: 80px;
  background: rgba(15, 23, 42, 0.5);
  color: white;
}

.question-textarea::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.question-textarea:focus {
  outline: none;
  border-color: #60a5fa;
  box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.2);
}

.question-actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.gemini-loading {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: rgba(96, 165, 250, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(96, 165, 250, 0.3);
  color: #60a5fa;
  margin-bottom: 20px;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(96, 165, 250, 0.3);
  border-top: 2px solid #60a5fa;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Response Container with Expansion Animation */
.response-container {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.response-container.has-response {
  margin-top: 20px;
}

/* Enhanced Response Slide Animation */
.response-slide-enter-active {
  transition: all 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.response-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.response-slide-enter-from {
  opacity: 0;
  transform: translateY(-30px) scale(0.9) rotateX(15deg);
  filter: blur(5px);
}

.response-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.98);
}

/* Stats Animation */
.stats-slide-enter-active {
  transition: all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.stats-slide-enter-from {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}

.stat-animate {
  animation: statPop 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
  opacity: 0;
  transform: translateY(10px) scale(0.9);
}

@keyframes statPop {
  0% {
    opacity: 0;
    transform: translateY(10px) scale(0.9);
  }
  60% {
    transform: translateY(-2px) scale(1.02);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Content Reveal Animation */
.content-reveal-enter-active {
  transition: all 1s cubic-bezier(0.23, 1, 0.32, 1);
}

.content-reveal-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.content-reveal-enter-to {
  opacity: 1;
  transform: translateY(0);
}

/* Notice Fade Animation */
.notice-fade-enter-active {
  transition: all 0.5s ease-out;
  transition-delay: 0.3s;
}

.notice-fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

/* Search Statistics Styles */
.search-stats {
  background: #1a1a2e;
  border: 1px solid #16213e;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}

.stats-title {
  color: #e2e8f0;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 12px;
  border-bottom: 1px solid #16213e;
  padding-bottom: 8px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #0f172a;
  border-radius: 6px;
  border: 1px solid #334155;
}

.stat-item.depth {
  grid-column: 1 / -1;
}

.stat-label {
  font-size: 12px;
  font-weight: 500;
}

.stat-label.bfs { color: #60a5fa; }
.stat-label.relevant { color: #34d399; }
.stat-label.dfs { color: #a78bfa; }
.stat-label.total { color: #fbbf24; }
.stat-label.depth { color: #f472b6; }

.stat-value {
  color: #e2e8f0;
  font-weight: 600;
  font-size: 14px;
}

/* Deep Search Button Styles */
/* Loading Animation Styles */
.gemini-loading-container {
  position: relative;
  min-height: 200px;
  overflow: hidden;
  border-radius: 12px;
}

.loading-glow-border {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 200px;
  background: #0f172a;
  border-radius: 12px;
  padding: 3px;
  background: linear-gradient(45deg, 
    #667eea, #764ba2, #f093fb, #f5576c, 
    #4facfe, #00f2fe, #667eea);
  background-size: 400% 400%;
  animation: glowBorder 3s ease-in-out infinite;
}

@keyframes glowBorder {
  0%, 100% {
    background-position: 0% 50%;
    box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
  }
  25% {
    background-position: 100% 50%;
    box-shadow: 0 0 30px rgba(118, 75, 162, 0.4);
  }
  50% {
    background-position: 50% 100%;
    box-shadow: 0 0 40px rgba(240, 147, 251, 0.3);
  }
  75% {
    background-position: 0% 100%;
    box-shadow: 0 0 35px rgba(245, 87, 108, 0.4);
  }
}

.loading-glow-border::before {
  content: '';
  position: absolute;
  top: 3px;
  left: 3px;
  right: 3px;
  bottom: 3px;
  background: #0f172a;
  border-radius: 9px;
  z-index: 1;
}

.vector-background {
  position: absolute;
  top: 3px;
  left: 3px;
  right: 3px;
  bottom: 3px;
  border-radius: 9px;
  overflow: hidden;
  z-index: 2;
}

.vector-grid {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(102, 126, 234, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(102, 126, 234, 0.1) 1px, transparent 1px);
  background-size: 20px 20px;
  animation: gridMove 4s linear infinite;
}

@keyframes gridMove {
  0% { transform: translate(0, 0); }
  100% { transform: translate(20px, 20px); }
}

.vector-dots {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.vector-dots::before,
.vector-dots::after {
  content: '';
  position: absolute;
  width: 4px;
  height: 4px;
  background: #667eea;
  border-radius: 50%;
  animation: dotFloat 2s ease-in-out infinite;
  box-shadow: 
    0 0 10px rgba(102, 126, 234, 0.8),
    40px 30px 0 #764ba2,
    80px 60px 0 #f093fb,
    120px 20px 0 #4facfe,
    160px 80px 0 #00f2fe;
}

.vector-dots::after {
  animation-delay: 1s;
  transform: translateX(200px);
}

@keyframes dotFloat {
  0%, 100% {
    transform: translateY(0px) scale(1);
    opacity: 0.7;
  }
  50% {
    transform: translateY(-20px) scale(1.2);
    opacity: 1;
  }
}

.vector-connections {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.vector-connections::before,
.vector-connections::after {
  content: '';
  position: absolute;
  height: 1px;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(102, 126, 234, 0.6), 
    rgba(118, 75, 162, 0.6), 
    transparent);
  animation: connectionPulse 3s ease-in-out infinite;
}

.vector-connections::before {
  top: 30%;
  left: 0;
  width: 70%;
  animation-delay: 0.5s;
}

.vector-connections::after {
  top: 70%;
  right: 0;
  width: 60%;
  animation-delay: 1.5s;
}

@keyframes connectionPulse {
  0%, 100% {
    opacity: 0;
    transform: scaleX(0);
  }
  50% {
    opacity: 1;
    transform: scaleX(1);
  }
}

.vector-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.vector-particles::before,
.vector-particles::after {
  content: '';
  position: absolute;
  width: 2px;
  height: 2px;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.8) 0%, transparent 70%);
  border-radius: 50%;
  animation: particleFloat 4s ease-in-out infinite;
}

.vector-particles::before {
  top: 20%;
  left: 10%;
  animation-delay: 0s;
  box-shadow: 
    60px 40px 0 rgba(118, 75, 162, 0.6),
    120px 80px 0 rgba(240, 147, 251, 0.5),
    180px 20px 0 rgba(79, 172, 254, 0.7);
}

.vector-particles::after {
  top: 60%;
  right: 15%;
  animation-delay: 2s;
  box-shadow: 
    -40px -20px 0 rgba(0, 242, 254, 0.6),
    -80px 30px 0 rgba(245, 87, 108, 0.5),
    -120px -40px 0 rgba(102, 126, 234, 0.7);
}

@keyframes particleFloat {
  0%, 100% {
    transform: translateY(0px) translateX(0px) scale(1);
    opacity: 0.3;
  }
  25% {
    transform: translateY(-15px) translateX(10px) scale(1.1);
    opacity: 0.8;
  }
  50% {
    transform: translateY(-10px) translateX(-5px) scale(0.9);
    opacity: 0.6;
  }
  75% {
    transform: translateY(5px) translateX(-10px) scale(1.05);
    opacity: 0.9;
  }
}

.loading-content {
  position: relative;
  z-index: 3;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 194px;
  padding: 20px;
}

.ai-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  animation: iconPulse 2s ease-in-out infinite;
  filter: drop-shadow(0 0 10px rgba(102, 126, 234, 0.5));
}

@keyframes iconPulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.loading-text-animation {
  text-align: center;
}

.loading-stage {
  color: #e2e8f0;
  font-size: 1.1rem;
  font-weight: 500;
  display: block;
  margin-bottom: 10px;
  animation: textGlow 2s ease-in-out infinite;
}

@keyframes textGlow {
  0%, 100% {
    text-shadow: 0 0 5px rgba(102, 126, 234, 0.3);
  }
  50% {
    text-shadow: 0 0 15px rgba(102, 126, 234, 0.6);
  }
}

.typing-dots {
  display: flex;
  justify-content: center;
  gap: 4px;
}

.typing-dots span {
  width: 6px;
  height: 6px;
  background: #667eea;
  border-radius: 50%;
  animation: typingDot 1.4s ease-in-out infinite;
}

.typing-dots span:nth-child(1) { animation-delay: 0s; }
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typingDot {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1.2);
    opacity: 1;
  }
}

.gemini-btn.deep-search {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: 1px solid #764ba2;
}

.gemini-btn.deep-search:hover:not(:disabled) {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(118, 75, 162, 0.3);
}

.gemini-response {
  border-radius: 8px;
  border: 1px solid rgba(96, 165, 250, 0.3);
  overflow: hidden;
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(10px);
}

.response-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: rgba(96, 165, 250, 0.1);
  border-bottom: 1px solid rgba(96, 165, 250, 0.2);
}

.response-type {
  font-weight: 600;
  color: #60a5fa;
  font-size: 0.9rem;
}

.response-actions {
  display: flex;
  gap: 6px;
}

.action-btn {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s ease;
  font-size: 0.85rem;
}

.action-btn:hover {
  color: white;
  background: rgba(96, 165, 250, 0.2);
}

.response-content {
  padding: 16px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
}

.response-content h1,
.response-content h2,
.response-content h3 {
  margin: 16px 0 8px 0;
  color: #60a5fa;
  font-weight: 600;
}

.response-content h1 {
  font-size: 1.4rem;
  border-bottom: 2px solid rgba(96, 165, 250, 0.3);
  padding-bottom: 4px;
}

.response-content h2 {
  font-size: 1.2rem;
  border-bottom: 1px solid rgba(96, 165, 250, 0.2);
  padding-bottom: 2px;
}

.response-content h3 {
  font-size: 1.1rem;
}

.response-content ul {
  margin: 8px 0;
  padding-left: 20px;
}

.response-content li {
  margin: 4px 0;
  color: rgba(255, 255, 255, 0.8);
}

.response-content code {
  background: rgba(255, 255, 255, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  color: #7dd3fc;
}

.response-content pre {
  background: rgba(0, 0, 0, 0.3);
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 12px 0;
}

.response-content pre code {
  background: none;
  padding: 0;
  color: #e5e7eb;
}

.response-content p {
  margin: 0 0 12px 0;
}

.response-content p:last-child {
  margin-bottom: 0;
}

.response-content strong {
  color: #60a5fa;
  font-weight: 600;
}

.response-content em {
  color: rgba(255, 255, 255, 0.7);
  font-style: italic;
}

.mock-notice {
  padding: 12px 16px;
  background: rgba(251, 191, 36, 0.1);
  border-top: 1px solid rgba(251, 191, 36, 0.2);
  color: #fbbf24;
  font-size: 0.8rem;
  text-align: center;
}

/* Responsive design for smaller screens */
@media (max-width: 768px) {
  .action-buttons {
    flex-direction: column;
  }
  
  .gemini-btn {
    justify-content: center;
  }
  
  .question-actions {
    flex-direction: column;
  }
}

/* Version History Panel Responsive design */
@media (max-width: 1200px) {
  .version-history-panel {
    width: 350px;
    min-width: 350px;
  }
}

@media (max-width: 900px) {
  .page-view-container {
    flex-direction: column;
  }
  
  .version-history-panel {
    width: 100%;
    min-width: 100%;
    max-height: 50vh;
  }
}
</style>
