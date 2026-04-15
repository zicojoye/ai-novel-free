import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import type { Project, Chapter, WorldBuilding, Foreshadow } from '@/types'

interface ProjectState {
  // 状态
  currentProject: Project | null
  projects: Project[]
  chapters: Chapter[]
  worldBuilding: WorldBuilding | null
  foreshadows: Foreshadow[]
  isLoading: boolean

  // 项目操作
  setProjects: (projects: Project[]) => void
  setCurrentProject: (project: Project | null) => void
  addProject: (project: Project) => void
  updateProject: (id: number, updates: Partial<Project>) => void
  removeProject: (id: number) => void

  // 章节操作
  setChapters: (chapters: Chapter[]) => void
  addChapter: (chapter: Chapter) => void
  updateChapter: (id: number, updates: Partial<Chapter>) => void
  removeChapter: (id: number) => void

  // 世界观操作
  setWorldBuilding: (worldBuilding: WorldBuilding | null) => void
  updateWorldBuilding: (updates: Partial<WorldBuilding>) => void

  // 伏笔操作
  setForeshadows: (foreshadows: Foreshadow[]) => void
  addForeshadow: (foreshadow: Foreshadow) => void
  updateForeshadow: (id: number, updates: Partial<Foreshadow>) => void
  removeForeshadow: (id: number) => void

  // 加载状态
  setLoading: (isLoading: boolean) => void
}

export const useProjectStore = create<ProjectState>()(
  devtools(
    persist(
      (set) => ({
        // 初始状态
        currentProject: null,
        projects: [],
        chapters: [],
        worldBuilding: null,
        foreshadows: [],
        isLoading: false,

        // 项目操作
        setProjects: (projects) => set({ projects }),
        setCurrentProject: (project) => set({ currentProject: project }),
        addProject: (project) => set((state) => ({ projects: [...state.projects, project] })),
        updateProject: (id, updates) =>
          set((state) => ({
            projects: state.projects.map((p) => (p.id === id ? { ...p, ...updates } : p)),
            currentProject: state.currentProject?.id === id ? { ...state.currentProject, ...updates } : state.currentProject,
          })),
        removeProject: (id) =>
          set((state) => ({
            projects: state.projects.filter((p) => p.id !== id),
            currentProject: state.currentProject?.id === id ? null : state.currentProject,
          })),

        // 章节操作
        setChapters: (chapters) => set({ chapters }),
        addChapter: (chapter) => set((state) => ({ chapters: [...state.chapters, chapter] })),
        updateChapter: (id, updates) =>
          set((state) => ({
            chapters: state.chapters.map((c) => (c.id === id ? { ...c, ...updates } : c)),
          })),
        removeChapter: (id) =>
          set((state) => ({
            chapters: state.chapters.filter((c) => c.id !== id),
          })),

        // 世界观操作
        setWorldBuilding: (worldBuilding) => set({ worldBuilding }),
        updateWorldBuilding: (updates) =>
          set((state) => ({
            worldBuilding: state.worldBuilding ? { ...state.worldBuilding, ...updates } : null,
          })),

        // 伏笔操作
        setForeshadows: (foreshadows) => set({ foreshadows }),
        addForeshadow: (foreshadow) =>
          set((state) => ({ foreshadows: [...state.foreshadows, foreshadow] })),
        updateForeshadow: (id, updates) =>
          set((state) => ({
            foreshadows: state.foreshadows.map((f) => (f.id === id ? { ...f, ...updates } : f)),
          })),
        removeForeshadow: (id) =>
          set((state) => ({
            foreshadows: state.foreshadows.filter((f) => f.id !== id),
          })),

        // 加载状态
        setLoading: (isLoading) => set({ isLoading }),
      }),
      {
        name: 'project-storage',
        partialize: (state) => ({
          currentProject: state.currentProject,
          projects: state.projects,
        }),
      }
    )
  )
)
