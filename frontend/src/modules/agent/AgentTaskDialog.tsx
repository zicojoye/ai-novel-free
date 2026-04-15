import { useState } from 'react'
import {
  X,
  Clock,
  CheckCircle2,
  XCircle,
  Loader2,
  Download,
  RefreshCw,
  ChevronDown,
  ChevronUp,
} from 'lucide-react'
import { useAgentTask, useAgents } from '@/hooks/useAgents'
import type { AgentTask } from '@/types'

interface AgentTaskDialogProps {
  taskId: number | null
  onClose: () => void
}

const statusConfig = {
  pending: {
    label: '等待中',
    color: 'bg-yellow-500',
    icon: Clock,
  },
  running: {
    label: '执行中',
    color: 'bg-blue-500',
    icon: Loader2,
    animate: true,
  },
  completed: {
    label: '已完成',
    color: 'bg-green-500',
    icon: CheckCircle2,
  },
  failed: {
    label: '失败',
    color: 'bg-red-500',
    icon: XCircle,
  },
}

export function AgentTaskDialog({ taskId, onClose }: AgentTaskDialogProps) {
  const [expandedSections, setExpandedSections] = useState<string[]>(['output'])

  const { data: taskData, isLoading, refetch } = useAgentTask(taskId || 0)
  const { data: agentsData } = useAgents()

  const task = taskData?.data
  const agent = agentsData?.data?.find((a) => a.id === task?.agent_id)
  const status = statusConfig[task?.status as keyof typeof statusConfig]
  const StatusIcon = status?.icon || Loader2

  const toggleSection = (section: string) => {
    setExpandedSections((prev) =>
      prev.includes(section)
        ? prev.filter((s) => s !== section)
        : [...prev, section]
    )
  }

  const downloadOutput = () => {
    if (task?.output) {
      const blob = new Blob([JSON.stringify(task.output, null, 2)], {
        type: 'application/json',
      })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `task-${taskId}-output.json`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    }
  }

  if (!taskId) return null

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-card border rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* 头部 */}
        <div className="flex items-center justify-between p-6 border-b">
          <div className="flex items-center space-x-3">
            <div
              className={`w-3 h-3 rounded-full ${status?.color} ${
                status?.animate ? 'animate-pulse' : ''
              }`}
            />
            <h2 className="text-xl font-bold">任务详情</h2>
            <span className="text-sm text-muted-foreground">
              #{taskId}
            </span>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => refetch()}
              className="p-2 hover:bg-accent rounded-lg transition-colors"
              title="刷新"
            >
              <RefreshCw className="w-5 h-5" />
            </button>
            <button
              onClick={onClose}
              className="p-2 hover:bg-accent rounded-lg transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* 内容 */}
        <div className="flex-1 overflow-y-auto p-6">
          {isLoading ? (
            <div className="flex items-center justify-center h-64">
              <Loader2 className="w-8 h-8 animate-spin text-primary" />
            </div>
          ) : task ? (
            <div className="space-y-6">
              {/* 状态卡片 */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-muted/50 rounded-lg p-4">
                  <div className="text-sm text-muted-foreground">状态</div>
                  <div className="flex items-center space-x-2 mt-2">
                    <StatusIcon
                      className={`w-5 h-5 ${
                        status?.animate ? 'animate-spin' : ''
                      }`}
                    />
                    <span className="font-medium">{status?.label}</span>
                  </div>
                </div>

                <div className="bg-muted/50 rounded-lg p-4">
                  <div className="text-sm text-muted-foreground">进度</div>
                  <div className="flex items-center space-x-2 mt-2">
                    <div className="flex-1 bg-secondary rounded-full h-2">
                      <div
                        className="bg-primary h-2 rounded-full transition-all"
                        style={{ width: `${task.progress}%` }}
                      />
                    </div>
                    <span className="font-medium">{task.progress}%</span>
                  </div>
                </div>

                <div className="bg-muted/50 rounded-lg p-4">
                  <div className="text-sm text-muted-foreground">Agent</div>
                  <div className="mt-2 font-medium">
                    {agent?.name || `Agent #${task.agent_id}`}
                  </div>
                </div>

                <div className="bg-muted/50 rounded-lg p-4">
                  <div className="text-sm text-muted-foreground">任务类型</div>
                  <div className="mt-2 font-medium">{task.type}</div>
                </div>
              </div>

              {/* 时间信息 */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-muted/50 rounded-lg p-4">
                  <div className="text-sm text-muted-foreground">创建时间</div>
                  <div className="mt-2 font-medium">
                    {new Date(task.created_at).toLocaleString('zh-CN')}
                  </div>
                </div>
                {task.completed_at && (
                  <div className="bg-muted/50 rounded-lg p-4">
                    <div className="text-sm text-muted-foreground">完成时间</div>
                    <div className="mt-2 font-medium">
                      {new Date(task.completed_at).toLocaleString('zh-CN')}
                    </div>
                  </div>
                )}
              </div>

              {/* 输入 */}
              {task.input && (
                <div className="border rounded-lg overflow-hidden">
                  <button
                    onClick={() => toggleSection('input')}
                    className="w-full flex items-center justify-between p-4 bg-muted/30 hover:bg-muted/50 transition-colors"
                  >
                    <h3 className="font-semibold">输入</h3>
                    {expandedSections.includes('input') ? (
                      <ChevronUp className="w-5 h-5" />
                    ) : (
                      <ChevronDown className="w-5 h-5" />
                    )}
                  </button>
                  {expandedSections.includes('input') && (
                    <div className="p-4 bg-background">
                      <pre className="text-sm whitespace-pre-wrap overflow-x-auto">
                        {JSON.stringify(task.input, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
              )}

              {/* 输出 */}
              {task.output && (
                <div className="border rounded-lg overflow-hidden">
                  <button
                    onClick={() => toggleSection('output')}
                    className="w-full flex items-center justify-between p-4 bg-muted/30 hover:bg-muted/50 transition-colors"
                  >
                    <div className="flex items-center space-x-2">
                      <h3 className="font-semibold">输出</h3>
                      {task.status === 'completed' && (
                        <button
                          onClick={downloadOutput}
                          className="p-1 hover:bg-accent rounded transition-colors"
                          title="下载输出"
                        >
                          <Download className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                    {expandedSections.includes('output') ? (
                      <ChevronUp className="w-5 h-5" />
                    ) : (
                      <ChevronDown className="w-5 h-5" />
                    )}
                  </button>
                  {expandedSections.includes('output') && (
                    <div className="p-4 bg-background">
                      <pre className="text-sm whitespace-pre-wrap overflow-x-auto">
                        {JSON.stringify(task.output, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
              )}

              {/* 错误信息 */}
              {task.error && (
                <div className="border border-red-500 rounded-lg overflow-hidden">
                  <button
                    onClick={() => toggleSection('error')}
                    className="w-full flex items-center justify-between p-4 bg-red-500/10 hover:bg-red-500/20 transition-colors"
                  >
                    <div className="flex items-center space-x-2">
                      <XCircle className="w-5 h-5 text-red-500" />
                      <h3 className="font-semibold text-red-500">错误信息</h3>
                    </div>
                    {expandedSections.includes('error') ? (
                      <ChevronUp className="w-5 h-5 text-red-500" />
                    ) : (
                      <ChevronDown className="w-5 h-5 text-red-500" />
                    )}
                  </button>
                  {expandedSections.includes('error') && (
                    <div className="p-4 bg-red-500/5">
                      <pre className="text-sm text-red-500 whitespace-pre-wrap overflow-x-auto">
                        {task.error}
                      </pre>
                    </div>
                  )}
                </div>
              )}
            </div>
          ) : (
            <div className="text-center text-muted-foreground">
              未找到任务信息
            </div>
          )}
        </div>

        {/* 底部 */}
        <div className="flex justify-end space-x-3 p-6 border-t">
          <button
            onClick={onClose}
            className="px-6 py-2 border rounded-lg hover:bg-accent transition-colors"
          >
            关闭
          </button>
          {task?.status === 'completed' && task.output && (
            <button
              onClick={downloadOutput}
              className="px-6 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90 transition-colors flex items-center space-x-2"
            >
              <Download className="w-4 h-4" />
              <span>下载输出</span>
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
