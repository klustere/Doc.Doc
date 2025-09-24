import { createApp } from 'vue'
import App from './App.vue'
import './styles/global.css'

// Vue Router setup
import { createRouter, createWebHistory } from 'vue-router'
const routes = [
	{ name: 'home', path: '/', component: () => import('./pages/Home.vue') },
	{ name: 'login', path: '/login', component: () => import('./pages/Login.vue') },
	{ name: 'dashboard', path: '/dashboard', component: () => import('./pages/Dashboard.vue') },
	{ name: 'pages.list', path: '/pages', component: () => import('./components/PagesList.vue') },
	{ name: 'pages.create', path: '/edit', component: () => import('./components/PageEditor.vue') },
	{ name: 'pages.view', path: '/pages/:id', component: () => import('./components/PageView.vue') },
	{ name: 'pages.edit', path: '/edit/:id', component: () => import('./components/PageEditor.vue') },
	{ name: 'graph', path: '/graph', component: () => import('./components/GraphView.vue') },
	{ name: 'version-history', path: '/version-history', component: () => import('./components/VersionHistory.vue') },
]
const router = createRouter({
	history: createWebHistory(),
	routes,
})

// Pinia setup
import { createPinia } from 'pinia'
const pinia = createPinia()

const app = createApp(App)
app.use(router)
app.use(pinia)

console.log('mounting app to #app')
try {
	const mounted = app.mount('#app')
	console.log('app mounted (debug):', mounted)
} catch (err) {
	console.error('Error mounting app:', err)
}
