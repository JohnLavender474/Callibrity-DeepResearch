import type ExecutionConfig from './executionConfig'


export default interface UserQueryRequest {
  query: string
  executionConfig?: ExecutionConfig
}
