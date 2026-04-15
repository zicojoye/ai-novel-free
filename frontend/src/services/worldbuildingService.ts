import api from '@/lib/api'
import type {
  ApiResponse,
  WorldBuilding,
} from '@/types'

export const worldbuildingService = {
  // 获取世界观
  async getWorldBuilding(projectId: string): Promise<ApiResponse<WorldBuilding>> {
    return api.get(`/worldbuilding/${projectId}`)
  },

  // 创建世界观
  async createWorldBuilding(data: Partial<WorldBuilding>): Promise<ApiResponse<WorldBuilding>> {
    return api.post('/worldbuilding', data)
  },

  // 更新世界观
  async updateWorldBuilding(projectId: string, data: Partial<WorldBuilding>): Promise<ApiResponse<WorldBuilding>> {
    return api.put(`/worldbuilding/${projectId}`, data)
  },

  // 删除世界观
  async deleteWorldBuilding(projectId: string): Promise<ApiResponse<void>> {
    return api.delete(`/worldbuilding/${projectId}`)
  },
}
