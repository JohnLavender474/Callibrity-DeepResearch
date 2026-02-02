<template>
  <div class="chat-section">
    <div v-if="props.isLoadingConversation" class="loading-conversation">
      <div class="spinner"></div>
      <span>Loading conversation...</span>
    </div>

    <ChatMessages
      v-else
      :messages="props.messages"
    />

    <UserInput
      ref="userInputRef"
      :disabled="props.isProcessing"
      :loading="props.isLoadingConversation"
      @submit="onSubmit"
    />

    <div v-if="props.error" class="error-banner">
      <p>{{ props.error }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import ChatMessages from './ChatMessages.vue'
import UserInput from './UserInput.vue'
import type ChatMessageViewModel from '@/model/chatMessageViewModel'
import '@/styles/shared.css'


interface ChatSectionProps {
  messages: ChatMessageViewModel[]
  isProcessing: boolean
  isLoadingConversation: boolean
  error: string
  profileId: string
}

const props = defineProps<ChatSectionProps>()

const emit = defineEmits<{
  (e: 'submit', query: string): void
  (e: 'conversation-created', conversationId: string): void
}>()

const userInputRef = ref<InstanceType<typeof UserInput> | null>(null)

const onSubmit = async (query: string) => {
  emit('submit', query)
}

const focusInput = () => {
  userInputRef.value?.focus()
}

defineExpose({
  focusInput,
})
</script>

<style scoped>
.chat-section {
  display: flex;
  flex-direction: column;
  height: 90%;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

.loading-conversation {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  color: #64748b;
  font-size: 0.95rem;
}

.error-banner {
  padding: 0.75rem 1rem;
  background-color: #fef2f2;
  border-top: 1px solid #fecaca;
  color: #dc2626;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.error-banner p {
  margin: 0;
}
</style>
