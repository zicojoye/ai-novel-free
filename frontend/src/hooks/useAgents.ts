import { useQuery, useMutation, useQueryClient, UseQueryOptions } from '@tanstack/react-query'
import { agentService } from '@/services/agentService'
import type { Agent, AgentTask, ApiResponse } from '@/types'

// 查询键工厂
export const agentKeys = {
  all: ['agents'] as const,
  lists: () => [...agentKeys.all, 'list'] as const,
  details: () => [...agentKeys.all, 'detail'] as const,
  detail: (id: number) => [...agentKeys.details(), id] as const,
  tasks: (agentId: number) => [...agentKeys.all, agentId, 'tasks'] as const,
  task: (taskId: number) => [...agentKeys.all, 'task', taskId] as const,
}

// 获取所有Agent
export function useAgents(options?: Omit<UseQueryOptions<ApiResponse<Agent[]>>, 'queryKey' | 'queryFn'>) {
  return useQuery({
    queryKey: agentKeys.lists(),
    queryFn: agentService.getAgents,
    ...options,
  })
}

// 获取Agent详情
export function useAgent(
  id: number,
  options?: Omit<UseQueryOptions<ApiResponse<Agent>>, 'queryKey' | 'queryFn'>
) {
  return useQuery({
    queryKey: agentKeys.detail(id),
    queryFn: () => agentService.getAgent(id),
    enabled: !!id,
    ...options,
  })
}

// 获取Agent任务列表
export function useAgentTasks(
  agentId: number,
  options?: Omit<UseQueryOptions<ApiResponse<AgentTask[]>>, 'queryKey' | 'queryFn'>
) {
  return useQuery({
    queryKey: agentKeys.tasks(agentId),
    queryFn: () => agentService.getAgentTasks(agentId),
    enabled: !!agentId,
    refetchInterval: 3000, // 每3秒自动刷新
    ...options,
  })
}

// 获取任务详情
export function useAgentTask(
  taskId: number,
  options?: Omit<UseQueryOptions<ApiResponse<AgentTask>>, 'queryKey' | 'queryFn'>
) {
  return useQuery({
    queryKey: agentKeys.task(taskId),
    queryFn: () => agentService.getAgentTask(taskId),
    enabled: !!taskId,
    refetchInterval: 2000, // 每2秒自动刷新
    ...options,
  })
}

// 执行Agent任务
export function useExecuteAgentTask() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ agentId, task }: { agentId: number; task: any }) =>
      agentService.executeAgentTask(agentId, task),
    onSuccess: (_, { agentId }) => {
      queryClient.invalidateQueries({ queryKey: agentKeys.tasks(agentId) })
      queryClient.invalidateQueries({ queryKey: agentKeys.lists() })
    },
  })
}
