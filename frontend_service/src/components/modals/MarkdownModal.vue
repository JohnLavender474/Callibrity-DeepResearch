<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen" class="modal-overlay" @click="closeModal">
        <div class="modal-container" @click.stop>
          <div class="modal-header">
            <h3 class="modal-title">{{ title }}</h3>
            <button class="close-button" @click="closeModal" title="Close">
              <X :size="20" />
            </button>
          </div>
          
          <div class="modal-body">
            <div class="markdown-content" v-html="renderedMarkdown"></div>
          </div>
          
          <div class="modal-footer">
            <button class="copy-button-modal" @click="copyContent">
              <Check v-if="copied" :size="18" />
              <Copy v-else :size="18" />
              <span>{{ copied ? 'Copied!' : 'Copy to clipboard' }}</span>
            </button>
            <button class="close-button-text" @click="closeModal">
              Close
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { marked } from 'marked'
import { X, Copy, Check } from 'lucide-vue-next'


interface MarkdownModalProps {
  isOpen: boolean
  title: string
  content: string
}

const props = defineProps<MarkdownModalProps>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const copied = ref(false)

const renderedMarkdown = computed(() => {
  return marked(props.content)
})

const closeModal = () => {
  emit('close')
}

const copyContent = async () => {
  try {
    await navigator.clipboard.writeText(props.content)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy text:', err)
  }
}

watch(() => props.isOpen, (newValue) => {
  if (newValue) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
    copied.value = false
  }
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #334155;
}

.close-button {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.close-button:hover {
  background: #f1f5f9;
  color: #334155;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.markdown-content {
  font-size: 0.95rem;
  line-height: 1.6;
  color: #334155;
}

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.copy-button-modal {
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  font-weight: 500;
}

.copy-button-modal:hover {
  background: #e2e8f0;
  color: #334155;
  border-color: #94a3b8;
}

.close-button-text {
  background: transparent;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  color: #64748b;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  font-weight: 500;
}

.close-button-text:hover {
  background: #f1f5f9;
  color: #334155;
  border-color: #94a3b8;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
