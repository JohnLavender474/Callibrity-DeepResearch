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
}

const props = withDefaults(defineProps<CollapsibleSectionProps>(), {
  defaultExpanded: false,
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
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  overflow: hidden;
}

.collapsible-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem 1rem;
  background-color: #f8fafc;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  color: #334155;
  text-align: left;
  transition: background-color 0.2s;
}

.collapsible-header:hover {
  background-color: #f1f5f9;
}

.collapsible-header.expanded {
  border-bottom: 1px solid #e2e8f0;
}

.chevron {
  font-size: 0.7rem;
  color: #64748b;
  width: 1rem;
}

.header-title {
  flex: 1;
}

.header-badge {
  padding: 0.125rem 0.5rem;
  background-color: #e2e8f0;
  border-radius: 9999px;
  font-size: 0.75rem;
  color: #64748b;
}

.collapsible-content {
  padding: 1rem;
  background-color: white;
}
</style>
