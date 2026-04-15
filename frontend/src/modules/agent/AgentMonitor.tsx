import { useState, useEffect } from 'react'
import { RefreshCw } from 'lucide-react'
import { useAgents } from '@/hooks/useAgents'
import api from '@/lib/api'
import type { Agent } from '@/types'

// ─── 常量 ──────────────────────────────────────────────────────────────────────

const ROLE_LABELS: Record<string, string> = {
  author: '创作作者',
  editor: '内容编辑',
  reviewer: '审核员',
  publisher: '发布员',
  world_builder: '世界观构建者',
  character_creator: '角色创建者',
  plot_designer: '剧情设计师',
  knowledge_manager: '知识库管理',
  logic_checker: '逻辑检查员',
  style_checker: '风格检查员',
  compliance_checker: '合规检查员',
  semantic_retriever: '语义检索器',
}

const ROLE_ICONS: Record<string, string> = {
  author: '✍️', editor: '📝', reviewer: '🔍', publisher: '📤',
  world_builder: '🌍', character_creator: '👤', plot_designer: '📖',
  knowledge_manager: '📚', logic_checker: '🔒', style_checker: '🎨',
  compliance_checker: '✅', semantic_retriever: '🔎',
}

const STATUS_COLORS: Record<string, string> = {
  idle: 'bg-gray-400',
  active: 'bg-green-500',
  completed: 'bg-blue-500',
  error: 'bg-red-500',
}

const STATUS_LABELS: Record<string, string> = {
  idle: '空闲', active: '运行中', completed: '已完成', error: '错误',
}

// ─── Agent配置抽屉（Free版：仅基础信息+提示词） ──────────────────────────────────

