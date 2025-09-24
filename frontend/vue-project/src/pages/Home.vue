<template>
  <div class="landing-page">
    <AnimatedLanding />
    
    <!-- Scroll indicator -->
    <div class="scroll-indicator" :class="{ visible: showBrand }">
      <div class="scroll-text">Scroll to explore</div>
      <div class="scroll-arrow">↓</div>
    </div>

    <!-- Main content sections -->
    <section class="content-section intro-section">
      <div class="container">
        <div class="intro-content">
          <h2 class="section-title">What is doc.doc?</h2>
          <p class="intro-description">
            Doc.doc is an intelligent document platform that transforms how you create, organize, 
            and interact with knowledge. Using advanced AI and graph technology, it creates 
            living documents that understand context, relationships, and meaning.
          </p>
          <div class="intro-visual">
            <div class="floating-docs">
              <div class="doc-node" style="animation-delay: 0.2s;">📄</div>
              <div class="doc-node" style="animation-delay: 0.4s;">📊</div>
              <div class="doc-node" style="animation-delay: 0.6s;">📝</div>
              <div class="connecting-lines"></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="content-section why-section">
      <div class="container">
        <div class="why-content">
          <h2 class="section-title">Why doc.doc?</h2>
          <p class="why-description">
            Traditional document systems are isolated islands of information. Doc.doc connects 
            your knowledge into an intelligent network where every piece of information enhances 
            every other piece, creating exponential value from your collective knowledge.
          </p>
          <div class="comparison-visual">
            <div class="traditional">
              <h4>Traditional Documents</h4>
              <div class="isolated-docs">
                <div class="isolated-doc">📄</div>
                <div class="isolated-doc">📄</div>
                <div class="isolated-doc">📄</div>
              </div>
            </div>
            <div class="vs-arrow">→</div>
            <div class="doc-doc-way">
              <h4>doc.doc Network</h4>
              <div class="networked-docs">
                <div class="network-node active">📄</div>
                <div class="network-node">📄</div>
                <div class="network-node">📄</div>
                <div class="network-connections"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="content-section features-section">
      <div class="container">
        <h2 class="section-title">Core Features</h2>
        <div class="features-grid">
          
          <div class="feature-capsule collaboration" data-aos="fade-up" data-aos-delay="100">
            <div class="capsule-header">
              <div class="feature-icon">👥</div>
              <h3>Collaboration</h3>
            </div>
            <p>Real-time collaborative editing with intelligent conflict resolution and seamless team workflows.</p>
            <div class="collaboration-effect">
              <div class="collaborator" style="animation-delay: 0s;">A</div>
              <div class="collaborator" style="animation-delay: 0.5s;">B</div>
              <div class="collaborator" style="animation-delay: 1s;">C</div>
              <div class="sync-waves"></div>
            </div>
          </div>

          <div class="feature-capsule gemini-writing" data-aos="fade-up" data-aos-delay="200">
            <div class="capsule-header">
              <div class="feature-icon">✨</div>
              <h3>Gemini Writing Assistant</h3>
            </div>
            <p>AI-powered writing companion that helps you craft, refine, and enhance your content in real-time.</p>
            <div class="writing-effect">
              <div class="writing-cursor"></div>
              <div class="ai-suggestions">
                <div class="suggestion">Enhance clarity</div>
                <div class="suggestion">Add context</div>
                <div class="suggestion">Improve flow</div>
              </div>
            </div>
          </div>

          <div class="feature-capsule ai-reading" data-aos="fade-up" data-aos-delay="300">
            <div class="capsule-header">
              <div class="feature-icon">🧠</div>
              <h3>AI Reading Assistant</h3>
            </div>
            <p>Intelligent document analysis that summarizes, extracts insights, and answers questions about your content.</p>
            <div class="reading-effect">
              <div class="document-scan">
                <div class="scan-line"></div>
                <div class="insights">
                  <div class="insight">Key insight 1</div>
                  <div class="insight">Summary point</div>
                  <div class="insight">Action item</div>
                </div>
              </div>
            </div>
          </div>

          <div class="feature-capsule vector-search" data-aos="fade-up" data-aos-delay="400">
            <div class="capsule-header">
              <div class="feature-icon">🔍</div>
              <h3>Vector Search</h3>
            </div>
            <p>Semantic search that understands meaning and context, finding relevant information even when exact words don't match.</p>
            <div class="search-effect">
              <div class="search-visualization">
                <div class="query-vector">[0.2, 0.8, -0.1]</div>
                <div class="result-vectors">
                  <div class="result-vector match-high">[0.3, 0.7, -0.2]</div>
                  <div class="result-vector match-medium">[0.1, 0.9, 0.1]</div>
                  <div class="result-vector match-low">[0.8, 0.1, 0.3]</div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>

    <section class="content-section tech-highlights">
      <div class="container">
        <h2 class="section-title">Technology Highlights</h2>
        
        <div class="tech-feature graph-structure">
          <div class="tech-content">
            <div class="tech-text">
              <h3>Graph Document Structure</h3>
              <p>
                Every document exists in a knowledge graph where relationships are first-class citizens. 
                Navigate through ideas, discover connections, and see how concepts relate across your 
                entire knowledge base.
              </p>
              <ul class="tech-benefits">
                <li>Visual relationship mapping</li>
                <li>Contextual navigation</li>
                <li>Knowledge discovery</li>
                <li>Semantic connections</li>
              </ul>
            </div>
            <div class="tech-visual">
              <div class="graph-container">
                <div class="graph-node central">📄</div>
                <div class="graph-node satellite" style="--angle: 0deg;">💡</div>
                <div class="graph-node satellite" style="--angle: 72deg;">📊</div>
                <div class="graph-node satellite" style="--angle: 144deg;">🔗</div>
                <div class="graph-node satellite" style="--angle: 216deg;">📝</div>
                <div class="graph-node satellite" style="--angle: 288deg;">🎯</div>
                <div class="graph-connections">
                  <div class="connection" style="--angle: 0deg;"></div>
                  <div class="connection" style="--angle: 72deg;"></div>
                  <div class="connection" style="--angle: 144deg;"></div>
                  <div class="connection" style="--angle: 216deg;"></div>
                  <div class="connection" style="--angle: 288deg;"></div>
                </div>
                <div class="pulse-effect"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="tech-feature version-history">
          <div class="tech-content reverse">
            <div class="tech-visual">
              <div class="timeline-container">
                <div class="timeline">
                  <div class="timeline-item active" style="animation-delay: 0s;">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">v3.2 - Latest</div>
                  </div>
                  <div class="timeline-item" style="animation-delay: 0.2s;">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">v3.1 - Major update</div>
                  </div>
                  <div class="timeline-item" style="animation-delay: 0.4s;">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">v3.0 - Rewrite</div>
                  </div>
                  <div class="timeline-item" style="animation-delay: 0.6s;">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">v2.8 - Features</div>
                  </div>
                </div>
                <div class="version-diff">
                  <div class="diff-line added">+ Enhanced AI integration</div>
                  <div class="diff-line removed">- Legacy API support</div>
                  <div class="diff-line modified">~ Updated UI components</div>
                </div>
              </div>
            </div>
            <div class="tech-text">
              <h3>Intelligent Version History</h3>
              <p>
                Beyond simple version control, our system understands semantic changes, tracks 
                concept evolution, and provides intelligent diffs that show not just what changed, 
                but what it means.
              </p>
              <ul class="tech-benefits">
                <li>Semantic change tracking</li>
                <li>Intelligent branching</li>
                <li>Concept evolution</li>
                <li>Smart merging</li>
              </ul>
            </div>
          </div>
        </div>
        
      </div>
    </section>

    <section class="content-section cta-section">
      <div class="container">
        <div class="cta-content">
          <h2 class="cta-title">Ready to Transform Your Documents?</h2>
          <p class="cta-description">
            Join the next generation of intelligent document management
          </p>
          <button class="dive-btn" @click="navigateToApp">
            <span class="btn-text">Dive In</span>
            <div class="btn-particles"></div>
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import AnimatedLanding from '../components/AnimatedLanding.vue'

