import { useQuery, useMutation, useQueryClient, UseQueryOptions } from '@tanstack/react-query'
import { foreshadowService } from '@/services/foreshadowService'
import type { Foreshadow, PaginationParams, ApiResponse } from '@/types'

// 查询键工厂
export const foreshadowKeys = {
  all: ['foreshadows'] as const,
  lists: () => [...foreshadowKeys.all, 'list'] as const,
  list: (projectId: number, params?: PaginationParams) =>
    [...foreshadowKeys.lists(), projectId, params] as const,
  details: () => [...foreshadowKeys.all, 'detail'] as const,
  detail: (id: number) => [...foreshadowKeys.details(), id] as const,
  byType: (projectId: number, type: string) =>
    [...foreshadowKeys.all, projectId, 'type', type] as const,
}

// 获取伏笔列表
export function useForeshadows(
  projectId: number,
  params?: PaginationParams,
  options?: Omit<UseQueryOptions<ApiResponse<Foreshadow[]>>, 'queryKey' | 'queryFn'>
) {
  return useQuery({
    queryKey: foreshadowKeys.list(projectId, params),
    queryFn: () => foreshadowService.getForeshadows(projectId, params),
    enabled: !!projectId,
    ...options,
  })
}

// 获取伏笔详情
export function useForeshadow(
  id: number,
  options?: Omit<UseQueryOptions<ApiResponse<Foreshadow>>, 'queryKey' | 'queryFn'>
) {
  return useQuery({
    queryKey: foreshadowKeys.detail(id),
    queryFn: () => foreshadowService.getForeshadow(id),
    enabled: !!id,
    ...options,
  })
}

// 按类型获取伏笔
export function useForeshadowsByType(
  projectId: number,
  type: string,
  options?: Omit<UseQueryOptions<ApiResponse<Foreshadow[]>>, 'queryKey' | 'queryFn'>
) {
  return useQuery({
    queryKey: foreshadowKeys.byType(projectId, type),
    queryFn: () => foreshadowService.getForeshadowsByType(projectId, type),
    enabled: !!projectId && !!type,
    ...options,
  })
}

// 创建伏笔
export function useCreateForeshadow() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: foreshadowService.createForeshadow,
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: foreshadowKeys.lists() })
      if (variables.project_id) {
        queryClient.invalidateQueries({
          queryKey: foreshadowKeys.list(variables.project_id),
        })
      }
    },
  })
}

// 更新伏笔
export function useUpdateForeshadow() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Foreshadow> }) =>
      foreshadowService.updateForeshadow(id, data),
    onSuccess: (_, { id, data }) => {
      queryClient.invalidateQueries({ queryKey: foreshadowKeys.details() })
      queryClient.invalidateQueries({ queryKey: foreshadowKeys.detail(id) })
      if (data.project_id) {
        queryClient.invalidateQueries({
          queryKey: foreshadowKeys.list(data.project_id),
        })
      }
    },
  })
}

// 删除伏笔
export function useDeleteForeshadow() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: foreshadowService.deleteForeshadow,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: foreshadowKeys.lists() })
    },
  })
}

// 关联伏笔
export function useLinkForeshadows() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, relatedIds }: { id: number; relatedIds: number[] }) =>
      foreshadowService.linkForeshadows(id, relatedIds),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: foreshadowKeys.detail(id) })
      queryClient.invalidateQueries({ queryKey: foreshadowKeys.details() })
    },
  })
}
