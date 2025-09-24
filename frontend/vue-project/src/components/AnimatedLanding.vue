<template>
  <div class="landing-wrap">
    <!-- Matrix startup animation -->
    <div v-if="showMatrix" class="matrix-overlay">
      <canvas ref="matrixCanvas" class="matrix-canvas"></canvas>
    </div>
    
    <!-- Vector embeddings background -->
    <canvas ref="vectorCanvas" class="vector-canvas"></canvas>
    
    <!-- Magnifying glass cursor effect -->
    <div ref="magnifier" class="magnifier" :style="magnifierStyle"></div>
    
    <!-- Brand overlay -->
    <div class="brand-overlay">
      <h1 class="brand-title" :class="{ visible: showBrand }">doc.doc</h1>
      <div class="gemini-container" :class="{ visible: showBrand }">
        <canvas ref="geminiCanvas" class="gemini-trail"></canvas>
        <div class="gemini-text">
          <span class="powered-by">powered by</span>
          <span class="gemini-brand">GEMINI</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'

const matrixCanvas = ref(null)
const vectorCanvas = ref(null)
const geminiCanvas = ref(null)
const magnifier = ref(null)
const showMatrix = ref(true)
const showBrand = ref(false)

const mouse = ref({ x: 0, y: 0 })
const magnifierStyle = computed(() => ({
  left: `${mouse.value.x - 100}px`,
  top: `${mouse.value.y - 100}px`,
  opacity: showBrand.value ? 1 : 0
}))

let matrixAnimId = null
let vectorAnimId = null
let geminiAnimId = null
let vectors = []

onMounted(() => {
  startMatrixAnimation()
  setupMouseTracking()
  
  // After matrix animation, show brand and start main animations
  setTimeout(() => {
    showMatrix.value = false
    showBrand.value = true
    startVectorAnimation()
    startGeminiAnimation()
    
    // Notify page that landing is ready
    setTimeout(() => {
      window.dispatchEvent(new CustomEvent('landing-ready'))
    }, 800)
  }, 1500)
})

onUnmounted(() => {
  if (matrixAnimId) cancelAnimationFrame(matrixAnimId)
  if (vectorAnimId) cancelAnimationFrame(vectorAnimId)
  if (geminiAnimId) cancelAnimationFrame(geminiAnimId)
  window.removeEventListener('mousemove', handleMouseMove)
})

function setupMouseTracking() {
  window.addEventListener('mousemove', handleMouseMove)
}

function handleMouseMove(e) {
  const rect = vectorCanvas.value?.getBoundingClientRect()
  if (rect) {
    mouse.value.x = e.clientX - rect.left
    mouse.value.y = e.clientY - rect.top
  }
}

function startMatrixAnimation() {
  const canvas = matrixCanvas.value
  const ctx = canvas.getContext('2d')
  
  function resize() {
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
  }
  resize()
  
  const chars = '01'
  const fontSize = 20
  const columns = Math.floor(canvas.width / fontSize)
  const drops = Array(columns).fill(1)
  
  function draw() {
    ctx.fillStyle = 'rgba(3, 16, 38, 0.05)'
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    
    ctx.fillStyle = '#60a5fa'
    ctx.font = `${fontSize}px monospace`
    
    for (let i = 0; i < drops.length; i++) {
      const text = chars[Math.floor(Math.random() * chars.length)]
      ctx.fillText(text, i * fontSize, drops[i] * fontSize)
      
      if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
        drops[i] = 0
      }
      drops[i]++
    }
    
    matrixAnimId = requestAnimationFrame(draw)
  }
  draw()
}

