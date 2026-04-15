// 通用类型
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  message?: string
  error?: string
}

export interface PaginationParams {
  page: number
  pageSize: number
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
  totalPages: number
}

// 项目类型
export interface Project {
  id: number
  name: string
  description?: string
  genre: string
  targetAudience: string
  status: 'draft' | 'active' | 'completed' | 'archived'
  created_at: string
  updated_at: string
}

// 世界观类型
export interface WorldBuilding {
  id: number
  project_id: number
  core_concept: string
  worldbuilding: string
  characters: Character[]
  factions: Faction[]
  power_system: string
  geography: string
  history: string
  items: Item[]
  main_plot: string
  world_rules: Record<string, unknown>
  created_at?: string
  updated_at?: string
}

export interface Character {
  id: string
  name: string
  role: string
  description: string
  personality: string[]
  background: string
  abilities?: string[]
  relationships: Relationship[]
  arc?: string
}

export interface Faction {
  id: string
  name: string
  type: string
  description: string
  members: string[]
  goals: string[]
}

export interface Item {
  id: string
  name: string
  type: string
  description: string
  powers?: string[]
}

export interface Relationship {
  from: string
  to: string
  type: 'friend' | 'enemy' | 'family' | 'mentor' | 'ally' | 'rival' | 'other'
  description: string
}

// 章节类型
export interface Chapter {
  id: number
  project_id: number
  chapter_number: number
  title: string
  content: string
  status: 'draft' | 'reviewing' | 'published' | 'archived'
  word_count: number
  outline?: string
  created_at: string
  updated_at: string
}

export interface BeatSheet {
  id: string
  chapterId: string
  beat: string
  description: string
  content: string
  order: number
}

// 伏笔类型
export type ForeshadowType =
  | 'chekhovs_gun'
  | 'grass_snake'
  | 'suspense'
  | 'setup'
  | 'foreshadowing'
  | 'callback'
  | 'payoff'
  | 'twist'
  | 'hook'
  | 'echo'

export interface Foreshadow {
  id: number
  project_id: number
  type: ForeshadowType
  title: string
  description: string
  chapter_id?: number
  chapter_number: number
  status: 'setup' | 'callback' | 'paid_off' | 'forgotten'
  related_foreshadows?: number[]
  created_at: string
  updated_at: string
}

// Agent类型
export interface Agent {
  id: number
  name: string
  role: string
  status: 'idle' | 'active' | 'completed' | 'error'
  last_activity?: string
  tasks_completed: number
  description?: string
  system_prompt?: string
  enabled?: boolean
}



export interface AgentTask {
  id: number
  agent_id: number
  project_id: number
  type: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  input: any
  output?: any
  error?: string
  progress: number
  created_at: string
  completed_at?: string
}

// 知识库类型
export interface KnowledgeEntry {
  id: number
  project_id: number
  type: 'character' | 'plot' | 'setting' | 'system' | 'other'
  title: string
  content: string
  tags: string[]
  source_chapter_id?: number
  embedding?: number[]
  created_at: string
  updated_at: string
}

// 提示词类型
export type PromptCategory =
  | 'worldbuilding' | 'character' | 'scene' | 'dialogue' | 'plot'
  | 'polish' | 'opening' | 'chapter' | 'ending' | 'other'

export interface Prompt {
  id: number
  name: string
  category: PromptCategory
  template: string
  variables: PromptVariable[]
  tags: string[]
  usage_count: number
  enabled: boolean
  created_at: string
  updated_at: string
}

export interface PromptVariable {
  name: string
  type: 'text' | 'number' | 'select' | 'textarea'
  defaultValue?: string
  required: boolean
  options?: string[]
}

// AI模型类型
export interface AIModel {
  id: string
  name: string
  provider: string
  description: string
  is_custom: boolean
}

export interface AIProvider {
  id: string
  name: string
  configured: boolean
}

export interface ApiKeyInfo {
  id: string
  name: string
  configured: boolean
  masked_key: string
  connection_status: 'connected' | 'disconnected' | 'unconfigured' | 'testing'
  active_agents: string[]
}

export interface ApiKeyUpdateRequest {
  openai_api_key?: string | null
  anthropic_api_key?: string | null
  deepseek_api_key?: string | null
  gemini_api_key?: string | null
  // 自定义 Provider
  custom_api_key?: string | null
  custom_api_base?: string | null
  custom_model_id?: string | null
  custom_provider_name?: string | null
}

// 设置类型
export interface UserSettings {
  theme: 'light' | 'dark' | 'auto'
  language: string
  font_size: number
  auto_save: boolean
  auto_save_interval: number
  default_model: string
  custom_model_input: string   // 用户手动输入的自定义模型ID
  budget_limit: number
  enable_cache: boolean
  enable_semantic_cache: boolean
}
