import type { ToastType } from '@/model/toastType'


export default interface Toast {
    id: string
    message: string
    type: ToastType
}