function startVectorAnimation() {
  const canvas = vectorCanvas.value
  const ctx = canvas.getContext('2d')
  
  function resize() {
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
    initializeVectors()
  }
  resize()
  window.addEventListener('resize', resize)
  
  function initializeVectors() {
    vectors = []
    for (let i = 0; i < 60; i++) {
      const vectorType = Math.random()
      let value, isArray = false
      
      if (vectorType < 0.4) {
        // Array embeddings - generate arrays of 3-8 numbers
        const arrayLength = Math.floor(Math.random() * 6) + 3
        const embedding = []
        for (let j = 0; j < arrayLength; j++) {
          embedding.push((Math.random() * 2 - 1).toFixed(3))
        }
        value = `[${embedding.join(', ')}]`
        isArray = true
      } else if (vectorType < 0.7) {
        // Single float values
        value = (Math.random() * 2 - 1).toFixed(3)
        isArray = false
      } else {
        // Text labels
        value = ['doc', 'text', 'query', 'embed', 'vector', 'ai', 'search', 'graph'][Math.floor(Math.random() * 8)]
        isArray = false
      }
      
      vectors.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.6,
        vy: (Math.random() - 0.5) * 0.6,
        size: isArray ? Math.random() * 12 + 16 : Math.random() * 8 + 12,
        value: value,
        isArray: isArray,
        isNumeric: !isNaN(parseFloat(value)),
        originalX: 0,
        originalY: 0,
        targetX: 0,
        targetY: 0
      })
    }
  }
  
  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    
    // Draw subtle grid
    ctx.strokeStyle = 'rgba(96, 165, 250, 0.04)'
    ctx.lineWidth = 1
    for (let x = 0; x < canvas.width; x += 60) {
      ctx.beginPath()
      ctx.moveTo(x, 0)
      ctx.lineTo(x, canvas.height)
      ctx.stroke()
    }
    for (let y = 0; y < canvas.height; y += 60) {
      ctx.beginPath()
      ctx.moveTo(0, y)
      ctx.lineTo(canvas.width, y)
      ctx.stroke()
    }
    
    vectors.forEach(vector => {
      // Calculate distance from mouse
      const dx = vector.x - mouse.value.x
      const dy = vector.y - mouse.value.y
      const distance = Math.sqrt(dx * dx + dy * dy)
      const maxDistance = 150
      
      // Magnification effect
      const magnetism = Math.max(0, 1 - distance / maxDistance)
      const pullStrength = magnetism * 0.02
      
      // Apply magnetic pull towards mouse
      if (distance < maxDistance) {
        vector.x -= dx * pullStrength
        vector.y -= dy * pullStrength
      }
      
      // Normal movement
      vector.x += vector.vx
      vector.y += vector.vy
      
      // Boundary wrapping - account for larger embeddings
      const margin = vector.isArray ? 100 : 50
      if (vector.x < -margin) vector.x = canvas.width + margin
      if (vector.x > canvas.width + margin) vector.x = -margin
      if (vector.y < -margin) vector.y = canvas.height + margin
      if (vector.y > canvas.height + margin) vector.y = -margin
      
      // Draw vector
      ctx.save()
      
      // Enhanced visibility near cursor
      const alpha = 0.3 + magnetism * 0.7
      const size = vector.size + magnetism * 16
      
      if (distance < maxDistance) {
        // Draw connection line to mouse
        ctx.beginPath()
        ctx.moveTo(vector.x, vector.y)
        ctx.lineTo(mouse.value.x, mouse.value.y)
        ctx.strokeStyle = `rgba(96, 165, 250, ${magnetism * 0.5})`
        ctx.lineWidth = 1 + magnetism * 2
        ctx.stroke()
        
        // Enhanced glow effect
        ctx.shadowColor = '#60a5fa'
        ctx.shadowBlur = 10 + magnetism * 20
      }
      
      // Draw vector content
      ctx.fillStyle = `rgba(96, 165, 250, ${alpha})`
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'
      
      if (vector.isArray) {
        // Array embeddings - larger, multi-line display
        ctx.font = `${Math.max(16, size * 0.6)}px "SF Mono", Consolas, monospace`
        ctx.fillStyle = `rgba(125, 211, 252, ${alpha})`
        
        // Split long arrays into multiple lines for better readability
        const maxCharsPerLine = 25
        if (vector.value.length > maxCharsPerLine) {
          const lines = []
          let currentLine = ''
          const parts = vector.value.split(', ')
          
          for (let i = 0; i < parts.length; i++) {
            const part = parts[i] + (i < parts.length - 1 ? ', ' : '')
            if ((currentLine + part).length > maxCharsPerLine && currentLine.length > 0) {
              lines.push(currentLine)
              currentLine = part
            } else {
              currentLine += part
            }
          }
          if (currentLine.length > 0) lines.push(currentLine)
          
          // Draw multi-line embedding
          const lineHeight = size * 0.8
          const totalHeight = lines.length * lineHeight
          lines.forEach((line, index) => {
            const y = vector.y - totalHeight/2 + index * lineHeight + lineHeight/2
            ctx.fillText(line, vector.x, y)
          })
        } else {
          ctx.fillText(vector.value, vector.x, vector.y)
        }
      } else if (typeof vector.value === 'string' && isNaN(parseFloat(vector.value))) {
        // Text vectors - labels
        ctx.font = `${Math.max(20, size * 0.8)}px "SF Mono", Consolas, monospace`
        ctx.fillStyle = `rgba(244, 114, 182, ${alpha})`
        ctx.fillText(vector.value, vector.x, vector.y)
      } else {
        // Single numeric vectors
        ctx.font = `${Math.max(20, size * 0.7)}px "SF Mono", Consolas, monospace`
        ctx.fillStyle = `rgba(96, 165, 250, ${alpha})`
        ctx.fillText(vector.value, vector.x, vector.y)
      }
      
      ctx.restore()
    })
    
    vectorAnimId = requestAnimationFrame(draw)
  }
  draw()
}

