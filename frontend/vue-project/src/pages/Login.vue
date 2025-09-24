<template>
  <div class="login-page">
    <div class="login-background">
      <div class="login-particles"></div>
      <div class="login-waves"></div>
    </div>
    
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <div class="logo">🧠 Confluence</div>
          <h1>Welcome Back</h1>
          <p>Sign in to access your intelligent document workspace</p>
        </div>
        
        <form @submit.prevent="handleLogin" class="login-form">
          <!-- Error Display -->
          <div v-if="error" class="error-message">
            <div class="error-icon">⚠️</div>
            <span>{{ error }}</span>
          </div>
          
          <!-- Success Message -->
          <div v-if="success" class="success-message">
            <div class="success-icon">✅</div>
            <span>{{ success }}</span>
          </div>
          
          <!-- Username Input -->
          <div class="input-group">
            <label for="username">Username</label>
            <input 
              id="username"
              v-model="username" 
              type="text" 
              placeholder="Enter your username"
              :disabled="loading"
              required
              class="login-input"
            />
          </div>
          
          <!-- Password Input -->
          <div class="input-group">
            <label for="password">Password</label>
            <input 
              id="password"
              v-model="password" 
              type="password" 
              placeholder="Enter your password"
              :disabled="loading"
              required
              class="login-input"
            />
          </div>
          
          <!-- Test User Info -->
          <div class="test-user-info">
            <div class="info-icon">💡</div>
            <div>
              <strong>Test User:</strong> username: <code>john</code>, password: <code>123</code>
            </div>
          </div>
          
          <!-- Login Button -->
          <button 
            type="submit" 
            :disabled="loading || !username.trim() || !password.trim()"
            class="login-button"
          >
            <span v-if="!loading">🚀 Sign In</span>
            <span v-else class="loading-text">
              <span class="spinner"></span>
              Signing in...
            </span>
          </button>
          
          <!-- Create Test User Button -->
          <button 
            type="button" 
            @click="createTestUser"
            :disabled="loading"
            class="create-user-button"
          >
            <span v-if="!creatingUser">👤 Create Test User</span>
            <span v-else class="loading-text">
              <span class="spinner"></span>
              Creating...
            </span>
          </button>
        </form>
        
        <!-- Back to Home -->
        <div class="login-footer">
          <button @click="$router.push('/')" class="back-button">
            ← Back to Home
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Form state
const username = ref('')
const password = ref('')
const loading = ref(false)
const creatingUser = ref(false)
const error = ref('')
const success = ref('')

// Auto-fill test credentials
username.value = 'john'
password.value = '123'

async function handleLogin() {
  if (!username.value.trim() || !password.value.trim()) {
    error.value = 'Please enter both username and password'
    return
  }
  
  loading.value = true
  error.value = ''
  success.value = ''
  
  try {
    const response = await fetch('http://127.0.0.1:8000/api/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username.value.trim(),
        password: password.value.trim()
      })
    })
    
    const data = await response.json()
    
    if (response.ok && data.success) {
      success.value = 'Login successful! Redirecting to dashboard...'
      
      // Store user info in localStorage (simple session)
      localStorage.setItem('user', JSON.stringify(data.user))
      
      // Redirect to dashboard after short delay
      setTimeout(() => {
        router.push('/dashboard')
      }, 1000)
      
    } else {
      error.value = data.error || 'Login failed'
    }
    
  } catch (e) {
    console.error('Login error:', e)
    error.value = 'Unable to connect to server. Please try again.'
  } finally {
    loading.value = false
  }
}