const router = useRouter()
const showBrand = ref(false)

let landingHandler = null
onMounted(() => {
  // Initialize AOS immediately (fallback) and also listen for landing-ready
  // in case the landing animation completes after mount.
  initializeAOS()

  landingHandler = () => {
    showBrand.value = true
    // Re-run to ensure any elements that became visible are observed/animated
    initializeAOS()
  }

  window.addEventListener('landing-ready', landingHandler)
})

onUnmounted(() => {
  if (landingHandler) window.removeEventListener('landing-ready', landingHandler)
})

function initializeAOS() {
  // Simple intersection observer for scroll animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  }
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in')
      }
    })
  }, observerOptions)
  
  // Observe all feature capsules (correct selector)
  document.querySelectorAll('.feature-capsule').forEach(card => {
    observer.observe(card)
  })
}

function navigateToApp() {
  router.push({ name: 'login' })
}
</script>

<style scoped>
.landing-page {
  position: relative;
  min-height: 100vh;
}

.scroll-indicator {
  position: fixed;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 15;
  opacity: 0;
  transition: opacity 0.8s ease 1s;
  pointer-events: none;
}

.scroll-indicator.visible {
  opacity: 1;
  animation: bounce 2s infinite;
}

.scroll-text {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  text-align: center;
  margin-bottom: 8px;
  font-family: 'Courier New', monospace;
}

