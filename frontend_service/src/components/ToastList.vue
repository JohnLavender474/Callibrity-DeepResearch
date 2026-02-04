<template>
    <div class="toast-container">
        <div
            v-for="toast in props.toasts"
            :key="toast.id"
            class="toast"
            :class="toast.type"
        >
            {{ toast.message }}
        </div>
    </div>
</template>

<script setup lang="ts">
import type Toast from '@/model/toast'


interface ToastListProps {
    toasts: Toast[]
}

const props = defineProps<ToastListProps>()
</script>

<style scoped>
.toast-container {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    z-index: 9999;
    max-width: 400px;
}

.toast {
    padding: 0.75rem 1rem;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 500;
    border: 1px solid transparent;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

.toast.info {
    background-color: #eff6ff;
    border-color: #bfdbfe;
    color: #1d4ed8;
}

.toast.success {
    background-color: #ecfdf3;
    border-color: #bbf7d0;
    color: #166534;
}

.toast.error {
    background-color: #fef2f2;
    border-color: #fecaca;
    color: #dc2626;
}
</style>
