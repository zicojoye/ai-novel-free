import { useState, useEffect, useCallback } from 'react'
import api from '@/lib/api'
import type { Prompt, PromptCategory } from '@/types'

// ─── 常量 ──────────────────────────────────────────────────────────────────────

const CATEGORIES: { key: PromptCategory; label: string; icon: string; desc: string }[] = [
  { key: 'worldbuilding', label: '世界观', icon: '🌍', desc: '构建小说世界的规则、背景、设定' },
  { key: 'character',     label: '角色',   icon: '👤', desc: '角色创建、人物卡、性格塑造' },
  { key: 'scene',         label: '场景',   icon: '🏞️', desc: '场景描写、氛围营造、环境细节' },
  { key: 'dialogue',      label: '对话',   icon: '💬', desc: '人物对话、口吻设计、台词生成' },
  { key: 'plot',          label: '剧情',   icon: '📖', desc: '剧情推进、冲突设计、爽点节奏' },
  { key: 'polish',        label: '润色',   icon: '✨', desc: '文笔优化、词句打磨、风格统一' },
  { key: 'opening',       label: '开头',   icon: '🚀', desc: '黄金开头、钩子设计、首章冲击' },
  { key: 'chapter',       label: '章节',   icon: '📝', desc: '章节大纲、节奏把控、篇幅规划' },
  { key: 'ending',        label: '结局',   icon: '🎯', desc: '大结局、番外、收尾逻辑' },
  { key: 'other',         label: '其他',   icon: '📦', desc: '通用提示词、工具性模板' },
]

// ─── 提示词编辑弹窗 ────────────────────────────────────────────────────────────

function PromptEditor({
  initial,
  defaultCategory,
  onSave,
  onClose,
}: {
  initial?: Prompt
  defaultCategory: PromptCategory
  onSave: (p: Partial<Prompt>) => Promise<void>
  onClose: () => void
}) {
  const [name, setName] = useState(initial?.name ?? '')
  const [category, setCategory] = useState<PromptCategory>(initial?.category ?? defaultCategory)
  const [template, setTemplate] = useState(initial?.template ?? '')
  const [tags, setTags] = useState((initial?.tags ?? []).join(', '))
  const [saving, setSaving] = useState(false)
  const [err, setErr] = useState('')

  const handle = async () => {
    if (!name.trim() || !template.trim()) { setErr('名称和模板不能为空'); return }
    setSaving(true); setErr('')
    try {
      await onSave({
        name: name.trim(),
        category,
        template: template.trim(),
        tags: tags.split(',').map(t => t.trim()).filter(Boolean),
      })
      onClose()
    } catch { setErr('保存失败，请重试') } finally { setSaving(false) }
  }

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-card rounded-2xl w-full max-w-lg shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="p-5 border-b flex items-center justify-between">
          <h3 className="font-bold text-lg">{initial ? '编辑提示词' : '新建提示词'}</h3>
          <button onClick={onClose} className="text-muted-foreground hover:text-foreground text-2xl leading-none">×</button>
        </div>
        <div className="p-5 space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-sm font-medium mb-1 block">名称 *</label>
              <input value={name} onChange={e => setName(e.target.value)}
                className="w-full border rounded-lg px-3 py-2 bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="提示词名称" />
            </div>
            <div>
              <label className="text-sm font-medium mb-1 block">分类</label>
              <select value={category} onChange={e => setCategory(e.target.value as PromptCategory)}
                className="w-full border rounded-lg px-3 py-2 bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary">
                {CATEGORIES.map(c => <option key={c.key} value={c.key}>{c.icon} {c.label}</option>)}
              </select>
            </div>
          </div>
          <div>
            <label className="text-sm font-medium mb-1 block">模板内容 *</label>
            <textarea value={template} onChange={e => setTemplate(e.target.value)} rows={6}
              className="w-full border rounded-lg px-3 py-2 bg-background text-sm font-mono resize-none focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="输入提示词模板，可用 {变量名} 定义变量..." />
          </div>
          <div>
            <label className="text-sm font-medium mb-1 block">标签（逗号分隔）</label>
            <input value={tags} onChange={e => setTags(e.target.value)}
              className="w-full border rounded-lg px-3 py-2 bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="爽文, 番茄, 摸鱼" />
          </div>
          {err && <p className="text-sm text-red-500 bg-red-500/10 rounded-lg px-3 py-2">{err}</p>}
        </div>
        <div className="p-5 border-t flex gap-3">
          <button onClick={onClose} className="flex-1 py-2.5 border rounded-lg text-sm font-medium hover:bg-accent">取消</button>
          <button onClick={handle} disabled={saving}
            className="flex-1 py-2.5 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 disabled:opacity-60">
            {saving ? '保存中...' : '保存'}
          </button>
        </div>
      </div>
    </div>
  )
}