.scroll-arrow {
  color: #60a5fa;
  font-size: 24px;
  text-align: center;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateX(-50%) translateY(0); }
  40% { transform: translateX(-50%) translateY(-10px); }
  60% { transform: translateX(-50%) translateY(-5px); }
}

.content-section {
  position: relative;
  z-index: 10;
  background: transparent;
  padding: 120px 0;
}

.intro-section {
  margin-top: 100vh;
  background: linear-gradient(180deg, 
    rgba(3, 16, 38, 0.9) 0%, 
    rgba(2, 16, 38, 0.95) 100%);
  backdrop-filter: blur(10px);
}

.why-section {
  background: linear-gradient(180deg, 
    rgba(2, 16, 38, 0.95) 0%, 
    rgba(1, 16, 38, 0.97) 100%);
  backdrop-filter: blur(10px);
}

.features-section {
  background: linear-gradient(180deg, 
    rgba(1, 16, 38, 0.97) 0%, 
    rgba(1, 12, 28, 0.98) 100%);
  backdrop-filter: blur(10px);
}

.tech-highlights {
  background: linear-gradient(180deg, 
    rgba(1, 12, 28, 0.98) 0%, 
    rgba(0, 8, 20, 1) 100%);
  backdrop-filter: blur(10px);
  padding: 160px 0;
}

.cta-section {
  background: linear-gradient(180deg, 
    rgba(0, 8, 20, 1) 0%, 
    rgba(0, 6, 16, 1) 100%);
  backdrop-filter: blur(10px);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 40px;
}

.hero-content {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.intro-content, .why-content {
  text-align: center;
  max-width: 900px;
  margin: 0 auto;
}

.intro-description, .why-description {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  margin-bottom: 60px;
}

/* Intro Visual Effects */
.intro-visual {
  display: flex;
  justify-content: center;
  margin-top: 60px;
}

.floating-docs {
  position: relative;
  width: 200px;
  height: 120px;
}

.doc-node {
  position: absolute;
  font-size: 32px;
  animation: float 3s ease-in-out infinite;
}

.doc-node:nth-child(1) { top: 0; left: 50%; transform: translateX(-50%); }
.doc-node:nth-child(2) { top: 60px; left: 0; }
.doc-node:nth-child(3) { top: 60px; right: 0; }

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-10px) rotate(5deg); }
}

/* Comparison Visual */
.comparison-visual {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 60px;
  margin-top: 60px;
}

.traditional, .doc-doc-way {
  text-align: center;
}

.traditional h4, .doc-doc-way h4 {
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 20px;
}

.isolated-docs {
  display: flex;
  gap: 20px;
}

.isolated-doc {
  font-size: 24px;
  opacity: 0.5;
  animation: fadeInOut 2s ease-in-out infinite;
}

