import type TaskEntry from './taskEntry'


export interface GraphStepDetails {
  input: Record<string, any>
  output: {
    task_entries?: TaskEntry[]
    process_type?: string
    [key: string]: any
  }
}


export default interface GraphStep {
  type: string
  details: GraphStepDetails
}
