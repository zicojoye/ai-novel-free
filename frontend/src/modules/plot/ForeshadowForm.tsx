import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { X, Plus, Save, Loader2 } from 'lucide-react'
import { useCreateForeshadow, useUpdateForeshadow } from '@/hooks/useForeshadows'
import { useChapters } from '@/hooks/useChapters'
import { toast } from '@/lib/toast'
import type { Foreshadow } from '@/types'

interface ForeshadowFormProps {
  projectId: number
  foreshadow?: Foreshadow
  onClose: () => void
  onSuccess?: () => void
}

interface FormData {
  type: string
  title: string
  description: string
  chapter_id: number | null
  chapter_number: number
  status: string
  notes?: string
}

const foreshadowTypes = [
  { value: 'chekhovs_gun', label: '契诃夫之枪', color: 'bg-blue-500' },
  { value: 'grass_snake', label: '草蛇灰线', color: 'bg-green-500' },
  { value: 'suspense', label: '设悬念', color: 'bg-purple-500' },
  { value: 'setup', label: '埋伏笔', color: 'bg-orange-500' },
  { value: 'foreshadowing', label: '预示', color: 'bg-cyan-500' },
  { value: 'callback', label: '回应', color: 'bg-pink-500' },
  { value: 'payoff', label: '揭晓', color: 'bg-yellow-500' },
  { value: 'twist', label: '反转', color: 'bg-red-500' },
  { value: 'hook', label: '钩子', color: 'bg-indigo-500' },
  { value: 'echo', label: '呼应', color: 'bg-teal-500' },
]

const statusOptions = [
  { value: 'setup', label: '已埋设', color: 'bg-gray-500' },
  { value: 'callback', label: '已回应', color: 'bg-blue-500' },
  { value: 'paid_off', label: '已揭晓', color: 'bg-green-500' },
  { value: 'forgotten', label: '已遗忘', color: 'bg-red-500' },
]

