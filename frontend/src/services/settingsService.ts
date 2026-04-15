import api from '@/lib/api'
import type { ApiResponse, UserSettings, AIModel, AIProvider, ApiKeyInfo, ApiKeyUpdateRequest } from '@/types'

export const settingsService = {
  // 获取用户设置
  async getSettings(): Promise<ApiResponse<UserSettings>> {
    return api.get('/settings')
  },

  // 更新用户设置
  async updateSettings(data: Partial<UserSettings>): Promise<ApiResponse<UserSettings>> {
    return api.put('/settings', data)
  },

  // 重置设置
  async resetSettings(): Promise<ApiResponse<UserSettings>> {
    return api.post('/settings/reset')
  },

  // 导出数据
  async exportData(): Promise<Blob> {
    return api.get('/settings/export', { responseType: 'blob' })
  },

  // 导入数据
  async importData(file: File): Promise<ApiResponse<void>> {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/settings/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  // 获取可用模型列表
  async getModels(): Promise<{ models: AIModel[]; default_model: string }> {
    return api.get('/models')
  },

  // 获取已配置的 provider 列表
  async getProviders(): Promise<{ providers: AIProvider[] }> {
    return api.get('/models/providers')
  },

  // 获取 API Key 详情（脱敏值 + 连接状态 + 使用中的 Agent）
  async getApiKeys(): Promise<{ keys: ApiKeyInfo[] }> {
    return api.get('/models/keys')
  },

  // 更新 API Key（写入后端 .env 并热更新）
  async updateApiKeys(data: ApiKeyUpdateRequest): Promise<{ success: boolean; updated: string[] }> {
    return api.put('/models/keys', data)
  },

  // 测试指定 provider 的连通性
  async testApiKey(providerId: string): Promise<{ provider_id: string; status: string; message: string }> {
    return api.post(`/models/keys/test/${providerId}`)
  },
}

