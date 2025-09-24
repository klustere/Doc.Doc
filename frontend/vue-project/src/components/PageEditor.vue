<template>
  <div class="editor-dashboard">
    <HeaderBar />

    <!-- Main Content -->
    <div class="dashboard-content">
      <!-- Editor Panel -->
      <main class="editor-panel">
        <div class="panel-header">
          <div class="header-content">
            <h1>{{ isEdit ? 'Edit Page' : 'Create New Page' }}</h1>
            <p>{{ isEdit ? 'Make changes to your document' : 'Start creating your new document' }}</p>
          </div>
          <div class="header-actions">
            <button @click="savePage" class="save-btn" :disabled="!title.trim()">
              <span class="btn-icon">💾</span>
              {{ isEdit ? 'Update Page' : 'Save Page' }}
            </button>
          </div>
        </div>

        <!-- Title Input -->
        <div class="title-section">
          <input v-model="title" placeholder="Enter page title..." class="title-input" />
        </div>

        <!-- Toolbar -->
        <div class="toolbar">
          <div class="toolbar-group">
            <button class="tool-btn" @click="addBold" title="Bold">
              <strong>B</strong>
            </button>
            <button class="tool-btn" @click="addItalic" title="Italic">
              <em>I</em>
            </button>
            <button class="tool-btn" @click="addHeading" title="Heading">
              H1
            </button>
            <button class="tool-btn" @click="addList" title="List">
              •
            </button>
          </div>
          <div class="toolbar-info">
            Markdown supported
          </div>
        </div>

        <!-- Content Area -->
        <div class="content-section">
          <div class="content-header">
            <span>Content</span>
            <transition name="link-fade">
              <button v-if="selectedText" class="link-selected-btn" @click="linkSelectedText">
                <span class="link-icon">🔗</span>
                Link "{{ selectedText.slice(0, 20) }}{{ selectedText.length > 20 ? '...' : '' }}"
              </button>
            </transition>
          </div>
          <div class="textarea-container">
            <textarea 
              ref="contentTextarea"
              v-model="content" 
              rows="20" 
              placeholder="Start writing your content here... You can use Markdown formatting.

💡 Pro Tips:
• Select text and click 'Link' to create [Page Title] connections
• Use # for headings, ** for bold, * for italic
• The AI assistant can help improve your writing
• Auto-save keeps your work safe"
              class="content-area"
              @mouseup="checkSelection"
              @keyup="checkSelection"
              @input="handleContentChange"
            ></textarea>
            <div class="textarea-footer">
              <div class="word-count">
                {{ wordCount }} words • {{ charCount }} characters
              </div>
              <div v-if="lastSaved" class="last-saved">
                Last saved: {{ lastSaved }}
              </div>
            </div>
          </div>
        </div>
      </main>

      <!-- Sidebar -->
      <aside class="editor-sidebar">
        <div class="sidebar-section">
          <h3>Gemini Assistant</h3>
          <div class="gemini-panel">
            <GeminiPanel />
          </div>
        </div>

        <div class="sidebar-section">
          <h3>Subpages</h3>
          <div class="subpages-list">
            <div v-if="links.length === 0" class="empty-state">
              No subpages linked
            </div>
            <div v-else class="links-list">
              <div v-for="l in links" :key="l.id" class="link-item">
                <router-link :to="{ name: 'pages.view', params: { id: l.id } }" class="link-title">
                  {{ l.title || 'Untitled' }}
                </router-link>
                <button class="unlink-btn" @click="unlink(l.id)">×</button>
              </div>
            </div>
          </div>

          <!-- Link Tools -->
          <div class="link-tools">
            <input 
              v-model="typeQuery" 
              @input="autoFilter" 
              placeholder="Search pages to link..." 
              class="link-search"
            />
            <div v-if="showSuggestions" class="suggestions">
              <div 
                v-for="p in filteredPages" 
                :key="p.id" 
                class="suggestion-item" 
                @click="chooseSuggestion(p)"
              >
                {{ p.title || 'Untitled' }}
              </div>
            </div>
            <div class="link-actions">
              <button class="link-btn" @click="linkSelected">Link Selected</button>
              <button class="link-btn secondary" @click="createSubpageInline">Create & Link</button>
            </div>
          </div>
        </div>
      </aside>
    </div>
    
    <!-- Success Toast -->
    <transition name="toast-slide">
      <div v-if="snack" class="success-toast">
        <span class="toast-icon">✅</span>
        {{ snack }}
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import GeminiPanel from './GeminiPanel.vue'

