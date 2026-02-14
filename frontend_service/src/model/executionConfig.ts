export default interface ExecutionConfig {
  processOverride?: string
  modelSelection?: string
  allowGeneralKnowledgeFallback?: boolean
  allowWebSearch?: boolean
  temperature?: number
  reasoningLevel?: string
}
