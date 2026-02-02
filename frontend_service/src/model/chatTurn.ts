export default interface ChatTurn {
    id: string
    conversation_id: string
    role: string
    data: Record<string, any>
    timestamp: string
}
