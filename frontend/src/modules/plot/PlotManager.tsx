import { useState } from 'react'
import { Plus, Search } from 'lucide-react'
import { useForeshadows, useDeleteForeshadow } from '@/hooks/useForeshadows'
import { ForeshadowForm } from './ForeshadowForm'
import { ConfirmDialog } from '@/components/common'
import { toast } from '@/lib/toast'
import type { Foreshadow } from '@/types'

interface PlotManagerProps {
  projectId?: number
}

const foreshadowTypeLabels: Record<string, string> = {
  chekhovs_gun: '契诃夫之枪',
  grass_snake: '草蛇灰线',
  suspense: '设悬念',
  setup: '埋伏笔',
  foreshadowing: '预示',
  callback: '回应',
  payoff: '揭晓',
  twist: '反转',
  hook: '钩子',
  echo: '呼应',
}

const statusLabels: Record<string, string> = {
  setup: '已埋设',
  callback: '已回应',
  paid_off: '已揭晓',
  forgotten: '已遗忘',
}

export default function PlotManager({ projectId = 0 }: PlotManagerProps) {
  const [showForeshadowForm, setShowForeshadowForm] = useState(false)
  const [selectedForeshadow, setSelectedForeshadow] =
    useState<Foreshadow | undefined>()
  const [filterType, setFilterType] = useState<string>('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [showDeleteDialog, setShowDeleteDialog] = useState(false)
  const [foreshadowToDelete, setForeshadowToDelete] = useState<number | null>(null)

  const { data: foreshadowsData, isLoading } = useForeshadows(projectId)
  const deleteMutation = useDeleteForeshadow()

  const foreshadows = foreshadowsData?.data || []

  // 过滤伏笔
  const filteredForeshadows = foreshadows.filter((f) => {
    const typeMatch = filterType === 'all' || f.type === filterType
    const searchMatch =
      !searchQuery ||
      f.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      f.description.toLowerCase().includes(searchQuery.toLowerCase())
    return typeMatch && searchMatch
  })

  const handleAddForeshadow = () => {
    setSelectedForeshadow(undefined)
    setShowForeshadowForm(true)
  }

  const handleEditForeshadow = (foreshadow: Foreshadow) => {
    setSelectedForeshadow(foreshadow)
    setShowForeshadowForm(true)
  }

  const handleDeleteForeshadow = (id: number) => {
    setForeshadowToDelete(id)
    setShowDeleteDialog(true)
  }

  const confirmDeleteForeshadow = async () => {
    if (!foreshadowToDelete) return
    try {
      await deleteMutation.mutateAsync(foreshadowToDelete)
      setShowDeleteDialog(false)
      setForeshadowToDelete(null)
      toast.success('伏笔删除成功')
    } catch (error) {
      toast.error('删除伏笔失败,请稍后重试')
    }
  }

  const foreshadowTypes = [
    'all',
    'chekhovs_gun',
    'grass_snake',
    'suspense',
    'setup',
    'foreshadowing',
    'callback',
    'payoff',
    'twist',
    'hook',
    'echo',
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold">剧情与伏笔</h2>
        <button
          onClick={handleAddForeshadow}
          className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90 flex items-center space-x-2"
        >
          <Plus className="w-4 h-4" />
          <span>添加伏笔</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 伏笔列表 */}
        <div className="bg-card border rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-4">伏笔追踪</h3>

          {/* 搜索框 */}
          <div className="relative mb-4">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="搜索伏笔..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-background border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          {/* 伏笔类型筛选 */}
          <div className="flex flex-wrap gap-2 mb-4">
            {foreshadowTypes.map((type) => (
              <button
                key={type}
                onClick={() => setFilterType(type)}
                className={`px-3 py-1 text-sm border rounded-lg transition-colors ${
                  filterType === type
                    ? 'bg-primary text-primary-foreground border-primary'
                    : 'hover:bg-accent'
                }`}
              >
                {type === 'all'
                  ? '全部'
                  : foreshadowTypeLabels[type] || type}
              </button>
            ))}
          </div>

          {/* 伏笔列表 */}
          {isLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <div key={i} className="p-4 border rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <div className="h-5 w-20 bg-muted animate-pulse rounded" />
                    <div className="h-5 w-16 bg-muted animate-pulse rounded" />
                  </div>
                  <div className="h-4 w-3/4 mb-2 bg-muted animate-pulse rounded" />
                  <div className="h-4 w-full bg-muted animate-pulse rounded" />
                  <div className="mt-2 flex justify-between">
                    <div className="h-5 w-16 bg-muted animate-pulse rounded" />
                    <div className="h-4 w-12 bg-muted animate-pulse rounded" />
                  </div>
                </div>
              ))}
            </div>
          ) : filteredForeshadows.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              {searchQuery || filterType !== 'all'
                ? '没有找到匹配的伏笔'
                : '暂无伏笔，点击上方按钮添加'}
            </div>
          ) : (
            <div className="space-y-3">
              {filteredForeshadows.map((foreshadow) => (
                <div
                  key={foreshadow.id}
                  className="p-4 border rounded-lg hover:border-primary transition-colors cursor-pointer"
                  onClick={() => handleEditForeshadow(foreshadow)}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs px-2 py-1 bg-primary text-primary-foreground rounded">
                      {foreshadowTypeLabels[foreshadow.type] ||
                        foreshadow.type}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      第{foreshadow.chapter_number}章
                    </span>
                  </div>
                  <h4 className="font-medium">{foreshadow.title}</h4>
                  <p className="text-sm text-muted-foreground mt-1 line-clamp-2">
                    {foreshadow.description}
                  </p>
                  <div className="mt-2 flex items-center justify-between">
                    <span className="text-xs px-2 py-1 bg-secondary rounded">
                      {statusLabels[foreshadow.status] || foreshadow.status}
                    </span>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        handleDeleteForeshadow(foreshadow.id)
                      }}
                      className="text-sm text-red-500 hover:underline"
                    >
                      删除
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* 钩子管理 */}
        <div className="bg-card border rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-4">钩子管理</h3>
          <div className="text-center py-8 text-muted-foreground">
            钩子管理功能即将上线...
          </div>
        </div>
      </div>

      {/* 时间线视图 */}
      <div className="bg-card border rounded-lg p-6">
        <h3 className="text-xl font-semibold mb-4">剧情时间线</h3>
        <div className="relative">
          <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-border"></div>
          <div className="space-y-6 ml-10">
            {Array.from({ length: 5 }, (_, i) => i + 1).map((chapter) => (
              <div key={chapter} className="relative">
                <div className="absolute -left-10 w-8 h-8 bg-primary rounded-full flex items-center justify-center text-primary-foreground text-sm font-medium">
                  {chapter}
                </div>
                <div className="p-4 border rounded-lg">
                  <h4 className="font-medium">第{chapter}章</h4>
                  <p className="text-sm text-muted-foreground mt-1">
                    章节内容摘要...
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 伏笔表单对话框 */}
      {showForeshadowForm && (
        <ForeshadowForm
          projectId={projectId}
          foreshadow={selectedForeshadow}
          onClose={() => setShowForeshadowForm(false)}
        />
      )}

      {/* 删除确认对话框 */}
      <ConfirmDialog
        isOpen={showDeleteDialog}
        title="确认删除伏笔"
        message="删除后将无法恢复,是否继续?"
        confirmText="删除"
        cancelText="取消"
        type="danger"
        onConfirm={confirmDeleteForeshadow}
        onCancel={() => {
          setShowDeleteDialog(false)
          setForeshadowToDelete(null)
        }}
      />
    </div>
  )
}
