import api from '@/lib/api'
import type {
  ApiResponse,
  Project,
  PaginatedResponse,
  PaginationParams,
} from '@/types'

export const projectService = {
  // 获取项目列表
  async getProjects(params?: PaginationParams): Promise<ApiResponse<PaginatedResponse<Project>>> {
    return api.get('/projects', { params })
  },

  // 获取项目详情
  async getProject(id: string): Promise<ApiResponse<Project>> {
    return api.get(`/projects/${id}`)
  },

  // 创建项目
  async createProject(data: Partial<Project>): Promise<ApiResponse<Project>> {
    return api.post('/projects', data)
  },

  // 更新项目
  async updateProject(id: string, data: Partial<Project>): Promise<ApiResponse<Project>> {
    return api.put(`/projects/${id}`, data)
  },

  // 删除项目
  async deleteProject(id: string): Promise<ApiResponse<void>> {
    return api.delete(`/projects/${id}`)
  },
}