function startGeminiAnimation() {
  const canvas = geminiCanvas.value
  const ctx = canvas.getContext('2d')
  
  canvas.width = 320
  canvas.height = 80
  
  let offset = 0
  
  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    
    const centerX = canvas.width / 2
    const centerY = canvas.height / 2
    
    // Rounded rectangle dimensions that wrap around the text
    const rectWidth = 300
    const rectHeight = 50
    const cornerRadius = 25
    const x = centerX - rectWidth / 2
    const y = centerY - rectHeight / 2
    
    // Draw animated particles around the rounded rectangle perimeter
    const perimeter = 2 * (rectWidth + rectHeight - 4 * cornerRadius) + 2 * Math.PI * cornerRadius
    const numParticles = 25
    
    for (let i = 0; i < numParticles; i++) {
      const progress = (offset + i * (perimeter / numParticles)) % perimeter
      const pos = getRoundedRectPoint(x, y, rectWidth, rectHeight, cornerRadius, progress / perimeter)
      
      const opacity = 0.9 - (i % 8) * 0.1
      const size = 5 - (i % 8) * 0.3
      const hue = (offset * 2 + i * 15) % 360
      
      ctx.beginPath()
      ctx.arc(pos.x, pos.y, size, 0, Math.PI * 2)
      ctx.fillStyle = `hsla(${200 + Math.sin(hue * 0.1) * 60}, 80%, 70%, ${opacity})`
      ctx.shadowColor = '#60a5fa'
      ctx.shadowBlur = 15
      ctx.fill()
    }
    
    offset += 1.5
    geminiAnimId = requestAnimationFrame(draw)
  }
  
  // Helper function to get points along rounded rectangle perimeter
  function getRoundedRectPoint(x, y, width, height, radius, t) {
    const perimeter = 2 * (width + height - 4 * radius) + 2 * Math.PI * radius
    const distance = t * perimeter
    
    // Top edge
    if (distance < width - 2 * radius) {
      return { x: x + radius + distance, y: y }
    }
    
    // Top-right corner
    const topRightStart = width - 2 * radius
    if (distance < topRightStart + Math.PI * radius / 2) {
      const angle = (distance - topRightStart) / radius - Math.PI / 2
      return {
        x: x + width - radius + Math.cos(angle) * radius,
        y: y + radius + Math.sin(angle) * radius
      }
    }
    
    // Right edge
    const rightStart = topRightStart + Math.PI * radius / 2
    if (distance < rightStart + height - 2 * radius) {
      return { x: x + width, y: y + radius + (distance - rightStart) }
    }
    
    // Bottom-right corner
    const bottomRightStart = rightStart + height - 2 * radius
    if (distance < bottomRightStart + Math.PI * radius / 2) {
      const angle = (distance - bottomRightStart) / radius
      return {
        x: x + width - radius + Math.cos(angle) * radius,
        y: y + height - radius + Math.sin(angle) * radius
      }
    }
    
    // Bottom edge
    const bottomStart = bottomRightStart + Math.PI * radius / 2
    if (distance < bottomStart + width - 2 * radius) {
      return { x: x + width - radius - (distance - bottomStart), y: y + height }
    }
    
    // Bottom-left corner
    const bottomLeftStart = bottomStart + width - 2 * radius
    if (distance < bottomLeftStart + Math.PI * radius / 2) {
      const angle = (distance - bottomLeftStart) / radius + Math.PI / 2
      return {
        x: x + radius + Math.cos(angle) * radius,
        y: y + height - radius + Math.sin(angle) * radius
      }
    }
    
    // Left edge
    const leftStart = bottomLeftStart + Math.PI * radius / 2
    if (distance < leftStart + height - 2 * radius) {
      return { x: x, y: y + height - radius - (distance - leftStart) }
    }
    
    // Top-left corner
    const topLeftStart = leftStart + height - 2 * radius
    const angle = (distance - topLeftStart) / radius + Math.PI
    return {
      x: x + radius + Math.cos(angle) * radius,
      y: y + radius + Math.sin(angle) * radius
    }
  }
  
  draw()
}
</script>

