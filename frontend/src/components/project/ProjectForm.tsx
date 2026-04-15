import { useState } from 'react'
import type { Project } from '@/types'

interface ProjectFormProps {
  project?: Project
  onSubmit: (data: Partial<Project>) => Promise<void>
  onCancel: () => void
}

export function ProjectForm({ project, onSubmit, onCancel }: ProjectFormProps) {
  const [formData, setFormData] = useState({
    name: project?.name || '',
    description: project?.description || '',
    genre: project?.genre || '都市',
    targetAudience: project?.targetAudience || '25-35岁男性',
    status: project?.status || 'draft',
  })

  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      await onSubmit(formData)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-2">项目名称</label>
        <input
          type="text"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
          placeholder="输入项目名称..."
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">项目描述</label>
        <textarea
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary h-24"
          placeholder="描述你的项目..."
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium mb-2">类型</label>
          <select
            value={formData.genre}
            onChange={(e) => setFormData({ ...formData, genre: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
          >
            <option value="都市">都市</option>
            <option value="玄幻">玄幻</option>
            <option value="仙侠">仙侠</option>
            <option value="科幻">科幻</option>
            <option value="历史">历史</option>
            <option value="军事">军事</option>
            <option value="游戏">游戏</option>
            <option value="灵异">灵异</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">目标读者</label>
          <select
            value={formData.targetAudience}
            onChange={(e) => setFormData({ ...formData, targetAudience: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
          >
            <option value="18-25岁男性">18-25岁男性</option>
            <option value="25-35岁男性">25-35岁男性</option>
            <option value="35-45岁男性">35-45岁男性</option>
            <option value="18-25岁女性">18-25岁女性</option>
            <option value="25-35岁女性">25-35岁女性</option>
            <option value="全年龄段">全年龄段</option>
          </select>
        </div>
      </div>

      <div className="flex justify-end space-x-3 pt-4">
        <button
          type="button"
          onClick={onCancel}
          className="px-6 py-2 bg-secondary text-secondary-foreground rounded-lg hover:opacity-90 transition-opacity"
        >
          取消
        </button>
        <button
          type="submit"
          disabled={loading || !formData.name}
          className="px-6 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? '提交中...' : project ? '更新项目' : '创建项目'}
        </button>
      </div>
    </form>
  )
}
