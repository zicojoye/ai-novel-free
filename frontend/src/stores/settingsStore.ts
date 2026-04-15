import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import type { UserSettings, AIModel, AIProvider, ApiKeyInfo, ApiKeyUpdateRequest } from '@/types'
import { settingsService } from '@/services/settingsService'

interface SettingsState {
  settings: UserSettings
  models: AIModel[]
  providers: AIProvider[]
  modelsLoading: boolean
  apiKeys: ApiKeyInfo[]
  apiKeysLoading: boolean

  updateSettings: (updates: Partial<UserSettings>) => void
  resetSettings: () => void
  loadModels: () => Promise<void>
  loadApiKeys: () => Promise<void>
  saveApiKeys: (data: ApiKeyUpdateRequest) => Promise<boolean>
}

const defaultSettings: UserSettings = {
  theme: 'auto',
  language: 'zh-CN',
  font_size: 14,
  auto_save: true,
  auto_save_interval: 60000,
  default_model: 'gpt-4o',
  custom_model_input: '',
  budget_limit: 10,
  enable_cache: true,
  enable_semantic_cache: true,
}

export const useSettingsStore = create<SettingsState>()(
  devtools(
    persist(
      (set) => ({
        settings: defaultSettings,
        models: [],
        providers: [],
        modelsLoading: false,
        apiKeys: [],
        apiKeysLoading: false,

        updateSettings: (updates) =>
          set((state) => ({
            settings: { ...state.settings, ...updates },
          })),

        resetSettings: () => set({ settings: defaultSettings }),

        loadModels: async () => {
          set({ modelsLoading: true })
          try {
            const [modelsRes, providersRes] = await Promise.all([
              settingsService.getModels(),
              settingsService.getProviders(),
            ])
            set({
              models: modelsRes.models ?? [],
              providers: providersRes.providers ?? [],
            })
          } catch {
            // 后端未启动时静默降级，保持空列表
          } finally {
            set({ modelsLoading: false })
          }
        },

        loadApiKeys: async () => {
          set({ apiKeysLoading: true })
          try {
            const res = await settingsService.getApiKeys()
            set({ apiKeys: res.keys ?? [] })
          } catch {
            // 静默降级
          } finally {
            set({ apiKeysLoading: false })
          }
        },

        saveApiKeys: async (data: ApiKeyUpdateRequest) => {
          try {
            await settingsService.updateApiKeys(data)
            const res = await settingsService.getApiKeys()
            set({ apiKeys: res.keys ?? [] })
            return true
          } catch {
            return false
          }
        },
      }),
      { name: 'settings-storage' }
    )
  )
)