const route = useRoute()
const router = useRouter()

const isEdit = ref(false)
const title = ref('')
const content = ref('')
const links = ref([])
const allPages = ref([])
const selectedLink = ref(null)
const typeQuery = ref('')
const filteredPages = ref([])
const showSuggestions = ref(false)
const newSubTitle = ref('')
const snack = ref('')
const highlight = ref(false)
const selectedText = ref('')
const selectionStart = ref(0)
const selectionEnd = ref(0)
const contentTextarea = ref(null)
const lastSaved = ref('')
const autoSaveTimer = ref(null)

// Computed properties
const wordCount = computed(() => {
  return content.value.trim() ? content.value.trim().split(/\s+/).length : 0
})

const charCount = computed(() => {
  return content.value.length
})

function addBold() { content.value += '**bold** ' }
function addItalic() { content.value += '*italic* ' }
function addHeading() { content.value += '\n# Heading\n' }
function addList() { content.value += '\n- List item\n' }

function handleContentChange() {
  // Clear previous auto-save timer
  if (autoSaveTimer.value) {
    clearTimeout(autoSaveTimer.value)
  }
  
  // Set new auto-save timer for 3 seconds
  autoSaveTimer.value = setTimeout(() => {
    if (route.params.id && content.value.trim()) {
      autoSave()
    }
  }, 3000)
}

async function autoSave() {
  if (!route.params.id || !title.value.trim()) return
  
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/pages/${route.params.id}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: title.value, content: content.value })
    })
    
    if (res.ok) {
      const now = new Date()
      lastSaved.value = now.toLocaleTimeString()
    }
  } catch (err) {
    console.log('Auto-save failed:', err)
  }
}

onMounted(async () => {
  if (route.params.id) {
    isEdit.value = true
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/pages/${route.params.id}/`)
      if (res.ok) {
        const data = await res.json()
        title.value = data.title
        content.value = data.content
        links.value = data.links || []
      }
    } catch (_) {}
  }
  try {
    const res2 = await fetch('http://127.0.0.1:8000/api/pages/')
    if (res2.ok) allPages.value = await res2.json()
  } catch (e) { allPages.value = [] }
  filteredPages.value = allPages.value
  highlight.value = true
  setTimeout(() => (highlight.value = false), 600)
})

async function linkSelected() {
  if (!route.params.id) return alert('Save the page first to add links')
  if (!selectedLink.value) return alert('Select a page to link')
  const res = await fetch(`http://127.0.0.1:8000/api/pages/${route.params.id}/links/`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ link_id: selectedLink.value })
  })
  if (res.ok) {
    const data = await res.json()
    links.value.push(data.link)
    selectedLink.value = null
  } else {
    alert('Failed to link page')
  }
}

async function unlink(id) {
  if (!route.params.id) return
  const res = await fetch(`http://127.0.0.1:8000/api/pages/${route.params.id}/links/`, {
    method: 'DELETE', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ link_id: id })
  })
  if (res.ok) links.value = links.value.filter(l => l.id !== id)
}

async function createSubpageInline() {
  if (!route.params.id) return alert('Save the page first to create subpages')
  const titleNew = newSubTitle.value || 'Untitled'
  const res = await fetch('http://127.0.0.1:8000/api/pages/', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ title: titleNew, content: '' })
  })
  if (res.ok) {
    const newPage = await res.json()
    await fetch(`http://127.0.0.1:8000/api/pages/${route.params.id}/links/`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ link_id: newPage.id })
    })
    links.value.push({ id: newPage.id, title: newPage.title })
    newSubTitle.value = ''
    snackShow('Subpage created and linked')
    router.push({ name: 'pages.edit', params: { id: newPage.id } })
  } else {
    alert('Failed to create subpage')
  }
}

function chooseSuggestion(p) { selectedLink.value = p.id; typeQuery.value = p.title; showSuggestions.value = false }

function autoFilter() {
  const q = (typeQuery.value || '').toLowerCase().trim()
  if (!q) { filteredPages.value = allPages.value; showSuggestions.value = false; return }
  filteredPages.value = allPages.value.filter(p => (p.title || '').toLowerCase().includes(q))
  showSuggestions.value = filteredPages.value.length > 0
}

function snackShow(msg) { snack.value = msg; setTimeout(() => (snack.value = ''), 2000) }

function checkSelection() {
  if (!contentTextarea.value) return
  const textarea = contentTextarea.value
  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  if (start !== end) {
    selectedText.value = content.value.slice(start, end)
    selectionStart.value = start
    selectionEnd.value = end
  } else {
    selectedText.value = ''
  }
}

