<template>
  <div>
    <div class="graph-wrap" ref="graphWrap">
      <div class="controls">
        <select v-model="selectedPageId" @change="loadData" class="page-selector">
          <option value="">All Pages</option>
          <option v-for="page in allPages" :key="page.id" :value="page.id">
            {{ page.title }}
          </option>
        </select>
        <button @click="fit">Zoom Out (Fit)</button>
        <button @click="layout">Relayout</button>
        <button @click="reload">Reload Graph</button>
      </div>
      
      <div v-if="noData" class="no-data">
        <h3>No Graph Data Available</h3>
        <p>Try running the population script or creating some pages with links.</p>
      </div>
      
      <div v-else class="cy-wrap">
        <canvas ref="vectorCanvas" class="vector-canvas"></canvas>
        <div ref="cyRef" class="cy"></div>
      </div>
      
      <!-- Hover Panel for Version History -->
      <div 
        v-if="hoveredPage" 
        class="version-panel"
        :style="panelStyle"
      >
        <div class="panel-header">
          <h3>{{ hoveredPage.title }}</h3>
          <span class="version-count">{{ pageVersions.length }} versions</span>
        </div>
        
        <!-- Version List -->
        <div class="version-list">
          <div 
            v-for="version in pageVersions.slice(0, 5)" 
            :key="version.id"
            class="version-item"
          >
            <div class="version-info">
              <span class="version-num">v{{ version.version_number }}</span>
              <span class="version-time">{{ formatTime(version.timestamp) }}</span>
            </div>
            <div class="version-summary">{{ version.summary }}</div>
            <div class="change-badge" :class="version.change_magnitude">
              {{ version.change_magnitude }}
            </div>
          </div>
          
          <div v-if="pageVersions.length > 5" class="more-versions">
            +{{ pageVersions.length - 5 }} more versions
          </div>
        </div>
      </div>
      
      <!-- Version History Detail Modal -->
      <div v-if="showDetailModal" class="modal-overlay" @click="closeDetailModal">
        <div class="version-detail-modal" @click.stop>
          <div class="modal-header">
            <h2>{{ selectedPage?.title }} - Version History</h2>
            <button @click="closeDetailModal" class="close-btn">×</button>
          </div>
          
          <div class="modal-content">
            <div class="version-timeline">
              <div 
                v-for="version in pageVersions" 
                :key="version.id"
                class="timeline-item"
              >
                <div class="timeline-marker" :class="version.change_magnitude"></div>
                <div class="timeline-content">
                  <div class="timeline-header">
                    <span class="version-number">Version {{ version.version_number }}</span>
                    <span class="version-date">{{ formatTimestamp(version.timestamp) }}</span>
                  </div>
                  <div class="timeline-summary">{{ version.summary }}</div>
                  <div class="timeline-badges">
                    <span class="change-badge" :class="version.change_magnitude">
                      {{ version.change_magnitude }} change
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import cytoscape from 'cytoscape';

