import { useQuery, useMutation, useQueryClient, UseQueryOptions } from '@tanstack/react-query'
import { worldbuildingService } from '@/services/worldbuildingService'
import type { WorldBuilding, ApiResponse } from '@/types'

// 查询键工厂
export const worldbuildingKeys = {
  all: ['worldbuilding'] as const,
  byProject: (projectId: number) => [...worldbuildingKeys.all, projectId] as const,
}

// 获取项目世界观
export function useWorldBuilding(
  projectId: number,
  options?: Omit<UseQueryOptions<ApiResponse<WorldBuilding>>, 'queryKey' | 'queryFn'>
) {
  return useQuery({
    queryKey: worldbuildingKeys.byProject(projectId),
    queryFn: () => worldbuildingService.getWorldBuilding(projectId),
    enabled: !!projectId,
    ...options,
  })
}

// 创建世界观
export function useCreateWorldBuilding() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: worldbuildingService.createWorldBuilding,
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({
        queryKey: worldbuildingKeys.byProject(variables.project_id),
      })
    },
  })
}

// 更新世界观
export function useUpdateWorldBuilding() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<WorldBuilding> }) =>
      worldbuildingService.updateWorldBuilding(id, data),
    onSuccess: (_, { id, data }) => {
      queryClient.invalidateQueries({
        queryKey: worldbuildingKeys.byProject(data.project_id || 0),
      })
    },
  })
}