async function linkSelectedText() {
  if (!selectedText.value) return
  
  // Check if selected text matches any existing page title
  const matchingPage = allPages.value.find(p => p.title.toLowerCase() === selectedText.value.toLowerCase())
  
  if (matchingPage) {
    // Replace selected text with [Page Title] format
    const before = content.value.slice(0, selectionStart.value)
    const after = content.value.slice(selectionEnd.value)
    content.value = before + `[${matchingPage.title}]` + after
    
    // Add link if we're editing an existing page
    if (route.params.id && !links.value.find(l => l.id === matchingPage.id)) {
      await linkPageById(matchingPage.id)
    }
    
    selectedText.value = ''
    snackShow(`Linked to ${matchingPage.title}`)
  } else {
    // Offer to create a new page with the selected text as title
    if (confirm(`Create new page titled "${selectedText.value}" and link it?`)) {
      await createAndLinkPage(selectedText.value)
    }
  }
}

async function linkPageById(pageId) {
  if (!route.params.id) return
  const res = await fetch(`http://127.0.0.1:8000/api/pages/${route.params.id}/links/`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ link_id: pageId })
  })
  if (res.ok) {
    const data = await res.json()
    links.value.push(data.link)
  }
}

async function createAndLinkPage(pageTitle) {
  // Create new page
  const res = await fetch('http://127.0.0.1:8000/api/pages/', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, 
    body: JSON.stringify({ title: pageTitle, content: `# ${pageTitle}\n\nContent for ${pageTitle} goes here...` })
  })
  
  if (res.ok) {
    const newPage = await res.json()
    
    // Replace selected text with [Page Title] format
    const before = content.value.slice(0, selectionStart.value)
    const after = content.value.slice(selectionEnd.value)
    content.value = before + `[${newPage.title}]` + after
    
    // Link to new page if we're editing an existing page
    if (route.params.id) {
      await linkPageById(newPage.id)
    }
    
    // Update allPages list
    allPages.value.push(newPage)
    selectedText.value = ''
    snackShow(`Created and linked ${newPage.title}`)
  } else {
    alert('Failed to create page')
  }
}

async function savePage() {
  if (!title.value.trim()) {
    alert('Please enter a title for your page')
    return
  }
  
  try {
    const url = route.params.id ? `http://127.0.0.1:8000/api/pages/${route.params.id}/` : 'http://127.0.0.1:8000/api/pages/'
    const method = route.params.id ? 'PUT' : 'POST'
    const res = await fetch(url, { 
      method, 
      headers: { 'Content-Type': 'application/json' }, 
      body: JSON.stringify({ title: title.value, content: content.value }) 
    })
    
    if (!res.ok) throw new Error('Save failed: ' + res.status)
    
    const data = await res.json()
    const now = new Date()
    lastSaved.value = now.toLocaleTimeString()
    
    // Show success feedback
    snackShow(route.params.id ? 'Page updated successfully!' : 'Page created successfully!')
    
    // Navigate to view page if this was a new page
    if (!route.params.id) {
      router.push({ name: 'pages.view', params: { id: data.id } })
    }
  } catch (err) { 
    alert('Failed to save page: ' + err.message)
  }
}
</script>

<style scoped>
.editor-dashboard {
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

.save-btn {
  background: linear-gradient(135deg, #60a5fa 0%, #7dd3fc 100%);
  border: none;
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
}

.save-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(96, 165, 250, 0.4);
}

.dashboard-content {
  display: grid;
  grid-template-columns: 1fr 420px;
  min-height: calc(100vh - 70px);
}

.editor-panel {
  padding: 32px;
  overflow-y: auto;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid rgba(96, 165, 250, 0.2);
}

.header-content h1 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 8px;
  color: white;
}

.header-content p {
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
}

.header-actions {
  flex-shrink: 0;
}

.save-btn {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  border: none;
  color: white;
  padding: 14px 24px;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  font-size: 15px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3);
}

.save-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2);
}

.btn-icon {
  font-size: 16px;
}

.title-section {
  margin-bottom: 24px;
}

.title-input {
  width: 100%;
  padding: 16px 20px;
  border: 1px solid rgba(96, 165, 250, 0.3);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
  color: white;
  font-size: 24px;
  font-weight: 600;
}

.title-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  margin-bottom: 24px;
  border: 1px solid rgba(96, 165, 250, 0.2);
}

.toolbar-group {
  display: flex;
  gap: 8px;
}

