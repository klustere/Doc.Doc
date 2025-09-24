
<template>
  <div class="writing-assistant">
    <!-- Assistant Header -->
    <div class="assistant-header">
      <div class="header-left">
        <span class="ai-icon">🤖</span>
        <h4>Writing Assistant</h4>
      </div>
      <div v-if="contextAdded" class="context-badge">
        📄 Context Added
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="quick-actions">
      <button type="button" @click="showPromptFor('grammar')" class="action-btn">
        <span class="action-icon">✍️</span>
        Grammar Check
      </button>
      <button type="button" @click="showPromptFor('summary')" class="action-btn">
        <span class="action-icon">📝</span>
        Summarize
      </button>
    </div>

    <!-- Custom Prompt Section -->
    <div class="prompt-section">
      <div class="prompt-header">
        <span>Custom Request</span>
        <button v-if="promptText" @click="clearPrompt" class="clear-btn">Clear</button>
      </div>
      
      <div class="prompt-input-container">
        <textarea 
          v-model="promptText" 
          placeholder="Ask me to help with your writing... 
• Check grammar and spelling
• Improve clarity and tone  
• Generate ideas and content
• Restructure paragraphs
• Add examples or details"
          class="prompt-textarea"
          rows="4"
        ></textarea>
        
        <div class="prompt-actions">
          <button @click="sendPrompt" :disabled="!promptText.trim() || loading" class="send-btn">
            <span v-if="loading" class="loading-spinner"></span>
            <span v-else class="send-icon">🚀</span>
            {{ loading ? 'Thinking...' : 'Send' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Enhanced Loading Animation -->
    <div v-if="loading" class="loading-container">
      <div class="ai-brain-container">
        <!-- Neural Network Background -->
        <div class="neural-network">
          <div class="neural-grid"></div>
          <div class="neural-nodes"></div>
          <div class="neural-connections"></div>
          <div class="data-flow"></div>
        </div>
        
        <!-- Central AI Brain -->
        <div class="ai-brain">
          <div class="brain-core">
            <div class="core-pulse"></div>
            <span class="brain-emoji">🧠</span>
          </div>
          
          <!-- Processing Rings -->
          <div class="processing-rings">
            <div class="ring ring-1"></div>
            <div class="ring ring-2"></div>
            <div class="ring ring-3"></div>
          </div>
          
          <!-- Floating Data Particles -->
          <div class="data-particles">
            <div class="particle particle-1">💭</div>
            <div class="particle particle-2">✨</div>
            <div class="particle particle-3">🔮</div>
            <div class="particle particle-4">⚡</div>
            <div class="particle particle-5">💡</div>
            <div class="particle particle-6">🌟</div>
          </div>
        </div>
        
        <!-- Loading Progress -->
        <div class="loading-progress">
          <div class="progress-text">{{ loadingMessage }}</div>
          <div class="progress-bar">
            <div class="progress-fill"></div>
          </div>
          
          <!-- Typing Animation -->
          <div class="ai-typing">
            <span class="typing-label">AI Processing</span>
            <div class="typing-dots">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Response Section -->
    <transition name="response-appear">
      <div v-if="response || loading" class="response-section">
        <div class="response-header">
          <span class="response-title">✨ Assistant Response</span>
          <div class="response-actions">
            <button @click="copyResponse" class="action-icon-btn" title="Copy">📋</button>
            <button @click="insertResponse" class="action-icon-btn" title="Insert into content">📥</button>
            <button @click="clearResponse" class="action-icon-btn" title="Clear">✕</button>
          </div>
        </div>
        
        <div class="response-content">
          <div v-if="loading" class="response-loading">
            <div class="loading-spinner" style="display:inline-block;margin-right:8px;height:16px;width:16px;border-width:2px"></div>
            <strong>{{ loadingMessage }}</strong>
          </div>
          <div v-else class="response-text" v-html="formatResponse(response)"></div>
        </div>
        
        <div v-if="mockResponse" class="mock-notice">
          💡 Demo mode - Set GEMINI_API_KEY for real AI assistance
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { usePageStore } from '../stores/pageStore'

const store = usePageStore()
const route = useRoute()
const promptText = ref('')
const response = ref('')
const loading = ref(false)
const loadingMessage = ref('')
const mockResponse = ref(false)

// Quick action prompts
const quickPrompts = {
  grammar: 'Please check the grammar and spelling in the following text and suggest improvements:',
  summary: 'Please provide a concise summary of the following text:'
}

const contextAdded = computed(() => store.contextAdded)

// Loading messages that cycle during AI processing
const loadingMessages = [
  'Processing your request...',
  'Analyzing content...',
  'Generating response...'
]
async function showPromptFor(action) {
  // Show loading immediately so user sees progress even if something fails later
  loading.value = true
  response.value = ''
  mockResponse.value = false
  loadingMessage.value = loadingMessages[0]

  // Resolve current page ID (prefer store since PageView sets it, fallback to route)
  const pageId = (store?.current && store.current.id) || (route?.params && route.params.id)

  console.log('[GeminiPanel] quick action:', action, 'pageId:', pageId, 'store.current:', store?.current)
  if (!pageId) {
    loading.value = false
    response.value = 'Error: No page loaded (missing page ID). Open a page and try again.'
    return
  }

  // Cycle through loading messages
  let messageIndex = 0
  const messageInterval = setInterval(() => {
    messageIndex = (messageIndex + 1) % loadingMessages.length
    loadingMessage.value = loadingMessages[messageIndex]
    if (messageIndex === loadingMessages.length - 1) {
      clearInterval(messageInterval)
    }
  }, 1500)

  try {
    // Use exact same endpoint and format as working summarize
    const apiResponse = await fetch(`http://127.0.0.1:8000/api/pages/${pageId}/gemini/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        action: action === 'summary' ? 'summarize' : 'question',
        question: action === 'summary' ? '' : quickPrompts[action]
      })
    })
    
    clearInterval(messageInterval)
    
    if (apiResponse.ok) {
      const data = await apiResponse.json()
      response.value = data.response
      mockResponse.value = data.mock || false
      console.log('Success! Got response:', data.response.substring(0, 100) + '...')
    } else {
      throw new Error(`HTTP ${apiResponse.status}: ${apiResponse.statusText}`)
    }
  } catch (error) {
    clearInterval(messageInterval)
    console.error('Error:', error)
    response.value = `Error: ${error.message}. Please check if the backend server is running.`
    mockResponse.value = true
  }
  
  loading.value = false
}

async function sendPrompt() {
  if (!promptText.value.trim()) return
  
  loading.value = true
  mockResponse.value = false
  
  // Cycle through loading messages with varying timing
  let messageIndex = 0
  loadingMessage.value = loadingMessages[0]
  const messageInterval = setInterval(() => {
    messageIndex = (messageIndex + 1) % loadingMessages.length
    loadingMessage.value = loadingMessages[messageIndex]
    
    // If we've reached the last message, slow down the cycling
    if (messageIndex === loadingMessages.length - 1) {
      clearInterval(messageInterval)
    }
  }, messageIndex < 3 ? 1200 : 1800)
  
  try {
    const res = await fetch('http://127.0.0.1:8000/api/gemini/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: promptText.value }),
    })
    
    clearInterval(messageInterval)
    
    if (res.ok) {
      const data = await res.json()
      response.value = data.response
    } else {
      const text = await res.text().catch(() => '')
      console.error('sendPrompt server error', res.status, res.statusText, text)
      throw new Error('Failed to get response')
    }
  } catch (err) {
    clearInterval(messageInterval)
    console.error('sendPrompt error:', err)
    mockResponse.value = true
    response.value = generateMockResponse(promptText.value)
  }
  
  loading.value = false
}

function generateMockResponse(prompt) {
  const lowerPrompt = prompt.toLowerCase()
  
  if (lowerPrompt.includes('grammar')) {
    return `**Grammar Check Results:**

✅ **Good practices found:**
- Clear sentence structure
- Proper punctuation usage
- Consistent tense

💡 **Suggestions for improvement:**
- Consider varying sentence lengths for better flow
- Some passive voice could be made active
- A few comma splices could be corrected

**Overall:** Your writing shows good grammar fundamentals. Minor adjustments would enhance clarity and engagement.`
  }
  
  if (lowerPrompt.includes('improve') || lowerPrompt.includes('tone')) {
    return `**Tone & Clarity Improvements:**

🎯 **Current strengths:**
- Clear communication of main ideas
- Appropriate formality level

✨ **Enhancement suggestions:**
- Use more active voice for stronger impact
- Add transitional phrases for smoother flow  
- Consider more engaging vocabulary choices
- Break up longer sentences for readability

**Recommendation:** Your content has solid foundations. These refinements will make it more engaging and impactful.`
  }
  
  if (lowerPrompt.includes('summary') || lowerPrompt.includes('summarize')) {
    return `**Content Summary:**

📋 **Key Points:**
- Main concept clearly presented
- Supporting details provided
- Logical structure maintained

🎯 **Core Message:**
The text effectively communicates its primary objectives while maintaining reader engagement through structured presentation of ideas.

**Length:** Appropriately detailed for the scope of topics covered.`
  }
  
  if (lowerPrompt.includes('expand') || lowerPrompt.includes('detail')) {
    return `**Expansion Suggestions:**

🔍 **Areas to develop:**
- Add specific examples to illustrate key points
- Include relevant statistics or research
- Provide step-by-step processes where applicable
- Consider adding expert quotes or case studies

💡 **Additional ideas:**
- Explore potential challenges and solutions
- Discuss future implications
- Add personal insights or experiences
- Include relevant comparisons or analogies

**Next steps:** Choose 2-3 expansion areas that best serve your audience's needs.`
  }
  
  return `**AI Assistant Response:**

I've analyzed your request and here are my suggestions:

✨ **Key observations:**
- Well-structured content with clear intent
- Good foundation for further development
- Appropriate tone for the target audience

💡 **Recommendations:**
- Consider adding more specific examples
- Enhance transitions between ideas
- Strengthen opening and closing statements
- Review for consistent voice throughout

**Note:** This is a demo response. Connect your Gemini API key for personalized AI assistance tailored to your specific content.`
}

function formatResponse(text) {
  // Convert markdown to HTML with proper formatting
  let html = text
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
  
  // Clean up empty paragraphs
  html = html.replace(/<p><\/p>/g, '')
  
  return html
}

function copyResponse() {
  navigator.clipboard.writeText(response.value.replace(/\*\*/g, '').replace(/\*/g, ''))
  // Could add a toast notification here
}

function insertResponse() {
  // This would integrate with the parent editor to insert the response
  // For now, just copy to clipboard
  copyResponse()
}

function clearPrompt() {
  promptText.value = ''
  store.clearPrompt()
}

function clearResponse() {
  response.value = ''
  mockResponse.value = false
}
</script>

<style scoped>
.writing-assistant {
  background: rgba(15, 23, 42, 0.4);
  border: 1px solid rgba(96, 165, 250, 0.2);
  border-radius: 16px;
  padding: 20px;
  backdrop-filter: blur(10px);
}

.assistant-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(96, 165, 250, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.ai-icon {
  font-size: 20px;
  animation: iconPulse 3s ease-in-out infinite;
}

@keyframes iconPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.assistant-header h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #e2e8f0;
}

.context-badge {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 500;
}

.quick-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 20px;
}

.action-btn {
  background: rgba(96, 165, 250, 0.1);
  border: 1px solid rgba(96, 165, 250, 0.2);
  color: #e2e8f0;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.action-btn:hover {
  background: rgba(96, 165, 250, 0.2);
  border-color: rgba(96, 165, 250, 0.4);
  transform: translateY(-1px);
}

.action-icon {
  font-size: 14px;
}

.prompt-section {
  margin-bottom: 20px;
}

.prompt-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  font-size: 14px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.8);
}