export function ForeshadowForm({
  projectId,
  foreshadow,
  onClose,
  onSuccess,
}: ForeshadowFormProps) {
  const isEditing = !!foreshadow

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setValue,
    watch,
  } = useForm<FormData>({
    defaultValues: foreshadow
      ? {
          type: foreshadow.type,
          title: foreshadow.title,
          description: foreshadow.description,
          chapter_id: foreshadow.chapter_id || null,
          chapter_number: foreshadow.chapter_number,
          status: foreshadow.status,
          notes: foreshadow.description,
        }
      : {
          type: 'chekhovs_gun',
          title: '',
          description: '',
          chapter_id: null,
          chapter_number: 1,
          status: 'setup',
        },
  })

  const { data: chaptersData } = useChapters(projectId)
  const createMutation = useCreateForeshadow()
  const updateMutation = useUpdateForeshadow()

  const [selectedType, setSelectedType] = useState(
    foreshadow?.type || 'chekhovs_gun'
  )
  const [selectedStatus, setSelectedStatus] = useState(
    foreshadow?.status || 'setup'
  )

  const onSubmit = async (data: FormData) => {
    try {
      const payload = {
        ...data,
        project_id: projectId,
        type: selectedType,
        status: selectedStatus,
        chapter_id: data.chapter_id || undefined,
      }

      if (isEditing && foreshadow) {
        await updateMutation.mutateAsync({
          id: foreshadow.id,
          data: payload,
        })
      } else {
        await createMutation.mutateAsync(payload)
      }

      onSuccess?.()
      onClose()
      toast.success(isEditing ? '伏笔更新成功' : '伏笔创建成功')
    } catch (error) {
      toast.error('保存伏笔失败,请稍后重试')
    }
  }

  const selectedChapterId = watch('chapter_id')
  const selectedChapter = chaptersData?.data?.find(
    (ch) => ch.id === selectedChapterId
  )

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-card border rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* 头部 */}
        <div className="flex items-center justify-between p-6 border-b">
          <h2 className="text-xl font-bold">
            {isEditing ? '编辑伏笔' : '添加伏笔'}
          </h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-accent rounded-lg transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* 表单 */}
        <form onSubmit={handleSubmit(onSubmit)} className="p-6 space-y-6">
          {/* 伏笔类型 */}
          <div>
            <label className="block text-sm font-medium mb-3">伏笔类型</label>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
              {foreshadowTypes.map((type) => (
                <button
                  key={type.value}
                  type="button"
                  onClick={() => {
                    setSelectedType(type.value)
                    setValue('type', type.value)
                  }}
                  className={`px-3 py-2 text-sm rounded-lg border-2 transition-all ${
                    selectedType === type.value
                      ? `${type.color} text-white border-transparent`
                      : 'border-border hover:border-primary'
                  }`}
                >
                  {type.label}
                </button>
              ))}
            </div>
          </div>

          {/* 标题 */}
          <div>
            <label htmlFor="title" className="block text-sm font-medium mb-2">
              伏笔标题 <span className="text-red-500">*</span>
            </label>
            <input
              id="title"
              type="text"
              {...register('title', { required: '请输入伏笔标题' })}
              placeholder="例如：主角的特殊能力"
              className="w-full px-4 py-2 bg-background border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            />
            {errors.title && (
              <p className="mt-1 text-sm text-red-500">{errors.title.message}</p>
            )}
          </div>

          {/* 描述 */}
          <div>
            <label htmlFor="description" className="block text-sm font-medium mb-2">
              伏笔描述 <span className="text-red-500">*</span>
            </label>
            <textarea
              id="description"
              {...register('description', { required: '请输入伏笔描述' })}
              rows={4}
              placeholder="详细描述这个伏笔的内容和作用..."
              className="w-full px-4 py-2 bg-background border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary resize-none"
            />
            {errors.description && (
              <p className="mt-1 text-sm text-red-500">
                {errors.description.message}
              </p>
            )}
          </div>

          {/* 关联章节 */}
          <div>
            <label htmlFor="chapter_id" className="block text-sm font-medium mb-2">
              关联章节
            </label>
            <select
              id="chapter_id"
              {...register('chapter_id')}
              onChange={(e) => {
                const chapterId = e.target.value
                  ? parseInt(e.target.value)
                  : null
                setValue('chapter_id', chapterId)

                // 自动填充章节号
                const chapter = chaptersData?.data?.find(
                  (ch) => ch.id === chapterId
                )
                if (chapter) {
                  setValue('chapter_number', chapter.chapter_number)
                }
              }}
              className="w-full px-4 py-2 bg-background border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="">选择章节（可选）</option>
              {chaptersData?.data?.map((chapter) => (
                <option key={chapter.id} value={chapter.id}>
                  第{chapter.chapter_number}章 - {chapter.title}
                </option>
              ))}
            </select>
          </div>

          {/* 章节号 */}
          <div>
            <label
              htmlFor="chapter_number"
              className="block text-sm font-medium mb-2"
            >
              章节号
            </label>
            <input
              id="chapter_number"
              type="number"
              min="1"
              {...register('chapter_number', {
                valueAsNumber: true,
                required: '请输入章节号',
              })}
              className="w-full px-4 py-2 bg-background border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            />
            {errors.chapter_number && (
              <p className="mt-1 text-sm text-red-500">
                {errors.chapter_number.message}
              </p>
            )}
          </div>

          {/* 状态 */}
          <div>
            <label className="block text-sm font-medium mb-3">伏笔状态</label>
            <div className="flex flex-wrap gap-2">
              {statusOptions.map((status) => (
                <button
                  key={status.value}
                  type="button"
                  onClick={() => {
                    setSelectedStatus(status.value)
                    setValue('status', status.value)
                  }}
                  className={`px-4 py-2 text-sm rounded-lg border-2 transition-all ${
                    selectedStatus === status.value
                      ? `${status.color} text-white border-transparent`
                      : 'border-border hover:border-primary'
                  }`}
                >
                  {status.label}
                </button>
              ))}
            </div>
          </div>

          {/* 备注 */}
          <div>
            <label htmlFor="notes" className="block text-sm font-medium mb-2">
              备注
            </label>
            <textarea
              id="notes"
              {...register('notes')}
              rows={3}
              placeholder="额外的备注信息..."
              className="w-full px-4 py-2 bg-background border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary resize-none"
            />
          </div>

          {/* 底部按钮 */}
          <div className="flex justify-end space-x-3 pt-4 border-t">
            <button
              type="button"
              onClick={onClose}
              className="px-6 py-2 border rounded-lg hover:bg-accent transition-colors"
            >
              取消
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-6 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90 disabled:opacity-50 transition-colors flex items-center space-x-2"
            >
              {isSubmitting ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Save className="w-4 h-4" />
              )}
              <span>{isEditing ? '更新' : '创建'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
