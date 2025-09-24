<template>
  <div>
    <div class="graph-wrap" ref="graphWrap">
      <div class="controls">
        <button @click="fit">Zoom Out (Fit)</button>
        <button @click="layout">Relayout</button>
        <button @click="reload">Reload Graph</button>
      </div>
      <div v-if="noData" class="no-data">
        <h3>No Graph Data Available</h3>
        /* make slightly transparent so vector canvas underneath shows through */
        background: linear-gradient(180deg, rgba(15,23,42,0.85), rgba(2,6,23,0.85)); 
        <p>Try running the population script or creating some pages with links.</p>
      </div>
      <div v-else class="cy-wrap">
        <canvas ref="vectorCanvas" class="vector-canvas"></canvas>
        <div ref="cyRef" class="cy"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import cytoscape from 'cytoscape'
import { useRouter, useRoute } from 'vue-router'

const cyRef = ref(null)
const graphWrap = ref(null)
const vectorCanvas = ref(null)
let cy = null
const router = useRouter()
const route = useRoute()
const tooltip = ref(null)
const noData = ref(false)

// Animation variables
let vectorAnimId = null
let vectors = []
const mouse = ref({ x: 0, y: 0 })

// Direct DOM manipulation floating animation
function startFloatingAnimation() {
  if (!cy) return
  
  let animationId = null
  const nodeData = new Map()

  // Wait for layout to complete
  cy.once('layoutstop', () => {
    console.log('Starting DOM-based floating animation...')
    
    // Initialize floating data for each node
    cy.nodes().forEach((node, index) => {
      nodeData.set(node.id(), {
        node: node,
        time: Math.random() * Math.PI * 2, // Random start phase
        speed: 0.008 + Math.random() * 0.004, // Vary speed slightly
        amplitudeX: 0.8 + Math.random() * 0.4, // 0.8-1.2px
        amplitudeY: 0.6 + Math.random() * 0.3, // 0.6-0.9px
        baseDelay: index * 0.1
      })
    })

    // Start animation loop
    function animateNodes() {
      nodeData.forEach((data, nodeId) => {
        const { node, time, speed, amplitudeX, amplitudeY } = data
        
        // Skip if node is being interacted with
        if (node.hasClass('clicked') || node.hasClass('user-dragging') || node.hasClass('preview-expanded')) {
          return
        }

        // Calculate floating offsets using sine waves
        const offsetX = Math.sin(data.time) * amplitudeX
        const offsetY = Math.cos(data.time * 0.7) * amplitudeY

        // Get the node's DOM element and apply transform
        const nodeElement = node.renderedMidpoint()
        if (nodeElement) {
          const domNode = cy.container().querySelector(`[data-id="${nodeId}"]`)
          if (domNode) {
            domNode.style.transform = `translate(${offsetX}px, ${offsetY}px)`
          }
        }

        // Update time for next frame
        data.time += speed
      })

      animationId = requestAnimationFrame(animateNodes)
    }

    // Start the animation
    animateNodes()
    
    // Store animation ID for cleanup
    window.floatingAnimationId = animationId
  })
}async function fetchGraph() {
  try {
    console.log('Fetching graph data...')
    const res = await fetch('http://127.0.0.1:8000/api/graph/')
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}: ${res.statusText}`)
    }
    const data = await res.json()
    console.log('Graph data received:', data)
    return data
  } catch (error) {
    console.error('Error fetching graph:', error)
    // Return empty data if API fails
    return { nodes: [], edges: [] }
  }
}

function makeElements(data) {
  const elements = []
  
  // Add nodes
  if (data.nodes && Array.isArray(data.nodes)) {
    data.nodes.forEach(n => {
      elements.push({ 
        data: { 
          id: String(n.id), 
          label: n.label || 'Untitled' 
        } 
      })
    })
  }
  
  // Add edges  
  if (data.edges && Array.isArray(data.edges)) {
    data.edges.forEach(e => {
      elements.push({ 
        data: { 
          source: String(e.source), 
          target: String(e.target) 
        } 
      })
    })
  }
  
  console.log('Generated elements:', elements)
  return elements
}

// Breathing effect for random nodes
function startBreathingEffect() {
  if (!cy) return
  
  function breatheRandomNode() {
    const nodes = cy.nodes()
    if (nodes.length === 0) return
    
    const randomNode = nodes[Math.floor(Math.random() * nodes.length)]
    
    if (!randomNode.hasClass('hovered') && !randomNode.hasClass('clicked')) {
      randomNode.addClass('breathing')
      
      // Breathing animation sequence
      randomNode.animate({
        style: {
          'width': '80px',
          'height': '80px'
        }
      }, {
        duration: 1500,
        easing: 'ease-in-out-sine'
      }).animate({
        style: {
          'width': '70px',
          'height': '70px'
        }
      }, {
        duration: 1500,
        easing: 'ease-in-out-sine',
        complete: () => {
          randomNode.removeClass('breathing')
        }
      })
    }
  }
  
  // Start breathing effects every 4-8 seconds
  setInterval(breatheRandomNode, 4000 + Math.random() * 4000)
}

// Random sparkle effects
function startRandomSparkles() {
  if (!cy) return
  
  function sparkleRandomNode() {
    const nodes = cy.nodes()
    if (nodes.length === 0) return
    
    const randomNode = nodes[Math.floor(Math.random() * nodes.length)]
    
    if (!randomNode.hasClass('hovered') && !randomNode.hasClass('preview-expanded')) {
      randomNode.addClass('sparkle')
      
      setTimeout(() => {
        randomNode.removeClass('sparkle')
      }, 2000)
    }
  }
  
  // Sparkle every 6-12 seconds
  setInterval(sparkleRandomNode, 6000 + Math.random() * 6000)
}

// Edge pulse effects
function startEdgePulses() {
  if (!cy) return
  
  function pulseRandomEdge() {
    const edges = cy.edges()
    if (edges.length === 0) return
    
    const randomEdge = edges[Math.floor(Math.random() * edges.length)]
    
    if (!randomEdge.hasClass('highlighted')) {
      randomEdge.addClass('pulse')
      
      // Animate the dash offset for flowing effect
      let offset = 0
      const pulseInterval = setInterval(() => {
        offset += 2
        randomEdge.style('line-dash-offset', offset)
      }, 100)
      
      setTimeout(() => {
        clearInterval(pulseInterval)
        randomEdge.removeClass('pulse')
        randomEdge.style('line-dash-offset', 0)
      }, 3000)
    }
  }
  
  // Pulse every 5-10 seconds
  setInterval(pulseRandomEdge, 5000 + Math.random() * 5000)
}

// Vector background animation
// Use the landing page vector background logic but sized to the graph container
let vectorResize = null
function startVectorAnimation() {
  const canvas = vectorCanvas.value
  const container = cyRef.value || document.querySelector('.cy-wrap')
  if (!canvas || !container) return

  const ctx = canvas.getContext('2d')

  function resize() {
    const rect = container.getBoundingClientRect()
    canvas.style.width = rect.width + 'px'
    canvas.style.height = rect.height + 'px'
    canvas.width = Math.max(1, Math.floor(rect.width))
    canvas.height = Math.max(1, Math.floor(rect.height))
    initializeVectors()
  }
  vectorResize = resize
  resize()
  window.addEventListener('resize', resize)

  function initializeVectors() {
    vectors = []
    for (let i = 0; i < 60; i++) {
      const vectorType = Math.random()
      let value, isArray = false

      if (vectorType < 0.4) {
        const arrayLength = Math.floor(Math.random() * 6) + 3
        const embedding = []
        for (let j = 0; j < arrayLength; j++) {
          embedding.push((Math.random() * 2 - 1).toFixed(3))
        }
        value = `[${embedding.join(', ')}]`
        isArray = true
      } else if (vectorType < 0.7) {
        value = (Math.random() * 2 - 1).toFixed(3)
        isArray = false
      } else {
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
        alpha: 0.5 + Math.random() * 0.4 // Increased opacity: 0.5-0.9 range
      })
    }
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    // Subtle background grid
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
      // Magnetism to mouse
      const dx = vector.x - mouse.value.x
      const dy = vector.y - mouse.value.y
      const distance = Math.sqrt(dx * dx + dy * dy)
      const maxDistance = 150
      const magnetism = Math.max(0, 1 - distance / maxDistance)
      const pullStrength = magnetism * 0.02

      if (distance < maxDistance) {
        vector.x -= dx * pullStrength
        vector.y -= dy * pullStrength
      }

      // Normal movement
      vector.x += vector.vx
      vector.y += vector.vy

      // Boundary wrapping
      const margin = vector.isArray ? 100 : 50
      if (vector.x < -margin) vector.x = canvas.width + margin
      if (vector.x > canvas.width + margin) vector.x = -margin
      if (vector.y < -margin) vector.y = canvas.height + margin
      if (vector.y > canvas.height + margin) vector.y = -margin

      // Draw vector
      ctx.save()
      const alpha = 0.6 + magnetism * 0.4 // Increased base alpha from 0.3 to 0.6
      ctx.fillStyle = `rgba(96, 165, 250, ${alpha * (vector.alpha || 1)})`
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'

      if (vector.isArray) {
        ctx.font = `${Math.max(16, vector.size * 0.6)}px "SF Mono", Consolas, monospace`
        ctx.fillStyle = `rgba(125, 211, 252, ${alpha})`
      } else if (typeof vector.value === 'string' && isNaN(parseFloat(vector.value))) {
        ctx.font = `${Math.max(20, vector.size * 0.8)}px "SF Mono", Consolas, monospace`
        ctx.fillStyle = `rgba(244, 114, 182, ${alpha})`
      } else {
        ctx.font = `${Math.max(20, vector.size * 0.7)}px "SF Mono", Consolas, monospace`
        ctx.fillStyle = `rgba(96, 165, 250, ${alpha})`
      }

      ctx.fillText(vector.value, vector.x, vector.y)
      ctx.restore()
    })

    vectorAnimId = requestAnimationFrame(draw)
  }
  draw()
}

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

onMounted(async () => {
  try {
    console.log('GraphView mounting...')
    const data = await fetchGraph()
    const elements = makeElements(data)
    console.log('Creating cytoscape with elements:', elements)
    
    // Check if we have any data
    if (elements.length === 0) {
      noData.value = true
      return
    } else {
      noData.value = false
    }
    
    if (!cyRef.value) {
      console.error('cyRef.value is null')
      return
    }
    
    cy = cytoscape({
      container: cyRef.value,
      elements: elements,
      style: [
        { 
          selector: 'node', 
          style: { 
            'label': 'data(label)', 
            'background-color': '#4f46e5', 
            'color': '#fff', 
            'text-valign': 'center', 
            'text-halign': 'center', 
            'width': '70px',
            'height': '70px',
            'padding': '6px',
            'text-wrap': 'wrap',
            'text-max-width': '60px',
            'font-size': '10px',
            'font-weight': '600',
            'line-height': 1.2,
            'border-width': '2px',
            'border-color': '#60a5fa',
            'border-opacity': 0.8,
            'transition-property': 'width, height, background-color, border-width, font-size',
            'transition-duration': '0.3s',
            'transition-timing-function': 'ease-out',
            'shadow-blur': '10px',
            'shadow-color': '#4f46e5',
            'shadow-opacity': 0.3,
            'text-outline-color': '#000',
            'text-outline-width': 0.5,
            'text-justification': 'center'
          } 
        },
        {
          selector: 'node:hover',
          style: {
            'width': '85px',
            'height': '85px', 
            'background-color': '#7c3aed',
            'border-width': '3px',
            'border-color': '#a855f7',
            'shadow-blur': '20px',
            'shadow-opacity': 0.6,
            'font-size': '11px',
            'text-max-width': '75px',
            'padding': '7px',
            'z-index': 10
          }
        },
        {
          selector: 'node.hovered',
          style: {
            'width': '90px',
            'height': '90px',
            'background-color': '#7c3aed',
            'border-width': '3px',
            'border-color': '#a855f7',
            'shadow-blur': '25px',
            'shadow-opacity': 0.7,
            'font-size': '11px',
            'text-max-width': '80px',
            'padding': '8px',
            'z-index': 15
          }
        },
        {
          selector: 'node.preview-expanded',
          style: {
            'width': '140px',
            'height': '140px',
            'background-color': '#6366f1',
            'border-width': '4px',
            'border-color': '#818cf8',
            'shadow-blur': '35px',
            'shadow-opacity': 0.9,
            'font-size': '9px',
            'text-max-width': '125px',
            'padding': '12px',
            'z-index': 20,
            'content': 'data(content)',
            'line-height': 1.1
          }
        },
        {
          selector: 'node.clicked',
          style: {
            'width': '90px',
            'height': '90px',
            'background-color': '#059669',
            'border-color': '#10b981',
            'border-width': '4px',
            'shadow-blur': '25px',
            'shadow-color': '#10b981',
            'shadow-opacity': 0.8
          }
        },
        {
          selector: 'node.floating',
          style: {
            'background-color': '#8b5cf6',
            'border-color': '#a78bfa'
          }
        },
        { 
          selector: 'edge', 
          style: { 
            'width': 2, 
            'line-color': '#9ca3af', 
            'curve-style': 'bezier',
            'target-arrow-shape': 'triangle',
            'target-arrow-color': '#9ca3af',
            'opacity': 0.6,
            'transition-property': 'line-color, width, opacity',
            'transition-duration': '0.3s'
          } 
        },
        {
          selector: 'edge.highlighted',
          style: {
            'line-color': '#60a5fa',
            'target-arrow-color': '#60a5fa',
            'width': 4,
            'opacity': 1,
            'z-index': 5
          }
        },
        {
          selector: 'edge.pulse',
          style: {
            'line-color': '#f59e0b',
            'target-arrow-color': '#f59e0b',
            'width': 5,
            'opacity': 0.9,
            'line-style': 'dashed',
            'line-dash-pattern': [10, 5],
            'line-dash-offset': 24
          }
        },
        {
          selector: 'node.breathing',
          style: {
            'background-color': '#10b981',
            'shadow-color': '#10b981',
            'shadow-blur': '40px',
            'shadow-opacity': 0.6
          }
        },
        {
          selector: 'node.sparkle',
          style: {
            'border-color': '#fbbf24',
            'border-width': '5px',
            'shadow-color': '#fbbf24',
            'shadow-blur': '30px',
            'shadow-opacity': 1
          }
        }
      ],
      layout: { 
        name: 'cose', 
        animate: true,
        animationDuration: 2000,
        nodeOverlap: 20,
        idealEdgeLength: 120,
        padding: 30,
        componentSpacing: 100,
        nodeRepulsion: function(node) { return 400000; },
        edgeElasticity: function(edge) { return 100; },
        nestingFactor: 5,
        gravity: 80,
        numIter: 1000,
        initialTemp: 200,
        coolingFactor: 0.95,
        minTemp: 1.0
      }
    })

    console.log('Cytoscape created successfully')

    // Add floating animation to all nodes
    startFloatingAnimation()
    
    // Start background vector animation
    setupMouseTracking()
    startVectorAnimation()
    
    // Add cool visual effects
    startBreathingEffect()
    startRandomSparkles()
    startEdgePulses()

    cy.on('tap', 'node', (evt) => {
      const node = evt.target
      const id = node.id()
      console.log('Node clicked:', id)
      
      // Remove previous effects
      cy.nodes().removeClass('clicked sparkle breathing')
      cy.edges().removeClass('highlighted pulse')
      
      // Add dramatic click animation
      node.addClass('clicked')
      
      // Create ripple effect on connected nodes
      const connectedNodes = node.connectedEdges().connectedNodes().difference(node)
      connectedNodes.addClass('sparkle')
      setTimeout(() => connectedNodes.removeClass('sparkle'), 1500)
      
      // Pulse animation sequence
      node.animate({
        style: {
          'width': '110px',
          'height': '110px',
          'shadow-blur': '50px'
        },
        duration: 150
      }).animate({
        style: {
          'width': '95px',
          'height': '95px',
          'shadow-blur': '35px'
        },
        duration: 200
      }).animate({
        style: {
          'width': '100px',
          'height': '100px',
          'shadow-blur': '40px'
        },
        duration: 150
      })
      
      // Highlight connected edges with pulse effect
      const connectedEdges = node.connectedEdges()
      connectedEdges.addClass('highlighted pulse')
      
      // Create edge animation wave
      connectedEdges.forEach((edge, index) => {
        setTimeout(() => {
          edge.animate({
            style: { 'width': 6 }
          }, {
            duration: 200
          }).animate({
            style: { 'width': 4 }
          }, {
            duration: 200
          })
        }, index * 100)
      })
      
      // Navigate after dramatic effect
      setTimeout(() => {
        router.push({ name: 'pages.view', params: { id } })
      }, 600)
    })

    // Enhanced hover effects with node enlargement and delayed preview
    let hoverTimer = null
    let previewNode = null
    
    cy.on('mouseover', 'node', (evt) => {
      const node = evt.target
      
      // Clear any existing timer
      if (hoverTimer) {
        clearTimeout(hoverTimer)
      }
      
      // Immediate effects
      node.addClass('hovered')
      const connectedEdges = node.connectedEdges()
      connectedEdges.addClass('highlighted')
      
      // Delayed preview effect (after 800ms hover)
      hoverTimer = setTimeout(() => {
        if (previewNode && previewNode !== node) {
          previewNode.removeClass('preview-expanded')
        }
        
        node.addClass('preview-expanded')
        previewNode = node
        
        // Fetch and show content in the node itself
        fetch(`http://127.0.0.1:8000/api/pages/${node.id()}/`).then(r => r.json()).then(d => {
          const preview = (d.content || '').slice(0, 100) + '...'
          node.data('preview', preview)
          node.style('content', node.data('label') + '\n\n' + preview)
        }).catch(err => console.error('Preview fetch error:', err))
      }, 800)
    })
    
    cy.on('mouseout', 'node', (evt) => { 
      const node = evt.target
      
      // Clear timer if still pending
      if (hoverTimer) {
        clearTimeout(hoverTimer)
        hoverTimer = null
      }
      
      // Remove effects
      node.removeClass('hovered preview-expanded')
      cy.edges().removeClass('highlighted')
      
      // Reset node content to just label
      node.style('content', node.data('label'))
      
      if (previewNode === node) {
        previewNode = null
      }
    })

    // If route has focus id, focus on it
    if (route.query.focus) {
      const el = cy.$id(String(route.query.focus))
      if (el.length > 0) {
        cy.animate({ fit: { eles: el, padding: 40 }, duration: 500 })
        el.flashClass = true
      }
    }

    // restore positions if present
    const saved = localStorage.getItem('pageGraphPositions')
    if (saved) {
      try {
        const pos = JSON.parse(saved)
        Object.keys(pos).forEach(id => {
          const n = cy.$id(id)
          if (n.length > 0) n.position(pos[id])
        })
        cy.fit()
      } catch (e) {
        console.error('Error restoring positions:', e)
      }
    }

    // save positions after layout stop
    cy.on('layoutstop', () => {
      const positions = {}
      cy.nodes().forEach(n => { positions[n.id()] = n.position() })
      localStorage.setItem('pageGraphPositions', JSON.stringify(positions))
    })
    
  } catch (error) {
    console.error('Error in GraphView onMounted:', error)
  }
})