.isolated-doc:nth-child(2) { animation-delay: 0.5s; }
.isolated-doc:nth-child(3) { animation-delay: 1s; }

.networked-docs {
  position: relative;
  display: flex;
  gap: 20px;
}

.network-node {
  font-size: 24px;
  position: relative;
  z-index: 2;
}

.network-node.active {
  animation: pulse 2s ease-in-out infinite;
}

.network-connections {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #60a5fa, #7dd3fc, #60a5fa);
  animation: connectionFlow 2s ease-in-out infinite;
}

.vs-arrow {
  font-size: 32px;
  color: #60a5fa;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes fadeInOut {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.8; }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(96, 165, 250, 0.7); }
  50% { transform: scale(1.1); box-shadow: 0 0 20px 10px rgba(96, 165, 250, 0); }
}

@keyframes connectionFlow {
  0% { transform: translateX(-20px); opacity: 0; }
  50% { opacity: 1; }
  100% { transform: translateX(20px); opacity: 0; }
}

.section-title {
  font-size: 64px;
  font-weight: 900;
  color: white;
  margin-bottom: 30px;
  text-shadow: 0 0 30px #60a5fa;
  line-height: 1.2;
}

.hero-description {
  font-size: 24px;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  margin-bottom: 60px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 40px;
  margin-top: 80px;
}

.feature-capsule {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  border: 1px solid rgba(96, 165, 250, 0.2);
  padding: 32px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  opacity: 0;
  transform: translateY(30px);
  overflow: hidden;
  position: relative;
}

.feature-capsule.animate-in {
  opacity: 1;
  transform: translateY(0);
  transition: all 0.8s cubic-bezier(0.2, 0.9, 0.3, 1);
}

.feature-capsule:hover {
  transform: translateY(-8px);
  box-shadow: 0 16px 48px rgba(96, 165, 250, 0.2);
  border-color: rgba(96, 165, 250, 0.4);
}

.capsule-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.feature-capsule .feature-icon {
  font-size: 32px;
}

.feature-capsule h3 {
  font-size: 20px;
  font-weight: 700;
  color: white;
  margin: 0;
}

.feature-capsule p {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  margin-bottom: 24px;
}