// ─── 单条提示词卡片 ─────────────────────────────────────────────────────────────

function PromptCard({
  prompt,
  onToggle,
  onEdit,
  onDelete,
}: {
  prompt: Prompt
  onToggle: () => void
  onEdit: () => void
  onDelete: () => void
}) {
  const [expanded, setExpanded] = useState(false)

  return (
    <div className={`border rounded-xl p-4 transition-all ${prompt.enabled ? 'bg-card' : 'bg-muted/30 opacity-60'}`}>
      <div className="flex items-start gap-3">
        <button
          onClick={onToggle}
          className={`mt-0.5 w-10 h-6 rounded-full transition-colors shrink-0 relative ${prompt.enabled ? 'bg-primary' : 'bg-muted-foreground/30'}`}
          title={prompt.enabled ? '点击关闭' : '点击启用'}
        >
          <span className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow transition-all ${prompt.enabled ? 'left-4' : 'left-0.5'}`} />
        </button>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className="font-medium text-sm truncate">{prompt.name}</span>
            {(prompt.tags ?? []).slice(0, 2).map(t => (
              <span key={t} className="text-xs px-1.5 py-0.5 bg-accent text-accent-foreground rounded-full shrink-0">#{t}</span>
            ))}
          </div>
          <p className={`text-xs text-muted-foreground font-mono ${expanded ? '' : 'line-clamp-2'}`}>
            {prompt.template}
          </p>
          {prompt.template.length > 80 && (
            <button onClick={() => setExpanded(v => !v)} className="text-xs text-primary mt-1 hover:underline">
              {expanded ? '收起' : '展开'}
            </button>
          )}
        </div>

        <div className="flex flex-col gap-1 shrink-0">
          <button onClick={onEdit} className="text-xs px-2 py-1 border rounded hover:bg-accent transition-colors">编辑</button>
          <button onClick={onDelete} className="text-xs px-2 py-1 border border-red-500/30 text-red-500 rounded hover:bg-red-500/10 transition-colors">删除</button>
        </div>
      </div>
    </div>
  )
}

// ─── 主页面 ────────────────────────────────────────────────────────────────────

export default function PromptLibrary() {
  const [activeTab, setActiveTab] = useState<PromptCategory>('worldbuilding')
  const [prompts, setPrompts] = useState<Prompt[]>([])
  const [loading, setLoading] = useState(false)
  const [editTarget, setEditTarget] = useState<Prompt | 'new' | null>(null)
  const [search, setSearch] = useState('')

  const activeCat = CATEGORIES.find(c => c.key === activeTab)!

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const res = await api.get('/prompts', { params: { category: activeTab } })
      const list: Prompt[] = Array.isArray(res) ? res : (res?.data ?? res?.items ?? [])
      setPrompts(list)
    } catch {
      setPrompts([])
    } finally {
      setLoading(false)
    }
  }, [activeTab])

  useEffect(() => { load() }, [load])

  const handleSave = async (data: Partial<Prompt>) => {
    if (editTarget === 'new') {
      await api.post('/prompts', { ...data, enabled: true })
    } else if (editTarget) {
      await api.put(`/prompts/${editTarget.id}`, data)
    }
    await load()
  }

  const handleToggle = async (p: Prompt) => {
    try {
      await api.put(`/prompts/${p.id}`, { enabled: !p.enabled })
      setPrompts(prev => prev.map(x => x.id === p.id ? { ...x, enabled: !x.enabled } : x))
    } catch {}
  }

  const handleDelete = async (p: Prompt) => {
    if (!confirm(`确认删除「${p.name}」？`)) return
    try {
      await api.delete(`/prompts/${p.id}`)
      setPrompts(prev => prev.filter(x => x.id !== p.id))
    } catch {}
  }

  const filtered = prompts.filter(p =>
    !search || p.name.toLowerCase().includes(search.toLowerCase()) || p.template.includes(search)
  )

  const enabledCount = prompts.filter(p => p.enabled).length

  return (
    <div className="space-y-0">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-3xl font-bold">提示词库</h2>
          <p className="text-muted-foreground text-sm mt-1">10个维度，管理你的本地提示词，开启后自动生效</p>
        </div>
        <button
          onClick={() => setEditTarget('new')}
          className="px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90"
        >
          + 新建提示词
        </button>
      </div>

      <div className="border-b mb-6">
        <div className="flex gap-0 overflow-x-auto">
          {CATEGORIES.map(cat => {
            const count = prompts.filter(p => p.category === cat.key).length
            return (
              <button
                key={cat.key}
                onClick={() => { setActiveTab(cat.key); setSearch('') }}
                className={`flex items-center gap-1.5 px-4 py-3 text-sm font-medium border-b-2 whitespace-nowrap transition-colors ${
                  activeTab === cat.key
                    ? 'border-primary text-primary'
                    : 'border-transparent text-muted-foreground hover:text-foreground'
                }`}
              >
                <span>{cat.icon}</span>
                <span>{cat.label}</span>
                {count > 0 && (
                  <span className={`text-xs px-1.5 py-0.5 rounded-full ${
                    activeTab === cat.key ? 'bg-primary/10 text-primary' : 'bg-muted text-muted-foreground'
                  }`}>{count}</span>
                )}
              </button>
            )
          })}
        </div>
      </div>

      <div className="flex items-center gap-4 mb-4">
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <span className="text-lg">{activeCat.icon}</span>
          <span>{activeCat.desc}</span>
          <span className="text-xs px-2 py-0.5 bg-muted rounded-full">
            {enabledCount}/{prompts.length} 已启用
          </span>
        </div>
        <input
          value={search}
          onChange={e => setSearch(e.target.value)}
          placeholder="搜索提示词..."
          className="ml-auto border rounded-lg px-3 py-1.5 bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary w-48"
        />
      </div>

      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3].map(i => (
            <div key={i} className="border rounded-xl p-4 animate-pulse">
              <div className="flex gap-3">
                <div className="w-10 h-6 bg-muted rounded-full" />
                <div className="flex-1 space-y-2">
                  <div className="h-4 bg-muted rounded w-1/3" />
                  <div className="h-3 bg-muted rounded w-full" />
                  <div className="h-3 bg-muted rounded w-2/3" />
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-16 text-muted-foreground">
          <div className="text-5xl mb-3">{activeCat.icon}</div>
          <p className="text-lg font-medium mb-1">
            {search ? '没有匹配的提示词' : `${activeCat.label}维度暂无提示词`}
          </p>
          <p className="text-sm mb-4">
            {search ? '换个关键词试试' : '点击「新建提示词」添加'}
          </p>
          {!search && (
            <button
              onClick={() => setEditTarget('new')}
              className="px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90"
            >
              + 新建第一条
            </button>
          )}
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map(p => (
            <PromptCard
              key={p.id}
              prompt={p}
              onToggle={() => handleToggle(p)}
              onEdit={() => setEditTarget(p)}
              onDelete={() => handleDelete(p)}
            />
          ))}
        </div>
      )}

      {editTarget !== null && (
        <PromptEditor
          initial={editTarget === 'new' ? undefined : editTarget}
          defaultCategory={activeTab}
          onSave={handleSave}
          onClose={() => setEditTarget(null)}
        />
      )}
    </div>
  )
}
