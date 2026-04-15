import { useEffect, useState } from 'react'
import { Card } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { formatDistanceToNow } from 'date-fns'
import { Activity, Clock, CheckCircle, AlertCircle, Zap } from 'lucide-react'

interface Event {
  id: number
  event_type: string
  source: {
    id: number
    type: string
  }
  target?: {
    id: number
    type: string
  }
  description: string
  importance: number
  data?: any
  timestamp: string
}

interface CategorizedEvents {
  tasks: Event[]
  messages: Event[]
  memory: Event[]
  knowledge: Event[]
  system: Event[]
  errors: Event[]
}

interface EventStreamProps {
  projectId: number
  refreshInterval?: number
}

export default function EventStream({ projectId, refreshInterval = 30000 }: EventStreamProps) {
  const [categories, setCategories] = useState<CategorizedEvents>({
    tasks: [],
    messages: [],
    memory: [],
    knowledge: [],
    system: [],
    errors: []
  })
  const [selectedCategory, setSelectedCategory] = useState<string>('all')
  const [isLive, setIsLive] = useState(true)

  // 获取事件流
  const fetchEvents = async () => {
    try {
      const response = await fetch(`/api/events/project/${projectId}/categorized`)
      const data = await response.json()
      
      if (data.success) {
        setCategories(data.categories)
      }
    } catch (error) {
      console.error('Failed to fetch events:', error)
    }
  }

  // WebSocket监听实时事件
  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/client_${Math.random()}`)
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      
      if (data.type === 'event') {
        addEventToCategory(data)
      }
    }

    return () => ws.close()
  }, [projectId])

  // 定期刷新
  useEffect(() => {
    if (!isLive) return

    fetchEvents()
    const interval = setInterval(fetchEvents, refreshInterval)
    
    return () => clearInterval(interval)
  }, [projectId, isLive, refreshInterval])

  // 添加事件到分类
  const addEventToCategory = (event: Event) => {
    setCategories(prev => {
      const newCategories = { ...prev }
      
      // 确定分类
      let category: keyof CategorizedEvents = 'system'
      if (event.event_type.includes('task')) category = 'tasks'
      else if (event.event_type.includes('message')) category = 'messages'
      else if (event.event_type === 'memory_update') category = 'memory'
      else if (event.event_type === 'knowledge_update') category = 'knowledge'
      else if (event.event_type === 'system_notice') category = 'system'
      else category = 'errors'

      // 添加到对应分类
      newCategories[category] = [event, ...newCategories[category]].slice(0, 50)
      
      return newCategories
    })
  }

  // 渲染事件
  const renderEvent = (event: Event) => {
    const importanceColor = {
      10: 'text-red-600 bg-red-50',
      8: 'text-orange-600 bg-orange-50',
      5: 'text-yellow-600 bg-yellow-50',
      3: 'text-blue-600 bg-blue-50',
      1: 'text-gray-600 bg-gray-50'
    }[event.importance as keyof typeof importanceColor] || 'text-gray-600 bg-gray-50'

    const eventTypeIcon = {
      task_start: <Clock className="w-4 h-4" />,
      task_progress: <Activity className="w-4 h-4" />,
      task_complete: <CheckCircle className="w-4 h-4" />,
      task_error: <AlertCircle className="w-4 h-4" />,
      agent_message: <Zap className="w-4 h-4" />,
      agent_mention: <Activity className="w-4 h-4" />,
      agent_response: <Zap className="w-4 h-4" />,
      memory_update: <Clock className="w-4 h-4" />,
      knowledge_update: <Zap className="w-4 h-4" />,
      system_notice: <Activity className="w-4 h-4" />
    }[event.event_type] || <Activity className="w-4 h-4" />

    return (
      <div
        key={event.id}
        className="p-3 border-b hover:bg-accent/50 transition-colors"
      >
        <div className="flex items-start gap-3">
          {/* 图标 */}
          <div className={`p-2 rounded-lg ${importanceColor} mt-1`}>
            {eventTypeIcon}
          </div>

          {/* 内容 */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              {/* 来源 */}
              <div className="flex items-center gap-2">
                <div className="text-sm font-medium">
                  {event.source.type === 'agent' ? `Agent ${event.source.id}` : 'User'}
                </div>
                {event.target && (
                  <div className="text-xs text-muted-foreground">
                    → {event.target.type} {event.target.id}
                  </div>
                )}
              </div>

              {/* 时间 */}
              <div className="text-xs text-muted-foreground ml-auto">
                {formatDistanceToNow(new Date(event.timestamp), { addSuffix: true })}
              </div>
            </div>

            {/* 描述 */}
            <div className="text-sm mb-2">
              {event.description}
            </div>

            {/* 详细数据 */}
            {event.data && Object.keys(event.data).length > 0 && (
              <div className="text-xs text-muted-foreground bg-muted/50 p-2 rounded">
                {Object.entries(event.data).map(([key, value]) => (
                  <div key={key}>
                    <span className="font-medium">{key}:</span> {String(value).slice(0, 100)}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* 重要性徽章 */}
          <Badge variant={event.importance >= 8 ? 'destructive' : 'secondary'}>
            {event.importance}
          </Badge>
        </div>
      </div>
    )
  }

  return (
    <div className="h-full flex flex-col">
      {/* 头部 */}
      <div className="border-b p-4 bg-card flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Activity className="w-5 h-5" />
          <h2 className="text-lg font-semibold">事件流</h2>
        </div>

        <div className="flex items-center gap-2">
          {/* 实时开关 */}
          <button
            onClick={() => setIsLive(!isLive)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              isLive ? 'bg-green-500 text-white' : 'bg-secondary'
            }`}
          >
            {isLive ? '● 实时' : '○ 暂停'}
          </button>

          {/* 刷新按钮 */}
          <button
            onClick={fetchEvents}
            className="p-2 hover:bg-accent rounded-lg transition-colors"
          >
            <Activity className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* 分类标签 */}
      <div className="border-b p-2 bg-muted/30 flex gap-2 overflow-x-auto">
        <button
          onClick={() => setSelectedCategory('all')}
          className={`px-4 py-2 rounded-lg text-sm whitespace-nowrap transition-colors ${
            selectedCategory === 'all'
              ? 'bg-primary text-primary-foreground'
              : 'hover:bg-accent'
          }`}
        >
          全部 ({Object.values(categories).flat().length})
        </button>
        <button
          onClick={() => setSelectedCategory('tasks')}
          className={`px-4 py-2 rounded-lg text-sm whitespace-nowrap transition-colors ${
            selectedCategory === 'tasks'
              ? 'bg-primary text-primary-foreground'
              : 'hover:bg-accent'
          }`}
        >
          任务 ({categories.tasks.length})
        </button>
        <button
          onClick={() => setSelectedCategory('messages')}
          className={`px-4 py-2 rounded-lg text-sm whitespace-nowrap transition-colors ${
            selectedCategory === 'messages'
              ? 'bg-primary text-primary-foreground'
              : 'hover:bg-accent'
          }`}
        >
          消息 ({categories.messages.length})
        </button>
        <button
          onClick={() => setSelectedCategory('memory')}
          className={`px-4 py-2 rounded-lg text-sm whitespace-nowrap transition-colors ${
            selectedCategory === 'memory'
              ? 'bg-primary text-primary-foreground'
              : 'hover:bg-accent'
          }`}
        >
          记忆 ({categories.memory.length})
        </button>
        <button
          onClick={() => setSelectedCategory('knowledge')}
          className={`px-4 py-2 rounded-lg text-sm whitespace-nowrap transition-colors ${
            selectedCategory === 'knowledge'
              ? 'bg-primary text-primary-foreground'
              : 'hover:bg-accent'
          }`}
        >
          知识 ({categories.knowledge.length})
        </button>
      </div>

      {/* 事件列表 */}
      <div className="flex-1 overflow-y-auto">
        {selectedCategory === 'all' ? (
          Object.entries(categories).map(([category, events]) => (
            <div key={category} className="mb-4">
              <div className="px-4 py-2 bg-muted/50 font-medium text-sm">
                {getCategoryName(category)}
              </div>
              <Card>
                {events.map(renderEvent)}
              </Card>
            </div>
          ))
        ) : (
          <Card className="m-4">
            {categories[selectedCategory as keyof CategorizedEvents].map(renderEvent)}
            {categories[selectedCategory as keyof CategorizedEvents].length === 0 && (
              <div className="text-center py-8 text-muted-foreground">
                <Activity className="w-12 h-12 mx-auto mb-2 opacity-50" />
                <p>暂无该分类的事件</p>
              </div>
            )}
          </Card>
        )}
      </div>
    </div>
  )

  function getCategoryName(category: string): string {
    const names = {
      tasks: '📋 任务',
      messages: '💬 消息',
      memory: '🧠 记忆',
      knowledge: '📚 知识',
      system: '⚙️ 系统',
      errors: '❌ 错误'
    }
    return names[category as keyof typeof names] || category
  }
}
