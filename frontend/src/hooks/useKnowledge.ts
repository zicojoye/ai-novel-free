import { useQuery, useMutation, useQueryClient, UseQueryOptions } from '@tanstack/react-query'
import { knowledgeService } from '@/services/knowledgeService'
import type { KnowledgeEntry, PaginationParams, ApiResponse } from '@/types'

// 查询键工厂
export const knowledgeKeys = {
  all: ['knowledge'] as const,
  lists: () => [...knowledgeKeys.all, 'list'] as const,
  list: (projectId: number, params?: PaginationParams) =>
    [...knowledgeKeys.lists(), projectId, params] as const,
  details: () => [...knowledgeKeys.all, 'detail'] as const,
  detail: (id: number) => [...knowledgeKeys.details(), id] as const,
  search: (projectId: number, query: string) =>
    [...knowledgeKeys.all, projectId, 'search', query] as const,
}

// 获取知识库列表
export function useKnowledgeEntries(
  projectId: number,
  params?: PaginationParams,
  options?: Omit<UseQueryOptions<ApiResponse<KnowledgeEntry[]>>, 'queryKey' | 'queryFn'>
) {
  return useQuery({
    queryKey: knowledgeKeys.list(projectId, params),
    queryFn: () => knowledgeService.getKnowledgeEntries(projectId, params),
    enabled: !!projectId,
    ...options,
  })
}

// 获取知识条目详情
export function useKnowledgeEntry(
  id: number,
  options?: Omit<UseQueryOptions<ApiResponse<KnowledgeEntry>>, 'queryKey' | 'queryFn'>
) {
  return useQuery({
    queryKey: knowledgeKeys.detail(id),
    queryFn: () => knowledgeService.getKnowledgeEntry(id),
    enabled: !!id,
    ...options,
  })
}

// 搜索知识库
export function useSearchKnowledge(
  projectId: number,
  query: string,
  options?: Omit<UseQueryOptions<ApiResponse<KnowledgeEntry[]>>, 'queryKey' | 'queryFn'>
) {
  return useQuery({
    queryKey: knowledgeKeys.search(projectId, query),
    queryFn: () => knowledgeService.searchKnowledge(projectId, query),
    enabled: !!projectId && query.length > 0,
    ...options,
  })
}

// 创建知识条目
export function useCreateKnowledgeEntry() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: knowledgeService.createKnowledgeEntry,
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: knowledgeKeys.lists() })
      if (variables.project_id) {
        queryClient.invalidateQueries({
          queryKey: knowledgeKeys.list(variables.project_id),
        })
      }
    },
  })
}

// 更新知识条目
export function useUpdateKnowledgeEntry() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<KnowledgeEntry> }) =>
      knowledgeService.updateKnowledgeEntry(id, data),
    onSuccess: (_, { id, data }) => {
      queryClient.invalidateQueries({ queryKey: knowledgeKeys.details() })
      queryClient.invalidateQueries({ queryKey: knowledgeKeys.detail(id) })
      if (data.project_id) {
        queryClient.invalidateQueries({
          queryKey: knowledgeKeys.list(data.project_id),
        })
      }
    },
  })
}

// 删除知识条目
export function useDeleteKnowledgeEntry() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: knowledgeService.deleteKnowledgeEntry,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: knowledgeKeys.lists() })
    },
  })
}
