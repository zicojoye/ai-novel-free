import api from '@/lib/api'
import type {
  ApiResponse,
  Foreshadow,
  PaginationParams,
} from '@/types'

export const foreshadowService = {
  // 获取伏笔列表
  async getForeshadows(projectId: string, params?: PaginationParams): Promise<ApiResponse<Foreshadow[]>> {
    return api.get(`/foreshadows?project_id=${projectId}`, { params })
  },

  // 获取伏笔详情
  async getForeshadow(id: string): Promise<ApiResponse<Foreshadow>> {
    return api.get(`/foreshadows/${id}`)
  },

  // 创建伏笔
  async createForeshadow(data: Partial<Foreshadow>): Promise<ApiResponse<Foreshadow>> {
    return api.post('/foreshadows', data)
  },

  // 更新伏笔
  async updateForeshadow(id: string, data: Partial<Foreshadow>): Promise<ApiResponse<Foreshadow>> {
    return api.put(`/foreshadows/${id}`, data)
  },

  // 删除伏笔
  async deleteForeshadow(id: string): Promise<ApiResponse<void>> {
    return api.delete(`/foreshadows/${id}`)
  },

  // 关联伏笔
  async linkForeshadows(id: string, relatedIds: number[]): Promise<ApiResponse<void>> {
    return api.post(`/foreshadows/${id}/link`, { related_foreshadows: relatedIds })
  },

  // 按类型获取伏笔
  async getForeshadowsByType(projectId: string, type: string): Promise<ApiResponse<Foreshadow[]>> {
    return api.get(`/foreshadows?project_id=${projectId}&type=${type}`)
  },
}