function AgentConfigDrawer({
  agent,
  onSaved,
  onClose,
}: {
  agent: Agent
  onSaved: (updated: Agent) => void
  onClose: () => void
}) {
  const [tab, setTab] = useState<'basic' | 'prompt'>('basic')
  const [form, setForm] = useState({
    description: agent.description ?? '',
    system_prompt: agent.system_prompt ?? '',
    enabled: agent.enabled !== false,
  })
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)

  const handleSave = async () => {
    setSaving(true)
    try {
      const res = await api.put(`/agents/${agent.id}`, {
        description: form.description,
        system_prompt: form.system_prompt,
        enabled: form.enabled,
      })
      const updated: Agent = res?.data ?? res
      onSaved({ ...agent, ...updated })
      setSaved(true)
      setTimeout(() => setSaved(false), 1500)
    } catch {} finally {
      setSaving(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-end md:items-center justify-center p-4" onClick={onClose}>
      <div className="bg-card rounded-2xl w-full max-w-lg max-h-[90vh] flex flex-col shadow-2xl" onClick={e => e.stopPropagation()}>
        {/* 头部 */}
        <div className="p-5 border-b flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center text-xl shrink-0">
            {ROLE_ICONS[agent.role] ?? '🤖'}
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <span className="font-bold truncate">{agent.name}</span>
              <span className={`w-2 h-2 rounded-full shrink-0 ${STATUS_COLORS[agent.status]}`} />
              <span className="text-xs text-muted-foreground">{STATUS_LABELS[agent.status]}</span>
            </div>
            <div className="text-xs text-muted-foreground">{ROLE_LABELS[agent.role] ?? agent.role}</div>
          </div>
          <button
            onClick={() => setForm(f => ({ ...f, enabled: !f.enabled }))}
            className={`w-11 h-6 rounded-full transition-colors relative shrink-0 ${form.enabled ? 'bg-primary' : 'bg-muted-foreground/30'}`}
          >
            <span className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow transition-all ${form.enabled ? 'left-5' : 'left-0.5'}`} />
          </button>
          <button onClick={onClose} className="text-muted-foreground hover:text-foreground text-2xl leading-none ml-1">×</button>
        </div>

        {/* Tab导航 */}
        <div className="flex border-b">
          {(['basic', 'prompt'] as const).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium transition-colors ${
                tab === t ? 'border-b-2 border-primary text-primary' : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              {t === 'basic' ? '基础信息' : '提示词'}
            </button>
          ))}
        </div>

        {/* Tab内容 */}
        <div className="flex-1 overflow-y-auto p-5 space-y-4">
          {tab === 'basic' && (
            <>
              <div>
                <label className="text-sm font-medium mb-1 block">Agent名称</label>
                <div className="w-full border rounded-lg px-3 py-2 bg-muted text-sm text-muted-foreground">
                  {agent.name}
                </div>
              </div>
              <div>
                <label className="text-sm font-medium mb-1 block">角色类型</label>
                <div className="w-full border rounded-lg px-3 py-2 bg-muted text-sm text-muted-foreground flex items-center gap-2">
                  <span>{ROLE_ICONS[agent.role]}</span>
                  <span>{ROLE_LABELS[agent.role] ?? agent.role}</span>
                </div>
              </div>
              <div>
                <label className="text-sm font-medium mb-1 block">描述</label>
                <textarea value={form.description} onChange={e => setForm(f => ({ ...f, description: e.target.value }))}
                  rows={3} placeholder="描述这个Agent的用途和特点..."
                  className="w-full border rounded-lg px-3 py-2 bg-background text-sm resize-none focus:outline-none focus:ring-2 focus:ring-primary" />
              </div>
              <div className="p-3 bg-muted/50 rounded-lg text-sm text-muted-foreground space-y-1">
                <div className="flex justify-between"><span>已完成任务</span><span className="font-medium">{agent.tasks_completed}</span></div>
                <div className="flex justify-between"><span>最后活跃</span><span>{agent.last_activity ? new Date(agent.last_activity).toLocaleString('zh-CN') : '从未'}</span></div>
                <div className="flex justify-between"><span>状态</span><span>{STATUS_LABELS[agent.status]}</span></div>
              </div>
            </>
          )}

          {tab === 'prompt' && (
            <>
              <div className="text-sm text-muted-foreground p-3 bg-blue-500/5 border border-blue-500/20 rounded-lg">
                💡 人格提示词会在每次调用此Agent时附加到系统消息，影响其输出风格和侧重点
              </div>
              <div>
                <label className="text-sm font-medium mb-1 block">人格 / 系统提示词</label>
                <textarea value={form.system_prompt} onChange={e => setForm(f => ({ ...f, system_prompt: e.target.value }))}
                  rows={8} placeholder={'例如：\n你是一位专注于都市爽文的创作助手，擅长快节奏、反套路剧情...'}
                  className="w-full border rounded-lg px-3 py-2 bg-background text-sm font-mono resize-none focus:outline-none focus:ring-2 focus:ring-primary" />
              </div>
              <p className="text-xs text-muted-foreground">不填则使用系统内置的默认角色提示词</p>
            </>
          )}
        </div>

        {/* 底部操作 */}
        <div className="p-4 border-t flex gap-3">
          <button onClick={onClose} className="flex-1 py-2.5 border rounded-lg text-sm font-medium hover:bg-accent">取消</button>
          <button onClick={handleSave} disabled={saving}
            className="flex-1 py-2.5 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 disabled:opacity-60">
            {saving ? '保存中...' : saved ? '已保存 ✓' : '保存配置'}
          </button>
        </div>
      </div>
    </div>
  )
}

// ─── Agent卡片 ─────────────────────────────────────────────────────────────────

function AgentCard({
  agent,
  onUpdated,
}: {
  agent: Agent
  onUpdated: (a: Agent) => void
}) {
  const [showConfig, setShowConfig] = useState(false)

  return (
    <>
      <div className={`border rounded-xl p-5 bg-card transition-all ${agent.enabled === false ? 'opacity-50' : 'hover:border-primary hover:shadow-sm'}`}>
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-lg bg-primary/10 flex items-center justify-center text-lg shrink-0">
              {ROLE_ICONS[agent.role] ?? '🤖'}
            </div>
            <div>
              <div className="font-semibold text-sm">{agent.name}</div>
              <div className="text-xs text-muted-foreground">{ROLE_LABELS[agent.role] ?? agent.role}</div>
            </div>
          </div>
          <div className="flex items-center gap-2 shrink-0">
            <div className={`w-2 h-2 rounded-full ${STATUS_COLORS[agent.status]}`} title={STATUS_LABELS[agent.status]} />
            {agent.enabled === false && <span className="text-xs text-muted-foreground">已关闭</span>}
          </div>
        </div>

        {agent.description && (
          <p className="text-xs text-muted-foreground mb-3 line-clamp-2">{agent.description}</p>
        )}

        <div className="flex items-center justify-between text-xs text-muted-foreground mb-3">
          <span>完成任务：{agent.tasks_completed}</span>
        </div>

        <button
          onClick={() => setShowConfig(true)}
          className="w-full py-2 text-sm border rounded-lg hover:bg-accent transition-colors font-medium"
        >
          ⚙️ 配置
        </button>
      </div>

      {showConfig && (
        <AgentConfigDrawer
          agent={agent}
          onSaved={(updated) => { onUpdated(updated); setShowConfig(false) }}
          onClose={() => setShowConfig(false)}
        />
      )}
    </>
  )
}

// ─── 主页面 ────────────────────────────────────────────────────────────────────

export default function AgentMonitor() {
  const { data: agentsData, isLoading, refetch } = useAgents()
  const [agents, setAgents] = useState<Agent[]>([])

  useEffect(() => {
    const list = agentsData?.data ?? (Array.isArray(agentsData) ? agentsData : [])
    if (list.length) setAgents(list)
  }, [agentsData])

  const handleUpdated = (updated: Agent) => {
    setAgents(prev => prev.map(a => a.id === updated.id ? updated : a))
  }

  const enabledCount = agents.filter(a => a.enabled !== false).length
  const activeCount = agents.filter(a => a.status === 'active').length

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold">Agent 配置</h2>
          <p className="text-muted-foreground text-sm mt-1">
            管理每个Agent的描述和人格 · {enabledCount}/{agents.length} 已启用
          </p>
        </div>
        <button onClick={() => refetch()} className="p-2 border rounded-lg hover:bg-accent transition-colors" title="刷新">
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="bg-card border rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-primary">{agents.length}</div>
          <div className="text-xs text-muted-foreground mt-1">总Agent数</div>
        </div>
        <div className="bg-card border rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-green-500">{enabledCount}</div>
          <div className="text-xs text-muted-foreground mt-1">已启用</div>
        </div>
        <div className="bg-card border rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-blue-500">{activeCount}</div>
          <div className="text-xs text-muted-foreground mt-1">运行中</div>
        </div>
        <div className="bg-card border rounded-xl p-4 text-center">
          <div className="text-2xl font-bold">
            {agents.reduce((s, a) => s + (a.tasks_completed ?? 0), 0)}
          </div>
          <div className="text-xs text-muted-foreground mt-1">累计任务</div>
        </div>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="bg-card border rounded-xl p-5 animate-pulse">
              <div className="flex gap-2.5 mb-3">
                <div className="w-9 h-9 bg-muted rounded-lg" />
                <div className="flex-1 space-y-1.5">
                  <div className="h-4 bg-muted rounded w-1/2" />
                  <div className="h-3 bg-muted rounded w-2/3" />
                </div>
              </div>
              <div className="h-3 bg-muted rounded w-full mb-4" />
              <div className="h-8 bg-muted rounded w-full" />
            </div>
          ))}
        </div>
      ) : agents.length === 0 ? (
        <div className="text-center py-16 text-muted-foreground">
          <div className="text-5xl mb-3">🤖</div>
          <p>暂无Agent，请启动后端服务</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {agents.map(agent => (
            <AgentCard
              key={agent.id}
              agent={agent}
              onUpdated={handleUpdated}
            />
          ))}
        </div>
      )}
    </div>
  )
}
