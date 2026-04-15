import api from '@/lib/api'
import type {
  ApiResponse,
  KnowledgeEntry,
  PaginationParams,
} from '@/types'

export const knowledgeService = {
  // 获取知识列表
  async getKnowledgeEntries(projectId: string, params?: PaginationParams): Promise<ApiResponse<KnowledgeEntry[]>> {
    return api.get(`/knowledge?project_id=${projectId}`, { params })
  },

  // 获取知识详情
  async getKnowledgeEntry(id: string): Promise<ApiResponse<KnowledgeEntry>> {
    return api.get(`/knowledge/${id}`)
  },

  // 创建知识
  async createKnowledge(data: Partial<KnowledgeEntry>): Promise<ApiResponse<KnowledgeEntry>> {
    return api.post('/knowledge', data)
  },

  // 更新知识
  async updateKnowledge(id: string, data: Partial<KnowledgeEntry>): Promise<ApiResponse<KnowledgeEntry>> {
    return api.put(`/knowledge/${id}`, data)
  },

  // 删除知识
  async deleteKnowledge(id: string): Promise<ApiResponse<void>> {
    return api.delete(`/knowledge/${id}`)
  },

  // 搜索知识
  async searchKnowledge(projectId: string, query: string): Promise<ApiResponse<KnowledgeEntry[]>> {
    return api.post('/knowledge/search', { project_id: projectId, query })
  },
}
