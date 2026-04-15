import api from '@/lib/api'
import type {
  ApiResponse,
  Prompt,
} from '@/types'

export const promptService = {
  // 获取提示词列表
  async getPrompts(category?: string): Promise<ApiResponse<Prompt[]>> {
    const params = category ? { category } : {}
    return api.get('/prompts', { params })
  },

  // 获取提示词详情
  async getPrompt(id: string): Promise<ApiResponse<Prompt>> {
    return api.get(`/prompts/${id}`)
  },

  // 创建提示词
  async createPrompt(data: Partial<Prompt>): Promise<ApiResponse<Prompt>> {
    return api.post('/prompts', data)
  },

  // 更新提示词
  async updatePrompt(id: string, data: Partial<Prompt>): Promise<ApiResponse<Prompt>> {
    return api.put(`/prompts/${id}`, data)
  },

  // 删除提示词
  async deletePrompt(id: string): Promise<ApiResponse<void>> {
    return api.delete(`/prompts/${id}`)
  },
}
