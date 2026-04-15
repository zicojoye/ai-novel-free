import { useEffect, useState, useCallback } from 'react'
import { useSettingsStore } from '@/stores/settingsStore'
import { settingsService } from '@/services/settingsService'
import type { AIModel } from '@/types'

// ─── 状态颜色配置 ─────────────────────────────────────────────────────────────
const STATUS_CONFIG: Record<string, { dot: string; text: string; bg: string }> = {
  connected:    { dot: 'bg-green-500',  text: '已连接',   bg: 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400' },
  disconnected: { dot: 'bg-red-500',    text: '连接失败', bg: 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400' },
  unconfigured: { dot: 'bg-gray-400',   text: '未配置',   bg: 'bg-secondary text-muted-foreground' },
  testing:      { dot: 'bg-yellow-400 animate-pulse', text: '测试中…', bg: 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-700 dark:text-yellow-400' },
}

// ─── Token 限制弹窗 ───────────────────────────────────────────────────────────
interface TokenLimitModalProps {
  modelId: string
  modelName: string
  current: { limit: number; used: number } | null
  onSave: (modelId: string, limit: number) => void
  onClose: () => void
}

function TokenLimitModal({ modelId, modelName, current, onSave, onClose }: TokenLimitModalProps) {
  const [limit, setLimit] = useState(current?.limit ?? 100000)

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="bg-card border rounded-xl p-6 w-full max-w-md shadow-xl">
        <h3 className="text-lg font-semibold mb-1">Token 用量限制</h3>
        <p className="text-sm text-muted-foreground mb-4">为「{modelName}」设置每日 Token 上限</p>

        {current && (
          <div className="mb-4 p-3 bg-secondary rounded-lg">
            <div className="flex justify-between text-sm mb-1">
              <span className="text-muted-foreground">今日已用</span>
              <span className="font-medium">{current.used.toLocaleString()} / {current.limit.toLocaleString()} tokens</span>
            </div>
            <div className="w-full bg-background rounded-full h-2">
              <div
                className={`h-2 rounded-full ${current.used / current.limit > 0.8 ? 'bg-red-500' : 'bg-primary'}`}
                style={{ width: `${Math.min(100, (current.used / current.limit) * 100)}%` }}
              />
            </div>
            <div className="flex justify-between text-xs text-muted-foreground mt-1">
              <span>已用 {Math.round((current.used / current.limit) * 100)}%</span>
              <span>剩余 {(current.limit - current.used).toLocaleString()} tokens</span>
            </div>
          </div>
        )}

        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">每日 Token 限制</label>
          <input
            type="number"
            min={1000}
            step={10000}
            value={limit}
            onChange={e => setLimit(Number(e.target.value))}
            className="w-full p-3 border rounded-lg bg-background text-sm"
          />
          <p className="text-xs text-muted-foreground mt-1">建议值：10万（低频）/ 50万（中频）/ 100万（高频）</p>
        </div>

        <div className="flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 px-4 py-2 border rounded-lg text-sm hover:bg-secondary"
          >
            取消
          </button>
          <button
            onClick={() => { onSave(modelId, limit); onClose() }}
            className="flex-1 px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90"
          >
            保存限制
          </button>
        </div>
      </div>
    </div>
  )
}

// ─── 添加自定义模型弹窗 ────────────────────────────────────────────────────────
interface AddModelModalProps {
  onSave: (data: { name: string; apiBase: string; apiKey: string; modelId: string }) => Promise<void>
  onClose: () => void
  saving: boolean
}

function AddModelModal({ onSave, onClose, saving }: AddModelModalProps) {
  const [form, setForm] = useState({ name: '', apiBase: '', apiKey: '', modelId: '' })
  const [showKey, setShowKey] = useState(false)

  const valid = form.name && form.apiBase && form.apiKey && form.modelId

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="bg-card border rounded-xl p-6 w-full max-w-lg shadow-xl">
        <h3 className="text-lg font-semibold mb-1">添加自定义大模型</h3>
        <p className="text-sm text-muted-foreground mb-4">支持所有兼容 OpenAI 格式的接口（硅基流动、月之暗面、本地 Ollama 等）</p>

        <div className="space-y-3">
          <div>
            <label className="block text-xs font-medium mb-1 text-muted-foreground">显示名称 *</label>
            <input
              type="text"
              className="w-full p-2.5 border rounded-lg bg-background text-sm"
              placeholder="例如：硅基流动 / 月之暗面 / 本地 Ollama"
              value={form.name}
              onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
            />
          </div>
          <div>
            <label className="block text-xs font-medium mb-1 text-muted-foreground">API Base URL *</label>
            <input
              type="text"
              className="w-full p-2.5 border rounded-lg bg-background text-sm font-mono"
              placeholder="例如：https://api.siliconflow.cn/v1"
              value={form.apiBase}
              onChange={e => setForm(f => ({ ...f, apiBase: e.target.value }))}
            />
          </div>
          <div>
            <label className="block text-xs font-medium mb-1 text-muted-foreground">模型 ID *</label>
            <input
              type="text"
              className="w-full p-2.5 border rounded-lg bg-background text-sm font-mono"
              placeholder="例如：Qwen/Qwen2.5-72B-Instruct"
              value={form.modelId}
              onChange={e => setForm(f => ({ ...f, modelId: e.target.value }))}
            />
          </div>
          <div>
            <label className="block text-xs font-medium mb-1 text-muted-foreground">API Key *</label>
            <div className="relative">
              <input
                type={showKey ? 'text' : 'password'}
                className="w-full pr-10 p-2.5 border rounded-lg bg-background text-sm font-mono"
                placeholder="sk-..."
                value={form.apiKey}
                onChange={e => setForm(f => ({ ...f, apiKey: e.target.value }))}
              />
              <button
                type="button"
                className="absolute right-2.5 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground text-xs"
                onClick={() => setShowKey(v => !v)}
              >
                {showKey ? '🙈' : '👁️'}
              </button>
            </div>
          </div>
        </div>

        <div className="flex gap-3 mt-5">
          <button onClick={onClose} className="flex-1 px-4 py-2 border rounded-lg text-sm hover:bg-secondary">取消</button>
          <button
            disabled={!valid || saving}
            onClick={() => onSave(form)}
            className="flex-1 px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {saving ? '保存中…' : '保存并添加'}
          </button>
        </div>
      </div>
    </div>
  )
}

// ─── 大模型管理主组件 ──────────────────────────────────────────────────────────
interface TokenLimit { limit: number; used: number }

function ModelManager() {
  const { apiKeys, apiKeysLoading, loadApiKeys, saveApiKeys } = useSettingsStore()

  // 编辑已有 provider 的 key
  const [editKeys, setEditKeys] = useState<Record<string, string>>({})
  const [showKeys, setShowKeys] = useState<Record<string, boolean>>({})
  const [testing, setTesting] = useState<Record<string, boolean>>({})
  const [testResults, setTestResults] = useState<Record<string, string>>({})
  const [saving, setSaving] = useState<Record<string, boolean>>({})

  // Token 限制（纯前端本地存储，key = provider id）
  const [tokenLimits, setTokenLimits] = useState<Record<string, TokenLimit>>(() => {
    try { return JSON.parse(localStorage.getItem('ai-token-limits') ?? '{}') } catch { return {} }
  })
  const [tokenModalId, setTokenModalId] = useState<string | null>(null)

  // 添加自定义模型弹窗
  const [showAddModal, setShowAddModal] = useState(false)
  const [addSaving, setAddSaving] = useState(false)

  useEffect(() => { loadApiKeys() }, [loadApiKeys])

  const getInfo = (id: string) => apiKeys.find(k => k.id === id) as any

  const handleTest = useCallback(async (pid: string) => {
    setTesting(p => ({ ...p, [pid]: true }))
    setTestResults(p => ({ ...p, [pid]: 'testing' }))
    try {
      const res = await settingsService.testApiKey(pid)
      setTestResults(p => ({ ...p, [pid]: res.status }))
    } catch {
      setTestResults(p => ({ ...p, [pid]: 'disconnected' }))
    } finally {
      setTesting(p => ({ ...p, [pid]: false }))
    }
  }, [])

  const handleSaveKey = async (pid: string) => {
    const val = editKeys[pid]
    if (!val) return
    setSaving(p => ({ ...p, [pid]: true }))
    const fieldMap: Record<string, string> = {
      openai: 'openai_api_key', anthropic: 'anthropic_api_key',
      deepseek: 'deepseek_api_key', gemini: 'gemini_api_key', custom: 'custom_api_key',
    }
    const ok = await saveApiKeys({ [fieldMap[pid]]: val } as any)
    setSaving(p => ({ ...p, [pid]: false }))
    if (ok) setEditKeys(p => { const n = { ...p }; delete n[pid]; return n })
  }

  const handleSaveTokenLimit = (modelId: string, limit: number) => {
    const newLimits = { ...tokenLimits, [modelId]: { limit, used: tokenLimits[modelId]?.used ?? 0 } }
    setTokenLimits(newLimits)
    localStorage.setItem('ai-token-limits', JSON.stringify(newLimits))
  }

  const handleAddModel = async (data: { name: string; apiBase: string; apiKey: string; modelId: string }) => {
    setAddSaving(true)
    const ok = await saveApiKeys({
      custom_api_key: data.apiKey,
      custom_api_base: data.apiBase,
      custom_model_id: data.modelId,
      custom_provider_name: data.name,
    } as any)
    setAddSaving(false)
    if (ok) setShowAddModal(false)
  }

  const customInfo = getInfo('custom')
  const hasCustom = !!(customInfo?.api_base && customInfo?.configured)

  const tokenModalInfo = tokenModalId
    ? { id: tokenModalId, name: customInfo?.provider_name ?? '自定义' }
    : null

  return (
    <div className="bg-card border rounded-lg p-6">
      {/* 头部 */}
      <div className="flex items-center justify-between mb-2">
        <div>
          <h3 className="text-xl font-semibold">大模型管理</h3>
          <p className="text-xs text-muted-foreground mt-0.5">配置后自动写入后端，无需重启服务</p>
        </div>
        <div className="flex items-center gap-2">
          {apiKeysLoading && <span className="text-xs text-muted-foreground">加载中…</span>}
          <button
            onClick={() => setShowAddModal(true)}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90"
          >
            <span className="text-base leading-none">+</span> 添加自定义模型
          </button>
        </div>
      </div>

      {/* 已配置列表 */}
      {hasCustom && (
        <div className="mt-4 mb-2">
          <p className="text-xs font-medium text-muted-foreground mb-2 uppercase tracking-wide">已配置</p>
          <div className="space-y-3">
            {/* 自定义 Provider（已配置时显示） */}
            {hasCustom && (() => {
              const id = 'custom'
              const tl = tokenLimits[id]
              const displayStatus = testResults[id] ?? (testing[id] ? 'testing' : 'connected')
              const statusCfg = STATUS_CONFIG[displayStatus] ?? STATUS_CONFIG.connected
              return (
                <div key="custom" className="border-2 border-primary/20 rounded-lg p-4">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-medium text-sm">{customInfo?.provider_name || '自定义'}</span>
                        <span className="text-xs px-1.5 py-0.5 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded">自定义</span>
                        <div className={`flex items-center gap-1.5 px-2 py-0.5 rounded-full text-xs font-medium ${statusCfg.bg}`}>
                          <span className={`w-1.5 h-1.5 rounded-full ${statusCfg.dot}`} />
                          {statusCfg.text}
                        </div>
                      </div>
                      <p className="text-xs font-mono text-muted-foreground">{customInfo?.api_base}</p>
                      <p className="text-xs text-muted-foreground mt-0.5">模型：{customInfo?.model_id}</p>
                      {customInfo?.masked_key && (
                        <p className="text-xs font-mono text-muted-foreground mt-0.5">{customInfo.masked_key}</p>
                      )}
                      {tl && (
                        <div className="mt-2">
                          <div className="flex justify-between text-xs text-muted-foreground mb-1">
                            <span>Token 用量</span>
                            <span>{tl.used.toLocaleString()} / {tl.limit.toLocaleString()}</span>
                          </div>
                          <div className="w-full bg-secondary rounded-full h-1.5">
                            <div
                              className={`h-1.5 rounded-full ${tl.used / tl.limit > 0.8 ? 'bg-red-500' : 'bg-primary'}`}
                              style={{ width: `${Math.min(100, (tl.used / tl.limit) * 100)}%` }}
                            />
                          </div>
                          <p className="text-xs text-muted-foreground mt-0.5">剩余 {(tl.limit - tl.used).toLocaleString()} tokens</p>
                        </div>
                      )}
                    </div>
                    <div className="flex items-center gap-2 flex-shrink-0">
                      <button
                        onClick={() => setTokenModalId(id)}
                        className={`px-2.5 py-1.5 text-xs border rounded-lg hover:bg-secondary ${tl ? 'text-primary border-primary/30' : ''}`}
                      >
                        {tl ? '限制中' : 'Token 限制'}
                      </button>
                      <button
                        disabled={testing[id]}
                        onClick={() => handleTest(id)}
                        className="px-2.5 py-1.5 text-xs border rounded-lg hover:bg-secondary disabled:opacity-50"
                      >
                        {testing[id] ? '…' : '测试'}
                      </button>
                      <button
                        onClick={() => setShowAddModal(true)}
                        className="px-2.5 py-1.5 text-xs border rounded-lg hover:bg-secondary"
                      >
                        编辑
                      </button>
                    </div>
                  </div>
                </div>
              )
            })()}
          </div>
        </div>
      )}

      {/* 空状态（未配置自定义模型时） */}
      {!hasCustom && !apiKeysLoading && (
        <div className="mt-4 py-8 text-center text-muted-foreground">
          <p className="text-sm">尚未配置任何大模型</p>
          <p className="text-xs mt-1">在上方输入 API Key 后点击保存，或点击"添加自定义模型"</p>
        </div>
      )}

      {/* Token 限制弹窗 */}
      {tokenModalId && tokenModalInfo && (
        <TokenLimitModal
          modelId={tokenModalInfo.id}
          modelName={tokenModalInfo.name}
          current={tokenLimits[tokenModalInfo.id] ?? null}
          onSave={handleSaveTokenLimit}
          onClose={() => setTokenModalId(null)}
        />
      )}

      {/* 添加模型弹窗 */}
      {showAddModal && (
        <AddModelModal
          onSave={handleAddModel}
          onClose={() => setShowAddModal(false)}
          saving={addSaving}
        />
      )}
    </div>
  )
}
// ─────────────────────────────────────────────────────────────────────────────

export default function Settings() {
  const { settings, models, modelsLoading, updateSettings, resetSettings, loadModels } =
    useSettingsStore()

  const [saved, setSaved] = useState(false)
  const [customMode, setCustomMode] = useState(false)

  useEffect(() => {
    loadModels()
  }, [loadModels])

  const activeModel = customMode && settings.custom_model_input
    ? settings.custom_model_input
    : settings.default_model

  const groupedModels = models.reduce<Record<string, AIModel[]>>((acc, m) => {
    if (!acc[m.provider]) acc[m.provider] = []
    acc[m.provider].push(m)
    return acc
  }, {})

  const providerLabels: Record<string, string> = {
    openai: 'OpenAI',
    anthropic: 'Anthropic',
    deepseek: 'DeepSeek',
    gemini: 'Google Gemini',
    custom: '自定义',
  }

  const handleSave = () => {
    if (customMode && settings.custom_model_input) {
      updateSettings({ default_model: settings.custom_model_input })
    }
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold">设置</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 大模型管理 — 跨双列显示 */}
        <div className="lg:col-span-2">
          <ModelManager />
        </div>

        {/* 通用设置 */}
        <div className="bg-card border rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-4">通用设置</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">主题</label>
              <select
                className="w-full p-3 border rounded-lg bg-background"
                value={settings.theme}
                onChange={(e) => updateSettings({ theme: e.target.value as any })}
              >
                <option value="auto">跟随系统</option>
                <option value="light">浅色</option>
                <option value="dark">深色</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">语言</label>
              <select
                className="w-full p-3 border rounded-lg bg-background"
                value={settings.language}
                onChange={(e) => updateSettings({ language: e.target.value })}
              >
                <option value="zh-CN">简体中文</option>
                <option value="en-US">English</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">
                字体大小：{settings.font_size}px
              </label>
              <input
                type="range"
                min="12"
                max="20"
                value={settings.font_size}
                onChange={(e) => updateSettings({ font_size: Number(e.target.value) })}
                className="w-full"
              />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">自动保存</span>
              <input
                type="checkbox"
                checked={settings.auto_save}
                onChange={(e) => updateSettings({ auto_save: e.target.checked })}
                className="w-5 h-5"
              />
            </div>
          </div>
        </div>

        {/* AI模型设置 */}
        <div className="bg-card border rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-4">AI模型设置</h3>
          <div className="space-y-4">
            <div className="p-3 bg-secondary rounded-lg text-sm">
              <span className="text-muted-foreground">当前使用：</span>
              <span className="font-mono font-medium ml-1">{activeModel}</span>
            </div>

            <div className="flex rounded-lg border overflow-hidden">
              <button
                className={`flex-1 py-2 text-sm font-medium transition-colors ${
                  !customMode ? 'bg-primary text-primary-foreground' : 'bg-background hover:bg-secondary'
                }`}
                onClick={() => setCustomMode(false)}
              >
                从列表选择
              </button>
              <button
                className={`flex-1 py-2 text-sm font-medium transition-colors ${
                  customMode ? 'bg-primary text-primary-foreground' : 'bg-background hover:bg-secondary'
                }`}
                onClick={() => setCustomMode(true)}
              >
                自定义输入
              </button>
            </div>

            {!customMode && (
              <div>
                <label className="block text-sm font-medium mb-2">
                  选择模型
                  {modelsLoading && <span className="ml-2 text-muted-foreground">加载中...</span>}
                </label>
                {models.length > 0 ? (
                  <select
                    className="w-full p-3 border rounded-lg bg-background"
                    value={settings.default_model}
                    onChange={(e) => updateSettings({ default_model: e.target.value })}
                  >
                    {Object.entries(groupedModels).map(([provider, list]) => (
                      <optgroup key={provider} label={providerLabels[provider] ?? provider}>
                        {list.map((m) => (
                          <option key={m.id} value={m.id}>
                            {m.name}{m.description ? ` — ${m.description}` : ''}
                          </option>
                        ))}
                      </optgroup>
                    ))}
                  </select>
                ) : (
                  <select
                    className="w-full p-3 border rounded-lg bg-background"
                    value={settings.default_model}
                    onChange={(e) => updateSettings({ default_model: e.target.value })}
                  >
                    <optgroup label="OpenAI">
                      <option value="gpt-4o">GPT-4o</option>
                      <option value="gpt-4o-mini">GPT-4o mini</option>
                      <option value="gpt-4-turbo">GPT-4 Turbo</option>
                      <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                    </optgroup>
                    <optgroup label="Anthropic">
                      <option value="claude-3-5-sonnet-20241022">Claude 3.5 Sonnet</option>
                      <option value="claude-3-5-haiku-20241022">Claude 3.5 Haiku</option>
                      <option value="claude-3-opus-20240229">Claude 3 Opus</option>
                    </optgroup>
                    <optgroup label="DeepSeek">
                      <option value="deepseek-chat">DeepSeek Chat</option>
                      <option value="deepseek-reasoner">DeepSeek Reasoner</option>
                    </optgroup>
                    <optgroup label="Google Gemini">
                      <option value="gemini-1.5-pro">Gemini 1.5 Pro</option>
                      <option value="gemini-1.5-flash">Gemini 1.5 Flash</option>
                      <option value="gemini-2.0-flash">Gemini 2.0 Flash</option>
                    </optgroup>
                  </select>
                )}
              </div>
            )}

            {customMode && (
              <div>
                <label className="block text-sm font-medium mb-2">自定义模型 ID</label>
                <input
                  type="text"
                  className="w-full p-3 border rounded-lg bg-background font-mono"
                  placeholder="例如：gpt-4o / Qwen/Qwen2.5-72B-Instruct"
                  value={settings.custom_model_input}
                  onChange={(e) => updateSettings({ custom_model_input: e.target.value })}
                />
                <p className="text-xs text-muted-foreground mt-1">
                  输入任意模型名称，系统会根据前缀自动匹配 provider。
                </p>
              </div>
            )}

            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">启用缓存</span>
              <input
                type="checkbox"
                checked={settings.enable_cache}
                onChange={(e) => updateSettings({ enable_cache: e.target.checked })}
                className="w-5 h-5"
              />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">启用语义缓存</span>
              <input
                type="checkbox"
                checked={settings.enable_semantic_cache}
                onChange={(e) => updateSettings({ enable_semantic_cache: e.target.checked })}
                className="w-5 h-5"
              />
            </div>
          </div>
        </div>

        {/* 成本控制 */}
        <div className="bg-card border rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-4">成本控制</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">每日预算 ($)</label>
              <input
                type="number"
                value={settings.budget_limit}
                onChange={(e) => updateSettings({ budget_limit: Number(e.target.value) })}
                className="w-full p-3 border rounded-lg bg-background"
              />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">启用预算限制</span>
              <input type="checkbox" defaultChecked className="w-5 h-5" />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">超预算告警</span>
              <input type="checkbox" defaultChecked className="w-5 h-5" />
            </div>
            <div className="p-4 bg-secondary rounded-lg">
              <div className="text-sm text-muted-foreground mb-1">今日已用</div>
              <div className="text-2xl font-bold">$0.00 / ${settings.budget_limit}.00</div>
              <div className="w-full bg-background rounded-full h-2 mt-2">
                <div className="bg-primary h-2 rounded-full" style={{ width: '0%' }} />
              </div>
            </div>
            <p className="text-xs text-muted-foreground">
              Token 用量限制可在大模型管理卡片中为每个模型单独设置
            </p>
          </div>
        </div>

        {/* 高级设置 */}
        <div className="bg-card border rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-4">高级设置</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">数据存储位置</label>
              <input
                type="text"
                defaultValue="./data"
                className="w-full p-3 border rounded-lg bg-background"
                readOnly
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">备份路径</label>
              <input
                type="text"
                className="w-full p-3 border rounded-lg bg-background"
                placeholder="输入备份路径..."
              />
            </div>
            <div className="flex space-x-4">
              <button className="flex-1 px-4 py-2 bg-secondary text-secondary-foreground rounded-lg hover:opacity-90">
                导出数据
              </button>
              <button className="flex-1 px-4 py-2 bg-secondary text-secondary-foreground rounded-lg hover:opacity-90">
                导入数据
              </button>
            </div>
            <div className="flex space-x-4">
              <button className="flex-1 px-4 py-2 bg-destructive text-destructive-foreground rounded-lg hover:opacity-90">
                清除缓存
              </button>
              <button
                className="flex-1 px-4 py-2 bg-destructive text-destructive-foreground rounded-lg hover:opacity-90"
                onClick={resetSettings}
              >
                重置设置
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-end space-x-4">
        <button
          className="px-6 py-3 bg-secondary text-secondary-foreground rounded-lg hover:opacity-90"
          onClick={resetSettings}
        >
          恢复默认
        </button>
        <button
          className="px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:opacity-90"
          onClick={handleSave}
        >
          {saved ? '已保存 ✓' : '保存设置'}
        </button>
      </div>
    </div>
  )
}
