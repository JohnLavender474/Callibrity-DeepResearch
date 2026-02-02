export default interface ChatMessageViewModel {
  id: string
  role: 'user' | 'ai'
  content: any
  timestamp: Date
}
