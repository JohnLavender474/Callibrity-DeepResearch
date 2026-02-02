import type TaskCitation from './taskCitation'


export default interface TaskEntry {
  task: string
  success: boolean
  result?: string
  reasoning?: string
  citations: TaskCitation[]
}