/* Collaboration Effects */
.collaboration-effect {
  position: relative;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.collaborator {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #60a5fa, #7dd3fc);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  animation: collaboratorPulse 2s ease-in-out infinite;
}

.sync-waves {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120px;
  height: 120px;
  border: 2px solid rgba(96, 165, 250, 0.3);
  border-radius: 50%;
  animation: syncWave 3s ease-in-out infinite;
}

@keyframes collaboratorPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

@keyframes syncWave {
  0% { transform: translate(-50%, -50%) scale(0.5); opacity: 1; }
  100% { transform: translate(-50%, -50%) scale(1.5); opacity: 0; }
}

/* Writing Assistant Effects */
.writing-effect {
  position: relative;
  height: 60px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 12px;
}

.writing-cursor {
  width: 2px;
  height: 16px;
  background: #60a5fa;
  animation: blink 1s infinite;
  margin-bottom: 8px;
}

.ai-suggestions {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.suggestion {
  font-size: 10px;
  color: #7dd3fc;
  opacity: 0;
  animation: suggestionAppear 3s ease-in-out infinite;
}

.suggestion:nth-child(2) { animation-delay: 1s; }
.suggestion:nth-child(3) { animation-delay: 2s; }

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

@keyframes suggestionAppear {
  0%, 20% { opacity: 0; transform: translateX(-10px); }
  25%, 75% { opacity: 1; transform: translateX(0); }
  80%, 100% { opacity: 0; transform: translateX(10px); }
}

/* AI Reading Effects */
.reading-effect {
  position: relative;
  height: 60px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 12px;
  overflow: hidden;
}

.document-scan {
  position: relative;
  width: 100%;
  height: 100%;
}

.scan-line {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #60a5fa, transparent);
  animation: scan 3s ease-in-out infinite;
}

.insights {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: 16px;
}

.insight {
  font-size: 10px;
  color: #f472b6;
  opacity: 0;
  animation: insightReveal 3s ease-in-out infinite;
}

.insight:nth-child(2) { animation-delay: 1s; }
.insight:nth-child(3) { animation-delay: 2s; }

@keyframes scan {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(40px); }
}

@keyframes insightReveal {
  0%, 30% { opacity: 0; transform: scale(0.8); }
  35%, 65% { opacity: 1; transform: scale(1); }
  70%, 100% { opacity: 0; transform: scale(0.8); }
}

/* Vector Search Effects */
.search-effect {
  height: 60px;
  padding: 8px;
}

.search-visualization {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.query-vector {
  font-size: 10px;
  color: #60a5fa;
  font-family: monospace;
  text-align: center;
  animation: queryPulse 2s ease-in-out infinite;
}

.result-vectors {
  display: flex;
  justify-content: space-between;
}

.result-vector {
  font-size: 8px;
  font-family: monospace;
  padding: 2px 4px;
  border-radius: 4px;
  animation: resultMatch 3s ease-in-out infinite;
}

.match-high {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.match-medium {
  background: rgba(251, 191, 36, 0.2);
  color: #fbbf24;
  animation-delay: 0.5s;
}

.match-low {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  animation-delay: 1s;
}

@keyframes queryPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

@keyframes resultMatch {
  0%, 100% { opacity: 0.5; transform: scale(0.9); }
  50% { opacity: 1; transform: scale(1); }
}

/* Technology Highlights */
.tech-feature {
  margin-bottom: 120px;
}

.tech-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
}

.tech-content.reverse {
  grid-template-columns: 1fr 1fr;
}

.tech-text h3 {
  font-size: 36px;
  font-weight: 700;
  color: white;
  margin-bottom: 24px;
  text-shadow: 0 0 20px #60a5fa;
}

.tech-text p {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  margin-bottom: 32px;
}

.tech-benefits {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tech-benefits li {
  color: #60a5fa;
  font-size: 16px;
  padding: 12px 0;
  border-bottom: 1px solid rgba(96, 165, 250, 0.1);
  position: relative;
  padding-left: 24px;
}

.tech-benefits li:before {
  content: "▸";
  position: absolute;
  left: 0;
  color: #7dd3fc;
  font-weight: bold;
}

/* Graph Structure Visual */
.graph-container {
  position: relative;
  width: 300px;
  height: 300px;
  margin: 0 auto;
}

.graph-node {
  position: absolute;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: rgba(96, 165, 250, 0.2);
  border: 2px solid #60a5fa;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  transition: all 0.3s ease;
}

.graph-node.central {
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(96, 165, 250, 0.4);
  animation: centralPulse 3s ease-in-out infinite;
}

.graph-node.satellite {
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(var(--angle)) translateY(-120px) rotate(calc(-1 * var(--angle)));
  animation: satelliteOrbit 12s linear infinite;
}

.graph-connections {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.connection {
  position: absolute;
  width: 120px;
  height: 2px;
  background: linear-gradient(90deg, #60a5fa, transparent);
  transform-origin: 0 50%;
  transform: rotate(var(--angle));
  animation: connectionPulse 3s ease-in-out infinite;
}

.pulse-effect {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120px;
  height: 120px;
  border: 2px solid rgba(96, 165, 250, 0.3);
  border-radius: 50%;
  animation: graphPulse 4s ease-in-out infinite;
}

@keyframes centralPulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); box-shadow: 0 0 20px rgba(96, 165, 250, 0.5); }
  50% { transform: translate(-50%, -50%) scale(1.1); box-shadow: 0 0 40px rgba(96, 165, 250, 0.8); }
}

@keyframes satelliteOrbit {
  0% { transform: translate(-50%, -50%) rotate(var(--angle)) translateY(-120px) rotate(calc(-1 * var(--angle))); }
  100% { transform: translate(-50%, -50%) rotate(calc(var(--angle) + 360deg)) translateY(-120px) rotate(calc(-1 * (var(--angle) + 360deg))); }
}

@keyframes connectionPulse {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}

@keyframes graphPulse {
  0% { transform: translate(-50%, -50%) scale(1); opacity: 0.3; }
  50% { transform: translate(-50%, -50%) scale(1.5); opacity: 0.1; }
  100% { transform: translate(-50%, -50%) scale(2); opacity: 0; }
}

/* Version History Visual */
.timeline-container {
  width: 300px;
  margin: 0 auto;
}

.timeline {
  position: relative;
  padding: 20px 0;
}

.timeline:before {
  content: '';
  position: absolute;
  left: 30px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(180deg, #60a5fa, #7dd3fc);
}

.timeline-item {
  position: relative;
  padding-left: 80px;
  margin-bottom: 30px;
  opacity: 0;
  animation: timelineAppear 0.8s ease-out forwards;
}

.timeline-dot {
  position: absolute;
  left: 22px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #60a5fa;
  border: 3px solid #031026;
  box-shadow: 0 0 20px rgba(96, 165, 250, 0.5);
}

.timeline-item.active .timeline-dot {
  background: #7dd3fc;
  animation: activeDot 2s ease-in-out infinite;
}

.timeline-content {
  background: rgba(255, 255, 255, 0.05);
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid rgba(96, 165, 250, 0.2);
  color: white;
  font-size: 14px;
}

.version-diff {
  margin-top: 30px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  padding: 16px;
  font-family: monospace;
  font-size: 12px;
}

.diff-line {
  padding: 4px 0;
  border-radius: 4px;
  margin: 2px 0;
}

.diff-line.added {
  color: #22c55e;
  background: rgba(34, 197, 94, 0.1);
}

.diff-line.removed {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.diff-line.modified {
  color: #f59e0b;
  background: rgba(245, 158, 11, 0.1);
}

@keyframes timelineAppear {
  0% { opacity: 0; transform: translateX(-30px); }
  100% { opacity: 1; transform: translateX(0); }
}

@keyframes activeDot {
  0%, 100% { box-shadow: 0 0 20px rgba(96, 165, 250, 0.5); }
  50% { box-shadow: 0 0 40px rgba(125, 211, 252, 0.8); }
}

.cta-content {
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
}

.cta-title {
  font-size: 48px;
  font-weight: 900;
  color: white;
  margin-bottom: 24px;
  text-shadow: 0 0 30px #60a5fa;
}

.cta-description {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 48px;
}

.dive-btn {
  position: relative;
  background: linear-gradient(135deg, #60a5fa 0%, #7dd3fc 100%);
  border: none;
  border-radius: 50px;
  padding: 20px 60px;
  font-size: 24px;
  font-weight: 700;
  color: white;
  cursor: pointer;
  box-shadow: 
    0 8px 32px rgba(96, 165, 250, 0.4),
    inset 0 1px 2px rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  overflow: hidden;
}

.dive-btn:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 12px 48px rgba(96, 165, 250, 0.6),
    inset 0 1px 2px rgba(255, 255, 255, 0.3);
}

.dive-btn:active {
  transform: translateY(0);
}

.btn-text {
  position: relative;
  z-index: 2;
}

.btn-particles {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, 
    rgba(255, 255, 255, 0.2) 0%, 
    transparent 70%);
  border-radius: inherit;
  transform: translate(-50%, -50%) scale(0);
  transition: transform 0.3s ease;
}

.dive-btn:hover .btn-particles {
  transform: translate(-50%, -50%) scale(1.2);
}

@media (max-width: 768px) {
  .section-title {
    font-size: 40px;
  }
  
  .intro-description, .why-description {
    font-size: 16px;
  }
  
  .comparison-visual {
    flex-direction: column;
    gap: 30px;
  }
  
  .vs-arrow {
    transform: rotate(90deg);
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    gap: 30px;
  }
  
  .feature-capsule {
    padding: 24px;
  }
  
  .tech-content {
    grid-template-columns: 1fr;
    gap: 40px;
    text-align: center;
  }
  
  .tech-text h3 {
    font-size: 28px;
  }
  
  .graph-container, .timeline-container {
    width: 250px;
  }
  
  .cta-title {
    font-size: 32px;
  }
  
  .dive-btn {
    padding: 16px 40px;
    font-size: 20px;
  }
}
</style>