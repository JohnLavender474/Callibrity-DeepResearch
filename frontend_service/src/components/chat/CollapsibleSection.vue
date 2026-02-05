<template>
  <div class="collapsible-section">
    <button 
      class="collapsible-header"
      :class="{ expanded: isExpanded }"
      @click="toggle"
    >
      <span class="chevron">{{ isExpanded ? '▼' : '▶' }}</span>
      <span class="header-title">{{ title }}</span>
      <span v-if="badge" class="header-badge">{{ badge }}</span>
    </button>

    <div 
      v-if="isExpanded" 
      class="collapsible-content"
      :class="{ 'markdown-background': markdownBackground }"
    >
      <slot></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'


interface CollapsibleSectionProps {
  title: string
  badge?: string
  defaultExpanded?: boolean
  markdownBackground?: boolean
}

const props = withDefaults(defineProps<CollapsibleSectionProps>(), {
  defaultExpanded: false,
  markdownBackground: false,
})

const isExpanded = ref(props.defaultExpanded)

watch(
  () => props.defaultExpanded,
  (newVal) => {
    isExpanded.value = newVal
  }
)

const toggle = () => {
  isExpanded.value = !isExpanded.value
}
</script>

<style scoped>
.collapsible-section {
  border: 1px solid var(--color-border);
  border-radius: var(--size-border-radius-sm);
  overflow: hidden;
}

.collapsible-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem 1rem;
  background-color: var(--color-surface-hover);
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--color-text-primary);
  text-align: left;
  transition: background-color var(--transition-base);
}

.collapsible-header:hover {
  background-color: var(--color-surface-active);
}

.collapsible-header.expanded {
  border-bottom: 1px solid var(--color-border);
}

.chevron {
  font-size: 0.7rem;
  color: var(--color-text-secondary);
  width: 1rem;
}

.header-title {
  flex: 1;
}

.header-badge {
  padding: 0.125rem 0.5rem;
  background-color: var(--color-border);
  border-radius: 9999px;
  font-size: 0.75rem;
  color: var(--color-text-secondary);
}

.collapsible-content {
  padding: 1rem;
  background-color: var(--color-bg-2);
}

.collapsible-content.markdown-background {
  background-color: white;
}
</style>
