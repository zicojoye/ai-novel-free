import api from '@/lib/api'
import type { ApiResponse } from '@/types'

export interface AIWorldviewRequest {
  project_id: number
  genre: string
  core_concept: string
}

export interface AIChapterRequest {
  project_id: number
  chapter_number: number
  outline: string
  previous_chapter?: string
}

export interface AICharacterRequest {
  project_id: number
  name: string
  role: string
}

export interface AIPolishRequest {
  text: string
  style?: string
}

export const aiService = {
  // 生成世界观
  async generateWorldview(data: AIWorldviewRequest): Promise<ApiResponse<any>> {
    return api.post('/ai/worldview', data)
  },

  // 生成章节
  async generateChapter(data: AIChapterRequest): Promise<ApiResponse<{ content: string }>> {
    return api.post('/ai/chapter', data)
  },

  // 生成角色
  async generateCharacter(data: AICharacterRequest): Promise<ApiResponse<any>> {
    return api.post('/ai/character', data)
  },

  // 润色文本
  async polishText(data: AIPolishRequest): Promise<ApiResponse<{ text: string }>> {
    return api.post('/ai/polish', data)
  },

  // 提取知识
  async extractKnowledge(chapterId: number): Promise<ApiResponse<any[]>> {
    return api.post(`/ai/extract-knowledge/${chapterId}`)
  },

  // 生成对话
  async generateDialogue(data: {
    characters: string[]
    topic: string
    context?: string
  }): Promise<ApiResponse<{ dialogue: string }>> {
    return api.post('/ai/dialogue', data)
  },

  // 生成场景
  async generateScene(data: {
    location: string
    atmosphere?: string
    characters?: string[]
  }): Promise<ApiResponse<{ description: string }>> {
    return api.post('/ai/scene', data)
  },
}
