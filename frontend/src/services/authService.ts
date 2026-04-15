import api from '@/lib/api'
import type { ApiResponse } from '@/types'

export interface User {
  id: string
  email: string
  username: string
  created_at: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  username: string
  password: string
}

export const authService = {
  // 登录
  async login(credentials: LoginCredentials): Promise<ApiResponse<{ token: string; user: User }>> {
    return api.post('/auth/login', credentials)
  },

  // 注册
  async register(data: RegisterData): Promise<ApiResponse<{ token: string; user: User }>> {
    return api.post('/auth/register', data)
  },

  // 登出
  async logout(): Promise<ApiResponse<void>> {
    return api.post('/auth/logout')
  },

  // 刷新令牌
  async refreshToken(): Promise<ApiResponse<{ token: string }>> {
    return api.post('/auth/refresh')
  },

  // 获取当前用户
  async getCurrentUser(): Promise<ApiResponse<User>> {
    return api.get('/auth/me')
  },

  // 更新用户资料
  async updateProfile(data: Partial<User>): Promise<ApiResponse<User>> {
    return api.put('/auth/profile', data)
  },
}
