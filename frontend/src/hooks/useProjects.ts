import { useQuery, useMutation, useQueryClient, UseQueryOptions } from '@tanstack/react-query'
import { projectService } from '@/services/projectService'
import type { Project, PaginationParams, ApiResponse } from '@/types'

// 查询键工厂
export const projectKeys = {
  all: ['projects'] as const,
  lists: () => [...projectKeys.all, 'list'] as const,
  list: (params: PaginationParams) => [...projectKeys.lists(), params] as const,
  details: () => [...projectKeys.all, 'detail'] as const,
  detail: (id: number) => [...projectKeys.details(), id] as const,
}

// 获取所有项目
export function useProjects(params?: PaginationParams, options?: Omit<UseQueryOptions<ApiResponse<Project[]>>, 'queryKey' | 'queryFn'>) {
  return useQuery({
    queryKey: projectKeys.list(params || { page: 1, pageSize: 20 }),
    queryFn: () => projectService.getProjects(params),
    ...options,
  })
}

// 获取项目详情
export function useProject(id: number, options?: Omit<UseQueryOptions<ApiResponse<Project>>, 'queryKey' | 'queryFn'>) {
  return useQuery({
    queryKey: projectKeys.detail(id),
    queryFn: () => projectService.getProject(id),
    enabled: !!id,
    ...options,
  })
}

// 创建项目
export function useCreateProject() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: projectService.createProject,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: projectKeys.lists() })
    },
  })
}

// 更新项目
export function useUpdateProject() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Project> }) =>
      projectService.updateProject(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: projectKeys.lists() })
      queryClient.invalidateQueries({ queryKey: projectKeys.detail(id) })
    },
  })
}

// 删除项目
export function useDeleteProject() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: projectService.deleteProject,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: projectKeys.lists() })
    },
  })
}
