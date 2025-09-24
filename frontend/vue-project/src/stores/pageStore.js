import { defineStore } from 'pinia'
import { ref } from 'vue'

export const usePageStore = defineStore('page', () => {
  const current = ref(null)
  const geminiPrompt = ref('')
  const contextAdded = ref(false)
  function setPage(p) { current.value = p }
  function appendContextToPrompt(text) {
    geminiPrompt.value += '\n\n' + text
    contextAdded.value = true
  }
  function clearPrompt() {
    geminiPrompt.value = ''
    contextAdded.value = false
  }
  return { current, geminiPrompt, contextAdded, setPage, appendContextToPrompt, clearPrompt }
})
