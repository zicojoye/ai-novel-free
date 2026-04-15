import api from '@/lib/api'
import type {
  ApiResponse,
  Chapter,
  PaginationParams,
} from '@/types'

export const chapterService = {
  // 获取章节列表
  async getChapters(projectId: string, params?: PaginationParams): Promise<ApiResponse<Chapter[]>> {
    return api.get(`/chapters?project_id=${projectId}`, { params })
  },

  // 获取章节详情
  async getChapter(id: string): Promise<ApiResponse<Chapter>> {
    return api.get(`/chapters/${id}`)
  },

  // 创建章节
  async createChapter(data: Partial<Chapter>): Promise<ApiResponse<Chapter>> {
    return api.post('/chapters', data)
  },

  // 更新章节
  async updateChapter(id: string, data: Partial<Chapter>): Promise<ApiResponse<Chapter>> {
    return api.put(`/chapters/${id}`, data)
  },

  // 删除章节
  async deleteChapter(id: string): Promise<ApiResponse<void>> {
    return api.delete(`/chapters/${id}`)
  },
}
