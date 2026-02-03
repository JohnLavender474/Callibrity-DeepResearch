<template>
    <div class="file-upload">
        <UploadFile
            :uploading="uploading"
            @file-selected="handleFile"
        />

        <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
        </div>

        <div class="uploaded-files">
            <h4>Uploaded Documents</h4>
            <div v-if="loadingDocuments" class="loading-container">
                <div class="spinner"></div>
            </div>
            <ul v-else>
                <li
                    v-for="file in uploadedFiles"
                    :key="file.filename"
                    @click="openDocumentModal(file)"
                    class="document-row"
                >
                    <span class="file-name">{{ file.filename }}</span>
                </li>
                <li v-if="uploadedFiles.length === 0" class="no-documents">
                    No documents uploaded yet
                </li>
            </ul>
        </div>

        <DocumentModal
            :is-open="isModalOpen"
            :document="selectedDocument"
            :profile-id="profileId"
            @close="closeDocumentModal"
            @document-deleted="handleDocumentDeleted"
        />
    </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { uploadFile, fetchFilesForProfile } from '@/services/fileService'
import DocumentModal from './modals/DocumentModal.vue'
import UploadFile from './UploadFile.vue'
import '@/styles/shared.css'
import type FileInfo from '@/model/fileInfo'


interface FileManagementProps {
    profileId: string
}

const props = defineProps<FileManagementProps>()

const emit = defineEmits<{
    (e: 'file-uploaded', filename: string): void
}>()

const uploadedFiles = ref<FileInfo[]>([])
const uploading = ref(false)
const loadingDocuments = ref(false)

const errorMessage = ref('')

const isModalOpen = ref(false)
const selectedDocument = ref<FileInfo | null>(null)

const loadUploadedFiles = async (profileId: string) => {
    if (!profileId) {
        uploadedFiles.value = []
        loadingDocuments.value = false
        return
    }

    loadingDocuments.value = true
    try {
        uploadedFiles.value = await fetchFilesForProfile(profileId)
    } catch (error) {
        console.error('Failed to load documents:', error)
        uploadedFiles.value = []
    } finally {
        loadingDocuments.value = false
    }
}

const handleFile = async (file: File) => {
    errorMessage.value = ''

    if (!file.name.toLowerCase().endsWith('.pdf')) {
        errorMessage.value = 'Only PDF files are allowed'
        return
    }

    const existingFile = uploadedFiles.value.find(
        (f) => f.filename === file.name
    )
    if (existingFile) {
        errorMessage.value = 'A file with this name already exists'
        return
    }

    uploading.value = true

    try {
        await uploadFile(props.profileId, file)
        await loadUploadedFiles(props.profileId)
        emit('file-uploaded', file.name)
    } catch (error) {
        errorMessage.value =
            error instanceof Error
                ? error.message
                : 'Failed to upload document'
    } finally {
        uploading.value = false
    }
}

const openDocumentModal = (document: FileInfo) => {
    selectedDocument.value = document
    isModalOpen.value = true
}

const closeDocumentModal = () => {
    isModalOpen.value = false
    selectedDocument.value = null
}

const handleDocumentDeleted = async () => {
    await loadUploadedFiles(props.profileId)
}

watch(
    () => props.profileId,
    (newProfileId) => {
        loadUploadedFiles(newProfileId)
    },
    { immediate: true }
)
</script>

<style scoped>
.file-upload {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    height: 100%;
}

.uploaded-files {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 1rem;
    flex: 1;
    overflow-y: auto;
    min-height: 0;
    display: flex;
    flex-direction: column;
}

.uploaded-files h4 {
    margin: 0 0 0.75rem 0;
    font-size: 0.9rem;
    color: #475569;
    flex-shrink: 0;
}

.uploaded-files ul {
    list-style: none;
    padding: 0;
    margin: 0;
    flex: 1;
    overflow-y: auto;
    min-height: 0;
}

.document-row {
    display: flex;
    align-items: center;
    padding: 0.75rem;
    background-color: white;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    margin-bottom: 0.5rem;
    cursor: pointer;
    transition: all 0.2s;
}

.document-row:hover {
    background-color: #f1f5f9;
    border-color: #cbd5e1;
}

.document-row:last-child {
    margin-bottom: 0;
}

.no-documents {
    padding: 1rem;
    text-align: center;
    color: #94a3b8;
    font-size: 0.9rem;
    background-color: transparent;
    border: none;
    cursor: default;
}

.no-documents:hover {
    background-color: transparent;
    border-color: #e2e8f0;
}

.file-name {
    font-size: 0.9rem;
    color: #334155;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.error-message {
    padding: 0.75rem 1rem;
    background-color: #fef2f2;
    border: 1px solid #fecaca;
    border-radius: 6px;
    color: #dc2626;
    font-size: 0.9rem;
}
</style>