<style scoped>
.landing-wrap {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: linear-gradient(180deg, #031026 0%, #021026 100%);
  z-index: 1;
  overflow: hidden;
}

.matrix-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
}

.matrix-canvas,
.vector-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.vector-canvas {
  z-index: 1;
}

.magnifier {
  position: fixed;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: radial-gradient(circle at center, 
    rgba(96, 165, 250, 0.1) 0%,
    rgba(96, 165, 250, 0.05) 40%, 
    transparent 70%);
  border: 2px solid rgba(96, 165, 250, 0.3);
  box-shadow: 
    0 0 40px rgba(96, 165, 250, 0.2),
    inset 0 0 40px rgba(96, 165, 250, 0.1);
  backdrop-filter: blur(2px);
  pointer-events: none;
  z-index: 5;
  transition: opacity 0.3s ease;
  mix-blend-mode: screen;
}

.brand-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
  pointer-events: none;
}

.brand-title {
  font-size: 120px;
  font-weight: 900;
  color: white;
  text-shadow: 0 0 40px #60a5fa, 0 4px 8px rgba(0, 0, 0, 0.3);
  margin: 0;
  opacity: 0;
  transform: scale(0.8);
  transition: all 0.8s cubic-bezier(0.2, 0.9, 0.3, 1);
}

.brand-title.visible {
  opacity: 1;
  transform: scale(1);
}

.gemini-container {
  position: relative;
  margin-top: 20px;
  opacity: 0;
  transition: opacity 0.8s ease 0.3s;
}

.gemini-container.visible {
  opacity: 1;
}

.gemini-trail {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
}

.gemini-text {
  display: flex;
  align-items: baseline;
  gap: 8px;
  font-family: 'Courier New', monospace;
  position: relative;
  z-index: 2;
}

.powered-by {
  color: #9fbfff;
  font-size: 16px;
  font-weight: 400;
  letter-spacing: 1px;
  opacity: 0.8;
}

.gemini-brand {
  color: #ffffff;
  font-size: 24px;
  font-weight: 900;
  letter-spacing: 3px;
  text-shadow: 
    0 0 20px #60a5fa,
    0 0 40px #60a5fa,
    0 2px 4px rgba(0, 0, 0, 0.3);
  animation: gemini-pulse 3s ease-in-out infinite alternate;
}

@keyframes gemini-pulse {
  0% {
    text-shadow: 
      0 0 20px #60a5fa,
      0 0 40px #60a5fa,
      0 2px 4px rgba(0, 0, 0, 0.3);
  }
  100% {
    text-shadow: 
      0 0 30px #60a5fa,
      0 0 60px #60a5fa,
      0 0 80px #7dd3fc,
      0 2px 4px rgba(0, 0, 0, 0.3);
  }
}

@media (max-width: 768px) {
  .brand-title {
    font-size: 60px;
  }
  
  .powered-by {
    font-size: 12px;
  }
  
  .gemini-brand {
    font-size: 18px;
  }
  
  .magnifier {
    width: 120px;
    height: 120px;
  }
}
</style>