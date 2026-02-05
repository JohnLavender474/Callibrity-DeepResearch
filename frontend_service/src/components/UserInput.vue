<template>
  <div class="user-input">
    <div class="header">
      <button
        type="button"
        class="toggle-button"
        @click="isCollapsed = !isCollapsed"
        :aria-label="isCollapsed ? 'Show input' : 'Hide input'"
      >
        <svg
          :class="{ 'rotated': !isCollapsed }"
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <polyline points="18 15 12 9 6 15"></polyline>
        </svg>
      </button>
    </div>

    <form
      v-show="!isCollapsed"
      @submit.prevent="onSubmit"
      class="input-form"
    >
      <textarea
        ref="textareaRef"
        v-model="query"
        placeholder="Enter your research query..."
        rows="4"
        :disabled="disabled"
        @keydown.meta.enter="onSubmit"        
      ></textarea>

      <button
        type="submit"
        :disabled="disabled || !isValidInput"
      >
        {{ submitButtonText }}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'


interface UserInputProps {
  disabled?: boolean
  loading?: boolean
}

const props = withDefaults(defineProps<UserInputProps>(), {
  disabled: false,
  loading: false,
})

const emit = defineEmits<{
  (e: 'submit', query: string): void
}>()

const query = ref('')
const isCollapsed = ref(false)
const textareaRef = ref<HTMLTextAreaElement | null>(null)

const isValidInput = computed(() => query.value.trim().length > 0)

const submitButtonText = computed(() => {
  if (!query.value.trim()) {
    return 'Type in a prompt...'
  }
  if (props.loading) {
    return 'Loading...'
  }
  if (props.disabled) {
    return 'Processing...'
  }
  return 'Submit Query'
})

const onSubmit = () => {
  if (
    query.value.trim() &&
    !props.disabled &&
    !props.loading
  ) {
    emit('submit', query.value)
    query.value = ''
  }
}

const focus = () => {
  isCollapsed.value = false
  textareaRef.value?.focus()  
}

const clear = () => {
  query.value = ''
}

defineExpose({
  focus,
  clear,
})
</script>

<style scoped>
.user-input {
  padding: 0.5rem 1.5rem 1.5rem;
  border-top: 1px solid var(--color-border);
  background-color: var(--color-bg-2);
  flex-shrink: 0;
}

.header {
  display: flex;
  justify-content: center;
  margin-bottom: 0.5rem;
}

.toggle-button {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  color: var(--color-text-secondary);
  transition: color var(--transition-base);
  display: flex;
  align-items: center;
  justify-content: center;
}

.toggle-button:hover {
  color: var(--color-primary);
}

.toggle-button svg {
  transition: transform var(--transition-slow);
}

.toggle-button svg.rotated {
  transform: rotate(180deg);
}

.input-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

textarea {
  padding: 1rem;
  font-size: 1rem;
  border: 1px solid var(--color-border);
  border-radius: var(--size-border-radius-sm);
  font-family: inherit;
  resize: none;
  transition: border-color var(--transition-base);
  background-color: var(--color-bg-3);
  color: var(--color-text-primary);
}

textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1);
}

textarea:disabled {
  background-color: var(--color-surface-hover);
  color: var(--color-text-tertiary);
  cursor: not-allowed;
}

button {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  background-color: var(--color-primary);
  color: white;
  border: none;
  border-radius: var(--size-border-radius-sm);
  cursor: pointer;
  transition: background-color var(--transition-base);
  font-weight: 500;
}

button:hover:not(:disabled) {
  background-color: var(--color-primary-dark);
}

button:disabled {
  background-color: var(--color-border);
  cursor: not-allowed;
}
</style>
