<template>
  <div class="dashboard">
    <HeaderBar />

    <!-- Main Content -->
    <div class="dashboard-content">
      <!-- Sidebar -->
      <aside class="sidebar">
        <div class="sidebar-section">
          <h3>Your Enterprise</h3>
          <div class="enterprise-card">
            <div class="enterprise-logo">🏢</div>
            <div class="enterprise-info">
              <div class="enterprise-name">Acme Corp</div>
              <div class="enterprise-plan">Enterprise Plan</div>
            </div>
          </div>
        </div>

        <div class="sidebar-section">
          <h3>Quick Actions</h3>
          <div class="quick-actions">
            <button class="action-btn" @click="router.push({ name: 'pages.list' })">
              📄 Browse Pages
            </button>
            <button class="action-btn" @click="router.push({ name: 'pages.create' })">
              ✏️ Create Page
            </button>
            <button class="action-btn">
              📊 View Analytics
            </button>
            <button class="action-btn">
              👥 Manage Users
            </button>
          </div>
        </div>

        <div class="sidebar-section">
          <h3>Recent Activity</h3>
          <div class="activity-list">
            <div class="activity-item">
              <span class="activity-icon">📝</span>
              <div class="activity-text">
                <div>Page "Product Roadmap" updated</div>
                <div class="activity-time">2 hours ago</div>
              </div>
            </div>
            <div class="activity-item">
              <span class="activity-icon">🔍</span>
              <div class="activity-text">
                <div>Search performed: "AI integration"</div>
                <div class="activity-time">5 hours ago</div>
              </div>
            </div>
            <div class="activity-item">
              <span class="activity-icon">👤</span>
              <div class="activity-text">
                <div>New user Sarah joined</div>
                <div class="activity-time">1 day ago</div>
              </div>
            </div>
          </div>
        </div>
      </aside>

      <!-- Main Panel -->
      <main class="main-panel">
        <div class="panel-header">
          <h1>Welcome back, John!</h1>
          <p>Here's what's happening with your documents today.</p>
        </div>

        <!-- Stats Grid -->
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">📄</div>
            <div class="stat-content">
              <div class="stat-number">247</div>
              <div class="stat-label">Total Documents</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">🔍</div>
            <div class="stat-content">
              <div class="stat-number">1,432</div>
              <div class="stat-label">Searches Today</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">👥</div>
            <div class="stat-content">
              <div class="stat-number">23</div>
              <div class="stat-label">Active Users</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">🤖</div>
            <div class="stat-content">
              <div class="stat-number">89</div>
              <div class="stat-label">AI Assists</div>
            </div>
          </div>
        </div>

        <!-- Feature Cards -->
        <div class="features-section">
          <h2>Available Features</h2>
          <div class="features-grid">
            
            <!-- Actual Features -->
            <div class="feature-card clickable" @click="router.push({ name: 'pages.list' })">
              <div class="feature-header">
                <div class="feature-icon">📚</div>
                <h3>Documents & Pages</h3>
              </div>
              <p>Create, edit, and organize your documents with intelligent chapters and linking.</p>
              <div class="feature-status active">Active</div>
            </div>

            <div class="feature-card clickable" @click="router.push({ name: 'pages.list' })">
              <div class="feature-header">
                <div class="feature-icon">📖</div>
                <h3>Chapter Management</h3>
              </div>
              <p>Organize your content into logical chapters with hierarchical structure.</p>
              <div class="feature-status active">Active</div>
            </div>

            <!-- Dummy Enterprise Features -->
            <div class="feature-card">
              <div class="feature-header">
                <div class="feature-icon">🔐</div>
                <h3>Enterprise Security</h3>
              </div>
              <p>Advanced security controls, audit logs, and compliance management.</p>
              <div class="feature-status">Coming Soon</div>
            </div>

            <div class="feature-card">
              <div class="feature-header">
                <div class="feature-icon">📊</div>
                <h3>Advanced Analytics</h3>
              </div>
              <p>Deep insights into document usage, search patterns, and team collaboration.</p>
              <div class="feature-status">Coming Soon</div>
            </div>

            <div class="feature-card">
              <div class="feature-header">
                <div class="feature-icon">🔗</div>
                <h3>API Integration</h3>
              </div>
              <p>Connect with your existing tools via REST API and webhooks.</p>
              <div class="feature-status">Coming Soon</div>
            </div>

            <div class="feature-card">
              <div class="feature-header">
                <div class="feature-icon">👥</div>
                <h3>Team Management</h3>
              </div>
              <p>User roles, permissions, and collaborative workspace management.</p>
              <div class="feature-status">Coming Soon</div>
            </div>

            <div class="feature-card">
              <div class="feature-header">
                <div class="feature-icon">🌍</div>
                <h3>Multi-tenant</h3>
              </div>
              <p>Isolated workspaces for different departments or clients.</p>
              <div class="feature-status">Coming Soon</div>
            </div>

            <div class="feature-card">
              <div class="feature-header">
                <div class="feature-icon">🔄</div>
                <h3>Workflow Automation</h3>
              </div>
              <p>Automate document workflows with triggers and actions.</p>
              <div class="feature-status">Coming Soon</div>
            </div>

          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<style scoped>
.dashboard {
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
  gap: 24px;
}

.notifications {
  position: relative;
  font-size: 20px;
  cursor: pointer;
}

.notification-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #f59e0b;
  color: white;
  border-radius: 50%;
  font-size: 12px;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.profile-section {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.profile-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px solid #60a5fa;
}

.dashboard-content {
  display: grid;
  grid-template-columns: 300px 1fr;
  min-height: calc(100vh - 70px);
}

.sidebar {
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(10px);
  border-right: 1px solid rgba(96, 165, 250, 0.2);
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

.enterprise-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: rgba(96, 165, 250, 0.1);
  border-radius: 12px;
  border: 1px solid rgba(96, 165, 250, 0.2);
}

.enterprise-logo {
  font-size: 24px;
}

.enterprise-name {
  font-weight: 600;
  color: white;
}

.enterprise-plan {
  font-size: 12px;
  color: #60a5fa;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.action-btn {
  background: transparent;
  border: 1px solid rgba(96, 165, 250, 0.3);
  color: white;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.action-btn:hover {
  background: rgba(96, 165, 250, 0.1);
  border-color: rgba(96, 165, 250, 0.5);
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.activity-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 8px;
}

.activity-icon {
  font-size: 16px;
}

.activity-text {
  flex: 1;
  font-size: 14px;
}

.activity-time {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  margin-top: 4px;
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

.features-section h2 {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 24px;
  color: white;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.feature-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(96, 165, 250, 0.2);
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s ease;
  position: relative;
}

.feature-card.clickable {
  cursor: pointer;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(96, 165, 250, 0.2);
  border-color: rgba(96, 165, 250, 0.4);
}

.feature-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.feature-icon {
  font-size: 24px;
}

.feature-card h3 {
  font-size: 18px;
  font-weight: 600;
  color: white;
  margin: 0;
}

.feature-card p {
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.5;
  margin-bottom: 16px;
}

.feature-status {
  position: absolute;
  top: 16px;
  right: 16px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  background: rgba(156, 163, 175, 0.2);
  color: #9ca3af;
}

.feature-status.active {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

@media (max-width: 768px) {
  .dashboard-content {
    grid-template-columns: 1fr;
  }
  
  .sidebar {
    display: none;
  }
  
  .main-nav {
    display: none;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>