<template>
    <div
        class="drop-zone"
        :class="{ 'drag-over': isDragOver, 'uploading': uploading }"
        @click="openFileDialog"
    >
        <input
            ref="fileInput"
            type="file"
            accept=".pdf"
            @change="onFileSelected"
            hidden
        />

        <div class="upload-icon">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                width="48"
                height="48"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
            >
                <path
                    d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"
                />
                <polyline points="17 8 12 3 7 8" />
                <line x1="12" y1="3" x2="12" y2="15" />
            </svg>
        </div>

        <p v-if="uploading" class="upload-text">Uploading...</p>
        <p v-else class="upload-text">           
            <span class="upload-subtext">Click to select a file for upload</span>
        </p>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'


interface UploadFileProps {
    uploading: boolean
}

const props = defineProps<UploadFileProps>()

const emit = defineEmits<{
    (e: 'file-selected', file: File): void
}>()

const fileInput = ref<HTMLInputElement | null>(null)

const isDragOver = ref(false)

const openFileDialog = () => {
    if (!props.uploading && fileInput.value) {
        fileInput.value.click()
    }
}

const onFileSelected = (event: Event) => {
    const target = event.target as HTMLInputElement
    const files = target.files
    if (files && files.length > 0) {
        emit('file-selected', files[0])
    }

    if (fileInput.value) {
        fileInput.value.value = ''
    }
}
</script>

<style scoped>
.drop-zone {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    border: 2px dashed #cbd5e1;
    border-radius: 8px;
    background-color: #f8fafc;
    cursor: pointer;
    transition: all 0.2s;
    flex-shrink: 0;
}

.drop-zone:hover {
    border-color: #42b983;
    background-color: #f0fdf4;
}

.drop-zone.drag-over {
    border-color: #42b983;
    background-color: #dcfce7;
}

.drop-zone.uploading {
    opacity: 0.7;
    cursor: not-allowed;
}

.upload-icon {
    color: #94a3b8;
    margin-bottom: 0.5rem;
}

.drop-zone:hover .upload-icon,
.drop-zone.drag-over .upload-icon {
    color: #42b983;
}

.upload-text {
    text-align: center;
    color: #64748b;
    margin: 0;
    font-size: 0.95rem;
}

.upload-subtext {
    font-size: 0.85rem;
    color: #94a3b8;
}
</style>