async function createTestUser() {
  creatingUser.value = true
  error.value = ''
  success.value = ''
  
  try {
    const response = await fetch('http://127.0.0.1:8000/api/create-test-user/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    const data = await response.json()
    
    if (response.ok && data.success) {
      success.value = data.message + ' You can now sign in!'
    } else {
      error.value = data.error || 'Failed to create test user'
    }
    
  } catch (e) {
    console.error('Create user error:', e)
    error.value = 'Unable to connect to server. Please try again.'
  } finally {
    creatingUser.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.login-background {
  position: absolute;
  inset: 0;
  z-index: 1;
}

.login-particles {
  position: absolute;
  inset: 0;
  background: 
    radial-gradient(circle at 20% 80%, rgba(96, 165, 250, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(167, 243, 208, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(196, 181, 253, 0.1) 0%, transparent 50%);
  animation: particleFloat 8s ease-in-out infinite;
}

.login-waves {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(96, 165, 250, 0.03) 25%, 
    rgba(167, 243, 208, 0.03) 50%, 
    rgba(196, 181, 253, 0.03) 75%, 
    transparent 100%);
  animation: waveFlow 6s linear infinite;
}

@keyframes particleFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(-20px, -20px) scale(1.05); }
  66% { transform: translate(20px, -10px) scale(0.95); }
}

@keyframes waveFlow {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.login-container {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 400px;
  padding: 20px;
}

.login-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(96, 165, 250, 0.2);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo {
  font-size: 32px;
  font-weight: 900;
  color: #60a5fa;
  text-shadow: 0 0 20px #60a5fa;
  margin-bottom: 16px;
}

.login-header h1 {
  font-size: 28px;
  font-weight: 700;
  color: white;
  margin: 0 0 8px 0;
}

.login-header p {
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
  font-size: 14px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.error-message,
.success-message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
}

.error-message {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
}

.success-message {
  background: rgba(34, 197, 94, 0.1);
  border: 1px solid rgba(34, 197, 94, 0.3);
  color: #86efac;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-group label {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
}

.login-input {
  padding: 14px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(96, 165, 250, 0.3);
  border-radius: 12px;
  color: white;
  font-size: 16px;
  transition: all 0.3s ease;
}

.login-input:focus {
  outline: none;
  border-color: rgba(96, 165, 250, 0.6);
  box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1);
  background: rgba(255, 255, 255, 0.08);
}

.login-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.login-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.test-user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: rgba(96, 165, 250, 0.1);
  border: 1px solid rgba(96, 165, 250, 0.2);
  border-radius: 12px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.8);
}

.test-user-info code {
  background: rgba(0, 0, 0, 0.3);
  padding: 2px 6px;
  border-radius: 4px;
  color: #93c5fd;
  font-family: 'Courier New', monospace;
}

.login-button,
.create-user-button {
  padding: 14px 20px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.login-button {
  background: linear-gradient(135deg, #60a5fa 0%, #7dd3fc 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(96, 165, 250, 0.3);
}

.login-button:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(96, 165, 250, 0.4);
}

.create-user-button {
  background: rgba(34, 197, 94, 0.2);
  border: 1px solid rgba(34, 197, 94, 0.3);
  color: #86efac;
}

.create-user-button:not(:disabled):hover {
  background: rgba(34, 197, 94, 0.3);
  transform: translateY(-1px);
}

.login-button:disabled,
.create-user-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.loading-text {
  display: flex;
  align-items: center;
  gap: 8px;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.login-footer {
  margin-top: 24px;
  text-align: center;
}

.back-button {
  background: transparent;
  border: 1px solid rgba(96, 165, 250, 0.3);
  color: rgba(255, 255, 255, 0.7);
  padding: 10px 20px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
}

.back-button:hover {
  background: rgba(96, 165, 250, 0.1);
  color: white;
}

.info-icon,
.error-icon,
.success-icon {
  font-size: 16px;
  flex-shrink: 0;
}

@media (max-width: 480px) {
  .login-container {
    padding: 16px;
  }
  
  .login-card {
    padding: 24px;
    border-radius: 16px;
  }
  
  .logo {
    font-size: 28px;
  }
  
  .login-header h1 {
    font-size: 24px;
  }
}
</style>