.tool-btn {
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(96, 165, 250, 0.3);
  color: white;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 36px;
}

.tool-btn:hover {
  background: rgba(96, 165, 250, 0.2);
  border-color: rgba(96, 165, 250, 0.5);
}

.toolbar-info {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
}

.content-section {
  margin-bottom: 24px;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.content-header span {
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
}

.link-selected-btn {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  border: none;
  color: white;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.link-selected-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

.link-icon {
  font-size: 14px;
}

.link-fade-enter-active, .link-fade-leave-active {
  transition: all 0.3s ease;
}

.link-fade-enter-from, .link-fade-leave-to {
  opacity: 0;
  transform: translateX(10px);
}

.textarea-container {
  position: relative;
}

.content-area {
  width: 100%;
  padding: 20px;
  border: 1px solid rgba(96, 165, 250, 0.3);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
  color: white;
  font-size: 14px;
  line-height: 1.6;
  resize: vertical;
  min-height: 400px;
  transition: all 0.2s ease;
}

.content-area:focus {
  outline: none;
  border-color: rgba(96, 165, 250, 0.6);
  box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1);
  background: rgba(255, 255, 255, 0.08);
}

.content-area::placeholder {
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.5;
}

.textarea-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
  padding: 0 4px;
  font-size: 12px;
}

.word-count {
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
}

.last-saved {
  color: rgba(16, 185, 129, 0.8);
  font-weight: 500;
}

.editor-sidebar {
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(10px);
  border-left: 1px solid rgba(96, 165, 250, 0.2);
  padding: 32px 24px;
  overflow-y: auto;
}

.sidebar-section {
  margin-bottom: 32px;
}

.sidebar-section h3 {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 16px;
}

.gemini-panel {
  background: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
  padding: 16px;
  border: 1px solid rgba(96, 165, 250, 0.1);
}

.subpages-list {
  margin-bottom: 16px;
}

.empty-state {
  color: rgba(255, 255, 255, 0.5);
  font-style: italic;
  text-align: center;
  padding: 20px;
}

.links-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.link-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(96, 165, 250, 0.1);
}

.link-title {
  color: white;
  text-decoration: none;
  font-size: 14px;
}

.link-title:hover {
  color: #60a5fa;
}

.unlink-btn {
  background: none;
  border: none;
  color: rgba(239, 68, 68, 0.7);
  cursor: pointer;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.unlink-btn:hover {
  background: rgba(239, 68, 68, 0.2);
  color: rgba(239, 68, 68, 1);
}

.link-tools {
  position: relative;
}

.link-search {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid rgba(96, 165, 250, 0.3);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  color: white;
  font-size: 12px;
  margin-bottom: 12px;
}

.link-search::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.suggestions {
  position: absolute;
  top: 40px;
  left: 0;
  right: 0;
  background: rgba(15, 23, 42, 0.95);
  border: 1px solid rgba(96, 165, 250, 0.3);
  border-radius: 8px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 50;
  backdrop-filter: blur(10px);
}

.suggestion-item {
  padding: 8px 12px;
  cursor: pointer;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
  border-bottom: 1px solid rgba(96, 165, 250, 0.1);
}

.suggestion-item:last-child {
  border-bottom: none;
}

.suggestion-item:hover {
  background: rgba(96, 165, 250, 0.1);
  color: white;
}

.link-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.link-btn {
  padding: 8px 12px;
  background: rgba(96, 165, 250, 0.2);
  border: 1px solid rgba(96, 165, 250, 0.3);
  color: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s ease;
}

.link-btn:hover {
  background: rgba(96, 165, 250, 0.3);
}

.link-btn.secondary {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.2);
}

.link-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.1);
}

@media (max-width: 768px) {
  .dashboard-content {
    grid-template-columns: 1fr;
  }
  
  .editor-sidebar {
    display: none;
  }
  
  .main-nav {
    display: none;
  }
  
  .title-input {
    font-size: 20px;
  }
}

/* Success Toast */
.success-toast {
  position: fixed;
  top: 20px;
  right: 20px;
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  color: white;
  padding: 12px 20px;
  border-radius: 12px;
  font-weight: 500;
  font-size: 14px;
  z-index: 1000;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
  display: flex;
  align-items: center;
  gap: 8px;
}

.toast-icon {
  font-size: 16px;
}

.toast-slide-enter-active, .toast-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.toast-slide-enter-from {
  opacity: 0;
  transform: translateX(100px) scale(0.8);
}

.toast-slide-leave-to {
  opacity: 0;
  transform: translateX(100px) scale(0.9);
}
</style>
