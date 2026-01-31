<template>
  <div class="research">
    <h1>Research</h1>
    <div class="research-form">
      <textarea
        v-model="query"
        placeholder="Enter your research query..."
        rows="4"
      ></textarea>
      <button @click="submitResearch" :disabled="loading">
        {{ loading ? 'Processing...' : 'Submit Research' }}
      </button>
    </div>

    <div v-if="result" class="result">
      <h2>Result</h2>
      <pre>{{ result }}</pre>
    </div>

    <div v-if="error" class="error">
      <h2>Error</h2>
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'


const query = ref('')
const result = ref('')
const error = ref('')
const loading = ref(false)

const submitResearch = async () => {
  if (!query.value.trim()) {
    error.value = 'Please enter a query'
    return
  }

  loading.value = true
  error.value = ''
  result.value = ''
  /*
  try {
    const response = await axios.post(
      '/api/research',
      { query: query.value }
    )
    result.value = JSON.stringify(response.data, null, 2)
  } catch (err: any) {
    error.value = err.response?.data?.message || err.message || 'An error occurred'
  } finally {
    loading.value = false
  }
  */

  await new Promise((resolve) => setTimeout(resolve, 1000))
  result.value = `Simulated response for query: "${query.value}"`
  loading.value = false
}
</script>

<style scoped>
.research {
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  color: #2c3e50;
  margin-bottom: 2rem;
}

.research-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

textarea {
  padding: 1rem;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: inherit;
}

button {
  padding: 1rem 2rem;
  font-size: 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover:not(:disabled) {
  background-color: #38a071;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.result,
.error {
  margin-top: 2rem;
  padding: 1rem;
  border-radius: 4px;
}

.result {
  background-color: #f0f9ff;
  border: 1px solid #0ea5e9;
}

.error {
  background-color: #fef2f2;
  border: 1px solid #ef4444;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  font-size: 0.9rem;
}
</style>