export default {
  name: 'VersionHistory',
  components: {
  },
  data() {
    return {
      cy: null,
      allPages: [],
      selectedPageId: '',
      hoveredPage: null,
      pageVersions: [],
      mouseX: 0,
      mouseY: 0,
      noData: false,
      showDetailModal: false,
      selectedPage: null,
      // Vector animation variables
      vectorAnimId: null,
      vectors: [],
      mouse: { x: 0, y: 0 }
    };
  },
  computed: {
    panelStyle() {
      if (!this.hoveredPage) return {};
      
      return {
        left: `${this.mouseX + 20}px`,
        top: `${this.mouseY - 50}px`
      };
    }
  },
  async mounted() {
    await this.loadData();
    this.initGraph();
    this.initVectorAnimation();
  },
  beforeUnmount() {
    this.cleanup();
  },
  methods: {
    cleanup() {
      if (this.cy) {
        this.cy.destroy();
      }
      if (this.vectorAnimId) {
        cancelAnimationFrame(this.vectorAnimId);
      }
    },
    
    async loadData() {
      try {
        // Load all pages (same as graph page)
        const response = await fetch('http://localhost:8000/api/pages/');
        this.allPages = await response.json();
        
        this.noData = this.allPages.length === 0;
        
        if (this.cy && !this.noData) {
          this.updateGraph();
        }
      } catch (error) {
        console.error('Error loading data:', error);
        // If backend is not available, create demo data for testing
        this.createDemoData();
      }
    },
    
    createDemoData() {
      // Create demo pages for testing when backend isn't running
      this.allPages = [
        {
          id: 1,
          title: "Machine Learning Basics",
          content: "Introduction to ML concepts",
          links: [{ id: 2, title: "Neural Networks" }, { id: 3, title: "Deep Learning" }]
        },
        {
          id: 2,
          title: "Neural Networks",
          content: "Understanding neural networks",
          links: [{ id: 3, title: "Deep Learning" }, { id: 4, title: "CNNs" }]
        },
        {
          id: 3,
          title: "Deep Learning",
          content: "Advanced deep learning techniques",
          links: [{ id: 4, title: "CNNs" }, { id: 5, title: "RNNs" }]
        },
        {
          id: 4,
          title: "CNNs",
          content: "Convolutional Neural Networks",
          links: [{ id: 5, title: "RNNs" }]
        },
        {
          id: 5,
          title: "RNNs",
          content: "Recurrent Neural Networks",
          links: []
        }
      ];
      
      this.noData = false;
      
      if (this.cy) {
        this.updateGraph();
      }
    },
    
    async loadPageHistory(pageId) {
      try {
        // Try to load version history, but don't fail if it doesn't exist
        const response = await fetch(`http://localhost:8000/api/pages/${pageId}/history/`);
        if (response.ok) {
          const data = await response.json();
          this.pageVersions = data.history || [];
        } else {
          // Create mock version history for demo
          this.pageVersions = this.createMockVersions(pageId);
        }
      } catch (error) {
        // Create mock version history for demo
        this.pageVersions = this.createMockVersions(pageId);
      }
    },
    
    createMockVersions(pageId) {
      const page = this.allPages.find(p => p.id == pageId);
      if (!page) return [];
      
      const versions = [];
      const versionCount = Math.floor(Math.random() * 5) + 2; // 2-6 versions
      
      for (let i = versionCount; i >= 1; i--) {
        const daysAgo = Math.floor(Math.random() * 30) + 1;
        const date = new Date();
        date.setDate(date.getDate() - daysAgo);
        
        versions.push({
          id: `${pageId}_v${i}`,
          version_number: i,
          timestamp: date.toISOString(),
          summary: i === versionCount ? 'Initial version' : 
                  i === 1 ? 'Latest updates' : 
                  `Update ${versionCount - i + 1}`,
          change_magnitude: ['minor', 'medium', 'major'][Math.floor(Math.random() * 3)]
        });
      }
      
      return versions;
    },
    
    initGraph() {
      if (!this.$refs.cyRef || this.noData) return;
      
      this.cy = cytoscape({
        container: this.$refs.cyRef,
        elements: [],
        style: [
          {
            selector: 'node',
            style: {
              'background-color': '#4CAF50',
              'color': '#ffffff',
              'label': 'data(label)',
              'text-valign': 'center',
              'text-halign': 'center',
              'font-size': '12px',
              'width': '60px',
              'height': '60px',
              'border-width': '2px',
              'border-color': '#2E7D32',
              'text-wrap': 'wrap',
              'text-max-width': '50px'
            }
          },
          {
            selector: 'edge',
            style: {
              'width': 2,
              'line-color': '#9E9E9E',
              'target-arrow-color': '#9E9E9E',
              'target-arrow-shape': 'triangle',
              'curve-style': 'bezier'
            }
          },
          {
            selector: 'node:hover',
            style: {
              'background-color': '#2196F3',
              'border-color': '#1976D2',
              'border-width': '3px'
            }
          }
        ],
        layout: {
          name: 'cose',
          animate: false,
          animationDuration: 0,
          nodeRepulsion: 4000,
          nodeOverlap: 20,
          idealEdgeLength: 100
        }
      });
      
      // Add event listeners
      this.cy.on('mouseover', 'node', async (evt) => {
        const node = evt.target;
        const pageId = node.data('id');
        
        this.hoveredPage = this.allPages.find(p => p.id == pageId);
        if (this.hoveredPage) {
          await this.loadPageHistory(pageId);
        }
      });
      
      this.cy.on('mouseout', 'node', () => {
        setTimeout(() => {
          this.hoveredPage = null;
          this.pageVersions = [];
        }, 300);
      });
      
      // Add click event for version history details
      this.cy.on('tap', 'node', async (evt) => {
        const node = evt.target;
        const pageId = node.data('id');
        
        this.selectedPage = this.allPages.find(p => p.id == pageId);
        if (this.selectedPage) {
          await this.loadPageHistory(pageId);
          this.showDetailModal = true;
        }
      });
      
      // Track mouse position
      this.$refs.graphWrap.addEventListener('mousemove', (e) => {
        const rect = this.$refs.graphWrap.getBoundingClientRect();
        this.mouseX = e.clientX - rect.left;
        this.mouseY = e.clientY - rect.top;
        this.mouse.x = this.mouseX;
        this.mouse.y = this.mouseY;
      });
      
      this.updateGraph();
    },
    
    updateGraph() {
      if (!this.cy || !this.allPages.length) return;
      
      this.cy.elements().remove();
      
      // Filter pages if needed
      let pages = this.allPages;
      if (this.selectedPageId) {
        pages = pages.filter(p => p.id == this.selectedPageId);
      }
      
      // Create nodes
      const nodes = pages.map(page => ({
        data: {
          id: page.id,
          label: page.title
        }
      }));
      
      // Create edges (same as graph page)
      const edges = [];
      pages.forEach(page => {
        if (page.links) {
          page.links.forEach(link => {
            edges.push({
              data: {
                source: page.id,
                target: link.id
              }
            });
          });
        }
      });
      
      this.cy.add([...nodes, ...edges]);
      this.cy.layout({ name: 'cose', animate: false }).run();
    },
    
    // Control methods (same as GraphView)
    fit() {
      if (this.cy) this.cy.fit();
    },
    
    layout() {
      if (this.cy) this.cy.layout({ name: 'cose', animate: false }).run();
    },
    
    reload() {
      this.loadData();
    },
    
    closeDetailModal() {
      this.showDetailModal = false;
      this.selectedPage = null;
    },
    
    // Vector animation (copied from GraphView)
    initVectorAnimation() {
      const canvas = this.$refs.vectorCanvas;
      if (!canvas) return;
      
      const ctx = canvas.getContext('2d');
      
      const resizeCanvas = () => {
        canvas.width = this.$refs.graphWrap.clientWidth;
        canvas.height = this.$refs.graphWrap.clientHeight;
      };
      
      resizeCanvas();
      window.addEventListener('resize', resizeCanvas);
      
      // Initialize vectors
      this.vectors = [];
      for (let i = 0; i < 50; i++) {
        this.vectors.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          vx: (Math.random() - 0.5) * 0.5,
          vy: (Math.random() - 0.5) * 0.5,
          size: Math.random() * 2 + 1,
          opacity: Math.random() * 0.3 + 0.1
        });
      }
      
      // Animation loop
      const animate = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        this.vectors.forEach(vector => {
          // Update position
          vector.x += vector.vx;
          vector.y += vector.vy;
          
          // Bounce off edges
          if (vector.x < 0 || vector.x > canvas.width) vector.vx *= -1;
          if (vector.y < 0 || vector.y > canvas.height) vector.vy *= -1;
          
          // Mouse interaction
          const dx = this.mouse.x - vector.x;
          const dy = this.mouse.y - vector.y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          
          if (distance < 100) {
            const force = (100 - distance) / 100;
            vector.x -= dx * force * 0.01;
            vector.y -= dy * force * 0.01;
          }
          
          // Draw vector
          ctx.globalAlpha = vector.opacity;
          ctx.fillStyle = '#60a5fa';
          ctx.beginPath();
          ctx.arc(vector.x, vector.y, vector.size, 0, Math.PI * 2);
          ctx.fill();
        });
        
        this.vectorAnimId = requestAnimationFrame(animate);
      };
      
      animate();
    },
    
    formatTime(timestamp) {
      const date = new Date(timestamp);
      const now = new Date();
      const diffMs = now - date;
      const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
      
      if (diffDays === 0) return 'Today';
      if (diffDays === 1) return 'Yesterday';
      if (diffDays < 7) return `${diffDays}d ago`;
      if (diffDays < 30) return `${Math.floor(diffDays / 7)}w ago`;
      return `${Math.floor(diffDays / 30)}m ago`;
    },
    
    formatTimestamp(timestamp) {
      return new Date(timestamp).toLocaleString();
    }
  }
};
</script>

