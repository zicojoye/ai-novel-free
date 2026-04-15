import { X } from 'lucide-react'
import { cn } from '@/lib/utils'
import { HTMLAttributes, ReactNode } from 'react'

interface DialogProps extends HTMLAttributes<HTMLDivElement> {
  open: boolean
  onClose: () => void
  title?: string
  children: ReactNode
}

export function Dialog({ open, onClose, title, children, className, ...props }: DialogProps) {
  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* 背景遮罩 */}
      <div
        className="absolute inset-0 bg-black/50"
        onClick={onClose}
      />

      {/* 对话框 */}
      <div
        className={cn(
          'relative bg-card border rounded-lg shadow-lg max-w-2xl w-full max-h-[90vh] overflow-hidden flex flex-col',
          className
        )}
        {...props}
      >
        {/* 头部 */}
        {title && (
          <div className="flex items-center justify-between px-6 py-4 border-b">
            <h2 className="text-xl font-bold">{title}</h2>
            <button
              onClick={onClose}
              className="p-2 hover:bg-accent rounded-lg transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        )}

        {/* 内容 */}
        <div className="flex-1 overflow-y-auto p-6">
          {children}
        </div>
      </div>
    </div>
  )
}

// 对话框底部
export function DialogFooter({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn('flex items-center justify-end space-x-2 px-6 py-4 border-t', className)} {...props} />
  )
}
