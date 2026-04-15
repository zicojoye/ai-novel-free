import { useQuery, useMutation, useQueryClient, UseQueryOptions } from '@tanstack/react-query'
import { chapterService } from '@/services/chapterService'
import type { Chapter, PaginationParams, ApiResponse } from '@/types'

// 查询键工厂
export const chapterKeys = {
  all: ['chapters'] as const,
  lists: () => [...chapterKeys.all, 'list'] as const,
  list: (projectId: number, params?: PaginationParams) =>
    [...chapterKeys.lists(), projectId, params] as const,
  details: () => [...chapterKeys.all, 'detail'] as const,
  detail: (id: number) => [...chapterKeys.details(), id] as const,
}

// 获取章节列表
export function useChapters(
  projectId: number,
  params?: PaginationParams,
  options?: Omit<UseQueryOptions<ApiResponse<Chapter[]>>, 'queryKey' | 'queryFn'>
) {
  return useQuery({
    queryKey: chapterKeys.list(projectId, params),
    queryFn: () => chapterService.getChapters(projectId, params),
    enabled: !!projectId,
    ...options,
  })
}

// 获取章节详情
export function useChapter(
  id: number,
  options?: Omit<UseQueryOptions<ApiResponse<Chapter>>, 'queryKey' | 'queryFn'>
) {
  return useQuery({
    queryKey: chapterKeys.detail(id),
    queryFn: () => chapterService.getChapter(id),
    enabled: !!id,
    ...options,
  })
}

// 创建章节
export function useCreateChapter() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: chapterService.createChapter,
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: chapterKeys.list(variables.project_id) })
    },
  })
}

// 更新章节
export function useUpdateChapter() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Chapter> }) =>
      chapterService.updateChapter(id, data),
    onSuccess: (_, { id, data }) => {
      queryClient.invalidateQueries({ queryKey: chapterKeys.details() })
      queryClient.invalidateQueries({ queryKey: chapterKeys.detail(id) })
      if (data.project_id) {
        queryClient.invalidateQueries({ queryKey: chapterKeys.list(data.project_id) })
      }
    },
  })
}

// 删除章节
export function useDeleteChapter() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: chapterService.deleteChapter,
    onSuccess: (_, id) => {
      // 无法直接知道project_id，所以清空所有列表
      queryClient.invalidateQueries({ queryKey: chapterKeys.lists() })
    },
  })
}

// 自动保存章节
export function useAutoSaveChapter() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Chapter> }) =>
      chapterService.updateChapter(id, data),
    onSuccess: (_, { id, data }) => {
      queryClient.setQueryData(chapterKeys.detail(id), (old: any) => {
        if (old?.data) {
          return {
            ...old,
            data: { ...old.data, ...data },
          }
        }
        return old
      })
    },
  })
}
