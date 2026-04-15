import api from '@/lib/api'
import type {
  ApiResponse,
  Agent,
  AgentTask,
} from '@/types'

export const agentService = {
  // 获取所有 Agent
  async getAgents(): Promise<ApiResponse<Agent[]>> {
    return api.get('/agents')
  },

  // 获取 Agent 详情
  async getAgent(id: string): Promise<ApiResponse<Agent>> {
    return api.get(`/agents/${id}`)
  },

  // 执行 Agent 任务
  async executeAgentTask(agentId: string, task: any): Promise<ApiResponse<any>> {
    return api.post(`/agents/${agentId}/execute`, task)
  },

  // 获取任务列表
  async getAgentTasks(agentId: string): Promise<ApiResponse<AgentTask[]>> {
    return api.get(`/agents/${agentId}/tasks`)
  },

  // 获取任务详情
  async getAgentTask(taskId: string): Promise<ApiResponse<AgentTask>> {
    return api.get(`/ai/tasks/${taskId}`)
  },
}