function fit() {
  if (cy) cy.fit()
}

function layout() {
  if (cy) cy.layout({ name: 'cose', animate: true }).run()
}

async function reload() {
  console.log('Reloading graph...')
  try {
    const data = await fetchGraph()
    const elements = makeElements(data)
    
    if (elements.length === 0) {
      noData.value = true
      if (cy) cy.destroy()
      return
    } else {
      noData.value = false
    }
    
    if (cy) {
      cy.elements().remove()
      cy.add(elements)
      cy.layout({ name: 'cose', animate: true }).run()
    } else {
      // Recreate if needed
      location.reload()
    }
  } catch (error) {
    console.error('Error reloading graph:', error)
  }
}

onUnmounted(() => {
  if (vectorAnimId) {
    cancelAnimationFrame(vectorAnimId)
  }
  if (window.floatingAnimationId) {
    cancelAnimationFrame(window.floatingAnimationId)
  }
  window.removeEventListener('mousemove', handleMouseMove)
  if (vectorResize) window.removeEventListener('resize', vectorResize)
})
</script>

<style>
.graph-wrap { 
  height: calc(100vh - 70px); 
  display: flex; 
  flex-direction: column; 
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

.vector-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  pointer-events: none;
}

.cy-wrap {
  position: relative;
  flex: 1;
  margin: 8px;
  border-radius: 12px;
  overflow: hidden;
  z-index: 1;
  display: flex;
}

