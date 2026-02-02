export default interface Invocation {
  invocation_id: string
  profile_id: string
  user_query: string
  status: string
  graph_state: Record<string, any> | null
  created_at: string
  updated_at: string
}
