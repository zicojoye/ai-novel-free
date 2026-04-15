// 工作室和聊天相关类型

export interface ChatMessage {
  id: number
  room_id: string
  sender_id: number
  sender_type: 'agent' | 'user'
  content: string
  mentions?: number[]
  message_type: 'text' | 'image' | 'file'
  metadata?: Record<string, any>
  reply_to_id?: number
  status: 'sending' | 'sent' | 'delivered' | 'read' | 'failed'
  created_at: string
  updated_at: string
}

export interface ChatRoom {
  id: number
  project_id: number
  name: string
  room_type: 'workspace' | 'team' | 'private' | 'system'
  member_ids: number[]
  description?: string
  settings?: Record<string, any>
  created_by: number
  created_at: string
  updated_at: string
  last_message_at: string
}

export interface ChatRoomCreate {
  project_id: number
  name: string
  room_type: 'workspace' | 'team' | 'private'
  member_ids: number[]
  description?: string
  settings?: Record<string, any>
}

export interface ChatRoomUpdate {
  name?: string
  description?: string
  member_ids?: number[]
  settings?: Record<string, any>
}

export interface Agent {
  id: number
  name: string
  role: string
  status: 'idle' | 'active' | 'completed' | 'error'
  avatar?: string
  last_activity?: string
  tasks_completed: number
}

export interface EventStream {
  id: number
  project_id: number
  event_type: EventType
  source: {
    id: number
    type: string
  }
  target?: {
    id: number
    type: string
  }
  description: string
  task_id?: number
  chapter_id?: number
  data?: Record<string, any>
  importance: number
  created_at: string
}

export type EventType =
  | 'task_start'
  | 'task_progress'
  | 'task_complete'
  | 'task_error'
  | 'agent_message'
  | 'agent_mention'
  | 'agent_response'
  | 'system_notice'
  | 'memory_update'
  | 'knowledge_update'

export interface CategorizedEvents {
  tasks: EventStream[]
  messages: EventStream[]
  memory: EventStream[]
  knowledge: EventStream[]
  system: EventStream[]
  errors: EventStream[]
}

export interface WebSocketMessage {
  type: 'message' | 'event' | 'mention' | 'task_update' | 'ping' | 'pong' | 'subscribe' | 'message_sent' | 'agent_message_sent' | 'error'
  [key: string]: any
}

export interface TypingUser {
  id: number
  name: string
  role: string
}

export interface Memory {
  id: number
  agent_id: number
  project_id: number
  memory_type: 'stm' | 'ltm' | 'wm'
  content: string
  summary?: string
  priority: 'critical' | 'high' | 'medium' | 'low' | 'trivial'
  importance_score: number
  tags?: string[]
  metadata?: Record<string, any>
  status: 'active' | 'archived' | 'verified' | 'conflict'
  version: number
  parent_id?: number
  created_at: string
  updated_at: string
  last_accessed?: string
  access_count: number
  verified: boolean
  linked_memory_ids?: number[]
}

export interface MemoryOperation {
  id: number
  memory_id: number
  operation:
    | 'create_memory'
    | 'read_memory'
    | 'update_memory'
    | 'delete_memory'
    | 'search_memory'
    | 'link_memory'
    | 'prioritize_memory'
    | 'archive_memory'
    | 'recall_memory'
    | 'merge_memory'
    | 'split_memory'
    | 'verify_memory'
  performed_by: number
  performed_at: string
  operation_data?: Record<string, any>
  result: string
  error_message?: string
}
