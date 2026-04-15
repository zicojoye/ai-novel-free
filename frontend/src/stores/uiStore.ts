import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

export interface Toast {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message?: string
  duration?: number
}

interface UIState {
  // 状态
  theme: 'light' | 'dark' | 'auto'
  sidebarOpen: boolean
  modals: Record<string, boolean>
  toasts: Toast[]
  loadingStates: Record<string, boolean>

  // 操作
  setTheme: (theme: 'light' | 'dark' | 'auto') => void
  setSidebarOpen: (open: boolean) => void
  toggleModal: (modalId: string, open?: boolean) => void
  showToast: (toast: Omit<Toast, 'id'>) => void
  removeToast: (id: string) => void
  setLoading: (key: string, loading: boolean) => void
  clearToasts: () => void
}

export const useUIStore = create<UIState>()(
  devtools(
    persist(
      (set) => ({
        // 初始状态
        theme: 'auto',
        sidebarOpen: true,
        modals: {},
        toasts: [],
        loadingStates: {},

        // 操作
        setTheme: (theme) => set({ theme }),
        setSidebarOpen: (open) => set({ sidebarOpen: open }),
        toggleModal: (modalId, open) =>
          set((state) => ({
            modals: {
              ...state.modals,
              [modalId]: open !== undefined ? open : !state.modals[modalId],
            },
          })),
        showToast: (toast) =>
          set((state) => ({
            toasts: [
              ...state.toasts,
              { ...toast, id: Date.now().toString() + Math.random() },
            ],
          })),
        removeToast: (id) =>
          set((state) => ({
            toasts: state.toasts.filter((t) => t.id !== id),
          })),
        setLoading: (key, loading) =>
          set((state) => ({
            loadingStates: { ...state.loadingStates, [key]: loading },
          })),
        clearToasts: () => set({ toasts: [] }),
      }),
      {
        name: 'ui-storage',
        partialize: (state) => ({
          theme: state.theme,
          sidebarOpen: state.sidebarOpen,
        }),
      }
    )
  )
)