.cy-wrap .cy {
  position: relative;
  z-index: 2;
  flex: 1;
  margin: 0;
  border-radius: 12px;
  /* make slightly transparent so vector canvas underneath shows through */
  background: linear-gradient(180deg, rgba(15,23,42,0.85), rgba(2,6,23,0.85)); 
  border: 1px solid rgba(96, 165, 250, 0.2);
}

.controls { 
  padding: 16px; 
  display: flex;
  gap: 12px;
  background: rgba(15, 23, 42, 0.8);
  border-bottom: 1px solid rgba(96, 165, 250, 0.2);
  position: relative;
  z-index: 3;
}

button { 
  background: rgba(96, 165, 250, 0.2);
  border: 1px solid rgba(96, 165, 250, 0.3);
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

button:hover {
  background: rgba(96, 165, 250, 0.3);
  border-color: rgba(96, 165, 250, 0.5);
}

.cy-tooltip {
  background: rgba(15, 23, 42, 0.95) !important;
  color: white !important;
  border: 1px solid rgba(96, 165, 250, 0.3) !important;
  border-radius: 8px !important;
  backdrop-filter: blur(10px) !important;
}

.no-data {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: rgba(255, 255, 255, 0.7);
  padding: 40px;
}

.no-data h3 {
  color: white;
  margin-bottom: 16px;
  font-size: 24px;
}

.no-data p {
  margin-bottom: 8px;
  max-width: 500px;
}

/* CSS Keyframe animations for floating nodes */
@keyframes nodeFloat {
  0% { 
    transform: translate(0px, 0px) rotate(0deg); 
  }
  33% { 
    transform: translate(1.5px, -1px) rotate(0.3deg); 
  }
  66% { 
    transform: translate(-1px, 1.5px) rotate(-0.3deg); 
  }
  100% { 
    transform: translate(0px, 0px) rotate(0deg); 
  }
}

@keyframes nodeFloatAlt {
  0% { 
    transform: translate(0px, 0px) rotate(0deg); 
  }
  25% { 
    transform: translate(-1px, 1px) rotate(0.2deg); 
  }
  50% { 
    transform: translate(1.5px, 0.5px) rotate(-0.2deg); 
  }
  75% { 
    transform: translate(0.5px, -1.5px) rotate(0.4deg); 
  }
  100% { 
    transform: translate(0px, 0px) rotate(0deg); 
  }
}

/* Apply floating animation to Cytoscape nodes */
.cy :global(.css-floating) {
  animation: nodeFloat 4s ease-in-out infinite alternate;
}
</style>