.clear-btn {
  background: none;
  border: none;
  color: rgba(239, 68, 68, 0.7);
  cursor: pointer;
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.clear-btn:hover {
  color: rgba(239, 68, 68, 1);
  background: rgba(239, 68, 68, 0.1);
}

.prompt-input-container {
  position: relative;
}

.prompt-textarea {
  width: 100%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(96, 165, 250, 0.2);
  border-radius: 12px;
  color: #e2e8f0;
  padding: 16px;
  font-size: 13px;
  line-height: 1.5;
  resize: vertical;
  font-family: inherit;
}

.prompt-textarea::placeholder {
  color: rgba(255, 255, 255, 0.4);
  line-height: 1.4;
}

.prompt-textarea:focus {
  outline: none;
  border-color: rgba(96, 165, 250, 0.5);
  box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1);
}

.prompt-actions {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
}

.send-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  padding: 10px 18px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  font-size: 13px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.send-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.send-icon {
  font-size: 14px;
}

.loading-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-container {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(96, 165, 250, 0.3);
  border-radius: 16px;
  padding: 30px;
  margin: 16px 0;
  position: relative;
  overflow: hidden;
  min-height: 280px;
}

.ai-brain-container {
  position: relative;
  width: 100%;
  height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* Neural Network Background */
.neural-network {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0.3;
}

.neural-grid {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(circle at 20% 30%, rgba(102, 126, 234, 0.1) 1px, transparent 1px),
    radial-gradient(circle at 70% 20%, rgba(118, 75, 162, 0.1) 1px, transparent 1px),
    radial-gradient(circle at 40% 80%, rgba(240, 147, 251, 0.1) 1px, transparent 1px),
    radial-gradient(circle at 90% 60%, rgba(79, 172, 254, 0.1) 1px, transparent 1px);
  background-size: 40px 40px, 60px 60px, 50px 50px, 45px 45px;
  animation: neuralGrid 8s linear infinite;
}

@keyframes neuralGrid {
  0% { transform: translate(0, 0); }
  100% { transform: translate(20px, 20px); }
}

.neural-nodes {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.neural-nodes::before,
.neural-nodes::after {
  content: '';
  position: absolute;
  width: 4px;
  height: 4px;
  background: radial-gradient(circle, #667eea, #764ba2);
  border-radius: 50%;
  animation: nodeFloat 3s ease-in-out infinite;
  box-shadow: 
    30px 40px 0 rgba(102, 126, 234, 0.6),
    80px 20px 0 rgba(118, 75, 162, 0.6),
    120px 70px 0 rgba(240, 147, 251, 0.6),
    60px 90px 0 rgba(79, 172, 254, 0.6),
    200px 30px 0 rgba(16, 185, 129, 0.6),
    250px 80px 0 rgba(251, 191, 36, 0.6);
}

.neural-nodes::after {
  animation-delay: 1.5s;
  transform: translateX(150px);
}

@keyframes nodeFloat {
  0%, 100% {
    transform: translateY(0px) scale(1);
    opacity: 0.6;
  }
  50% {
    transform: translateY(-15px) scale(1.2);
    opacity: 1;
  }
}

.neural-connections {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.neural-connections::before,
.neural-connections::after {
  content: '';
  position: absolute;
  height: 1px;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(102, 126, 234, 0.4), 
    rgba(118, 75, 162, 0.6), 
    rgba(240, 147, 251, 0.4),
    transparent);
  animation: connectionPulse 4s ease-in-out infinite;
}

.neural-connections::before {
  top: 25%;
  left: 10%;
  width: 60%;
  animation-delay: 0s;
}

.neural-connections::after {
  top: 75%;
  right: 10%;
  width: 50%;
  animation-delay: 2s;
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

.data-flow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.data-flow::before,
.data-flow::after {
  content: '';
  position: absolute;
  width: 2px;
  height: 20px;
  background: linear-gradient(0deg, 
    transparent, 
    rgba(79, 172, 254, 0.8), 
    transparent);
  animation: dataStream 2s linear infinite;
}

.data-flow::before {
  top: 0;
  left: 30%;
  animation-delay: 0s;
}

.data-flow::after {
  top: 0;
  right: 30%;
  animation-delay: 1s;
}

@keyframes dataStream {
  0% {
    transform: translateY(-20px);
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: translateY(200px);
    opacity: 0;
  }
}

/* Central AI Brain */
.ai-brain {
  position: relative;
  z-index: 10;
  margin-bottom: 20px;
}

.brain-core {
  position: relative;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: radial-gradient(circle, 
    rgba(102, 126, 234, 0.2) 0%, 
    rgba(118, 75, 162, 0.3) 50%, 
    rgba(240, 147, 251, 0.2) 100%);
  border: 2px solid rgba(102, 126, 234, 0.4);
  animation: brainPulse 2s ease-in-out infinite;
}

@keyframes brainPulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
  }
  50% {
    transform: scale(1.1);
    box-shadow: 0 0 30px rgba(102, 126, 234, 0.6);
  }
}

.core-pulse {
  position: absolute;
  top: -10px;
  left: -10px;
  right: -10px;
  bottom: -10px;
  border: 2px solid rgba(102, 126, 234, 0.3);
  border-radius: 50%;
  animation: corePulseRing 3s ease-in-out infinite;
}

@keyframes corePulseRing {
  0% {
    transform: scale(0.8);
    opacity: 1;
  }
  100% {
    transform: scale(1.4);
    opacity: 0;
  }
}

.brain-emoji {
  font-size: 32px;
  animation: brainGlow 2s ease-in-out infinite;
}

@keyframes brainGlow {
  0%, 100% {
    filter: drop-shadow(0 0 5px rgba(102, 126, 234, 0.5));
  }
  50% {
    filter: drop-shadow(0 0 15px rgba(102, 126, 234, 0.8));
  }
}

/* Processing Rings */
.processing-rings {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.ring {
  position: absolute;
  border: 2px solid transparent;
  border-radius: 50%;
  border-top-color: rgba(102, 126, 234, 0.6);
  border-right-color: rgba(118, 75, 162, 0.4);
  animation: ringRotate 3s linear infinite;
}

.ring-1 {
  width: 100px;
  height: 100px;
  top: -50px;
  left: -50px;
  animation-duration: 2s;
}

.ring-2 {
  width: 130px;
  height: 130px;
  top: -65px;
  left: -65px;
  animation-duration: 3s;
  animation-direction: reverse;
}

.ring-3 {
  width: 160px;
  height: 160px;
  top: -80px;
  left: -80px;
  animation-duration: 4s;
}

@keyframes ringRotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Floating Data Particles */
.data-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.particle {
  position: absolute;
  font-size: 16px;
  animation: particleFloat 4s ease-in-out infinite;
  opacity: 0.7;
}

.particle-1 {
  top: 20%;
  left: 15%;
  animation-delay: 0s;
}

.particle-2 {
  top: 30%;
  right: 20%;
  animation-delay: 0.8s;
}

.particle-3 {
  top: 60%;
  left: 10%;
  animation-delay: 1.6s;
}

.particle-4 {
  top: 70%;
  right: 15%;
  animation-delay: 2.4s;
}

.particle-5 {
  top: 15%;
  left: 50%;
  animation-delay: 3.2s;
}

.particle-6 {
  top: 80%;
  left: 60%;
  animation-delay: 4s;
}

@keyframes particleFloat {
  0%, 100% {
    transform: translateY(0px) rotate(0deg) scale(1);
    opacity: 0.4;
  }
  25% {
    transform: translateY(-20px) rotate(90deg) scale(1.1);
    opacity: 0.8;
  }
  50% {
    transform: translateY(-10px) rotate(180deg) scale(0.9);
    opacity: 1;
  }
  75% {
    transform: translateY(-25px) rotate(270deg) scale(1.2);
    opacity: 0.6;
  }
}

/* Loading Progress */
.loading-progress {
  width: 100%;
  text-align: center;
  z-index: 10;
}

.progress-text {
  color: #e2e8f0;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 12px;
  animation: textShimmer 2s ease-in-out infinite;
}

@keyframes textShimmer {
  0%, 100% {
    opacity: 0.8;
    text-shadow: 0 0 5px rgba(102, 126, 234, 0.3);
  }
  50% {
    opacity: 1;
    text-shadow: 0 0 10px rgba(102, 126, 234, 0.6);
  }
}

.progress-bar {
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 12px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, 
    #667eea 0%, 
    #764ba2 25%, 
    #f093fb 50%, 
    #f5576c 75%, 
    #4facfe 100%);
  background-size: 200% 100%;
  animation: progressFlow 2s linear infinite;
  border-radius: 2px;
}

@keyframes progressFlow {
  0% {
    width: 0%;
    background-position: 0% 50%;
  }
  50% {
    width: 80%;
    background-position: 100% 50%;
  }
  100% {
    width: 100%;
    background-position: 200% 50%;
  }
}

.ai-typing {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.typing-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
  font-weight: 500;
}

.typing-dots {
  display: flex;
  gap: 3px;
}

.typing-dots span {
  width: 4px;
  height: 4px;
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

.response-appear-enter-active {
  transition: all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.response-appear-enter-from {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}

.response-section {
  background: rgba(16, 185, 129, 0.05);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 12px;
  padding: 16px;
  margin-top: 16px;
}

.response-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(16, 185, 129, 0.1);
}

.response-title {
  font-size: 14px;
  font-weight: 600;
  color: #10b981;
}

.response-actions {
  display: flex;
  gap: 4px;
}

.action-icon-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  font-size: 12px;
  transition: all 0.2s ease;
}

.action-icon-btn:hover {
  color: rgba(255, 255, 255, 0.9);
  background: rgba(255, 255, 255, 0.1);
}

.response-content {
  margin-bottom: 12px;
}

.response-text {
  color: #e2e8f0;
  font-size: 13px;
  line-height: 1.6;
}

.response-text h1,
.response-text h2,
.response-text h3 {
  margin: 16px 0 8px 0;
  color: #10b981;
  font-weight: 600;
}

.response-text h1 {
  font-size: 1.3rem;
  border-bottom: 2px solid rgba(16, 185, 129, 0.3);
  padding-bottom: 4px;
}

.response-text h2 {
  font-size: 1.1rem;
  border-bottom: 1px solid rgba(16, 185, 129, 0.2);
  padding-bottom: 2px;
}

.response-text h3 {
  font-size: 1rem;
}

.response-text code {
  background: rgba(255, 255, 255, 0.1);
  padding: 2px 4px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  color: #60a5fa;
}

.response-text pre {
  background: rgba(0, 0, 0, 0.3);
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
  margin: 10px 0;
  border-left: 3px solid #10b981;
}

.response-text pre code {
  background: none;
  padding: 0;
  color: #e5e7eb;
}

.response-text p {
  margin: 0 0 12px 0;
}

.response-text p:last-child {
  margin-bottom: 0;
}

.response-text strong {
  color: #10b981;
  font-weight: 600;
}

.response-text em {
  color: #60a5fa;
  font-style: italic;
}

.response-text ul {
  margin: 8px 0 12px 16px;
  padding: 0;
}

.response-text li {
  margin-bottom: 4px;
  color: rgba(255, 255, 255, 0.9);
}

.mock-notice {
  background: rgba(251, 191, 36, 0.1);
  border: 1px solid rgba(251, 191, 36, 0.2);
  color: rgba(251, 191, 36, 0.9);
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 11px;
  text-align: center;
}
</style>