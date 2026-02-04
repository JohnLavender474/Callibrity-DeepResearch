import { ref } from 'vue'

import type Toast from '@/model/toast'
import type { ToastType } from '@/model/toastType'


const toasts = ref<Toast[]>([])


const addToast = (
    message: string,
    type: ToastType,
): void => {
    const id = `${Date.now()}-${Math.random().toString(36).slice(2, 10)}`
    toasts.value.push({
        id,
        message,
        type,
    })

    setTimeout(() => {
        toasts.value = toasts.value.filter(
            (toast) => toast.id !== id
        )
    }, 4000)
}


export const useToasts = () => {
    return {
        toasts,
        addToast,
    }
}
