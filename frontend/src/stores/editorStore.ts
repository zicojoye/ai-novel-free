import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import type { Chapter } from '@/types'

interface EditorState {
  // 状态
  currentChapter: Chapter | null
  draftContent: string
  wordCount: number
  autoSaveEnabled: boolean
  lastSavedAt: string | null
  autoSaveInterval: number

  // 操作
  setCurrentChapter: (chapter: Chapter | null) => void
  setDraftContent: (content: string) => void
  updateWordCount: (count: number) => void
  setAutoSaveEnabled: (enabled: boolean) => void
  setLastSavedAt: (time: string | null) => void
  resetEditor: () => void
}

export const useEditorStore = create<EditorState>()(
  devtools(
    persist(
      (set) => ({
        // 初始状态
        currentChapter: null,
        draftContent: '',
        wordCount: 0,
        autoSaveEnabled: true,
        lastSavedAt: null,
        autoSaveInterval: 30000,

        // 操作
        setCurrentChapter: (chapter) => set({ currentChapter: chapter }),
        setDraftContent: (content) => set({ draftContent: content }),
        updateWordCount: (count) => set({ wordCount: count }),
        setAutoSaveEnabled: (enabled) => set({ autoSaveEnabled: enabled }),
        setLastSavedAt: (time) => set({ lastSavedAt: time }),
        resetEditor: () =>
          set({
            currentChapter: null,
            draftContent: '',
            wordCount: 0,
            lastSavedAt: null,
          }),
      }),
      {
        name: 'editor-storage',
        partialize: (state) => ({
          autoSaveEnabled: state.autoSaveEnabled,
          autoSaveInterval: state.autoSaveInterval,
        }),
      }
    )
  )
)