<style>
/* Same styling as GraphView.vue */
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
  align-items: center;
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

.page-selector {
  background: rgba(96, 165, 250, 0.2);
  border: 1px solid rgba(96, 165, 250, 0.3);
  color: white;
  padding: 8px 12px;
  border-radius: 8px;
  min-width: 150px;
}

.page-selector option {
  background: #1e293b;
  color: white;
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

/* Version panel styling */
.version-panel {
  position: absolute;
  background: rgba(15, 23, 42, 0.95);
  border-radius: 12px;
  padding: 15px;
  min-width: 280px;
  max-width: 350px;
  z-index: 1000;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(96, 165, 250, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  animation: slideIn 0.2s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(96, 165, 250, 0.2);
}

.panel-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #60a5fa;
}

.version-count {
  background: rgba(96, 165, 250, 0.3);
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
}

.version-list {
  max-height: 250px;
  overflow-y: auto;
}

.version-item {
  background: rgba(96, 165, 250, 0.1);
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 8px;
  transition: all 0.2s ease;
}

.version-item:hover {
  background: rgba(96, 165, 250, 0.2);
}

.version-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.version-num {
  font-weight: bold;
  color: #60a5fa;
}

.version-time {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
}

.version-summary {
  font-size: 0.9rem;
  margin-bottom: 8px;
  color: rgba(255, 255, 255, 0.8);
}

.change-badge {
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 0.7rem;
  font-weight: bold;
  display: inline-block;
}

.change-badge.minor { background: rgba(76, 175, 80, 0.3); color: #4CAF50; }
.change-badge.medium { background: rgba(33, 150, 243, 0.3); color: #2196F3; }
.change-badge.major { background: rgba(244, 67, 54, 0.3); color: #F44336; }

.more-versions {
  text-align: center;
  padding: 8px;
  color: rgba(255, 255, 255, 0.5);
  font-style: italic;
}

/* Modal styling */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.version-detail-modal {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  border-radius: 16px;
  border: 1px solid rgba(96, 165, 250, 0.3);
  max-width: 800px;
  max-height: 80vh;
  width: 90%;
  overflow: hidden;
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid rgba(96, 165, 250, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  margin: 0;
  color: #60a5fa;
  font-size: 1.5rem;
}

.close-btn {
  background: none !important;
  border: none !important;
  color: rgba(255, 255, 255, 0.6) !important;
  font-size: 24px;
  cursor: pointer;
  padding: 0 !important;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: white !important;
}

.modal-content {
  padding: 20px;
  max-height: 60vh;
  overflow-y: auto;
}

.version-timeline {
  position: relative;
}

.timeline-item {
  display: flex;
  margin-bottom: 20px;
  position: relative;
}

.timeline-item:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 10px;
  top: 24px;
  width: 2px;
  height: calc(100% + 20px);
  background: rgba(96, 165, 250, 0.3);
}

.timeline-marker {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  margin-right: 15px;
  margin-top: 2px;
  flex-shrink: 0;
  z-index: 1;
}

.timeline-marker.minor { background: #4CAF50; }
.timeline-marker.medium { background: #2196F3; }
.timeline-marker.major { background: #F44336; }

.timeline-content {
  flex: 1;
  background: rgba(96, 165, 250, 0.1);
  padding: 15px;
  border-radius: 8px;
  border: 1px solid rgba(96, 165, 250, 0.2);
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.version-number {
  font-weight: bold;
  color: #60a5fa;
  font-size: 1.1rem;
}

.version-date {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.6);
}

.timeline-summary {
  margin-bottom: 10px;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.4;
}

.timeline-badges {
  display: flex;
  gap: 8px;
}
</style>