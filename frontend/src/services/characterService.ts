import api from '@/lib/api'
import type {
  ApiResponse,
  Character,
  PaginationParams,
} from '@/types'

export const characterService = {
  // 获取角色列表
  async getCharacters(projectId: string, params?: PaginationParams): Promise<ApiResponse<Character[]>> {
    return api.get(`/characters?project_id=${projectId}`, { params })
  },

  // 获取角色详情
  async getCharacter(id: string): Promise<ApiResponse<Character>> {
    return api.get(`/characters/${id}`)
  },

  // 创建角色
  async createCharacter(data: Partial<Character>): Promise<ApiResponse<Character>> {
    return api.post('/characters', data)
  },

  // 更新角色
  async updateCharacter(id: string, data: Partial<Character>): Promise<ApiResponse<Character>> {
    return api.put(`/characters/${id}`, data)
  },

  // 删除角色
  async deleteCharacter(id: string): Promise<ApiResponse<void>> {
    return api.delete(`/characters/${id}`)
  },

  // 更新角色关系
  async updateCharacterRelations(id: string, relations: any[]): Promise<ApiResponse<void>> {
    return api.put(`/characters/${id}/relations`, { relationships: relations })
  },
}
