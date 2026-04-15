import { Loader2, AlertCircle, RefreshCw } from 'lucide-react'
import { Button } from '@/components/ui/Button'

interface LoadingStateProps {
  loading?: boolean
  error?: Error | string | null
  onRetry?: () => void
  children: React.ReactNode
  loadingComponent?: React.ReactNode
  errorComponent?: React.ReactNode
}

export function LoadingState({
  loading = false,
  error = null,
  onRetry,
  children,
  loadingComponent,
  errorComponent,
}: LoadingStateProps) {
  // 加载状态
  if (loading) {
    return (
      loadingComponent || (
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <Loader2 className="w-8 h-8 animate-spin text-primary mx-auto mb-3" />
            <p className="text-sm text-muted-foreground">加载中...</p>
          </div>
        </div>
      )
    )
  }

  // 错误状态
  if (error) {
    return (
      errorComponent || (
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center max-w-md">
            <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">加载失败</h3>
            <p className="text-sm text-muted-foreground mb-4">
              {typeof error === 'string' ? error : error.message || '未知错误'}
            </p>
            {onRetry && (
              <Button onClick={onRetry} className="flex items-center space-x-2">
                <RefreshCw className="w-4 h-4" />
                <span>重试</span>
              </Button>
            )}
          </div>
        </div>
      )
    )
  }

  // 正常状态
  return <>{children}</>
}

// 空状态组件
interface EmptyStateProps {
  icon?: React.ReactNode
  title: string
  description?: string
  action?: React.ReactNode
}

export function EmptyState({
  icon,
  title,
  description,
  action,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[400px] p-8 text-center">
      {icon && <div className="mb-4">{icon}</div>}
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      {description && <p className="text-sm text-muted-foreground mb-4">{description}</p>}
      {action}
    </div>
  )
}

// 页面级加载器
export function PageLoader() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <Loader2 className="w-12 h-12 animate-spin text-primary" />
    </div>
  )
}

// 小型加载器
export function SmallLoader({ size = 'w-4 h-4' }: { size?: string }) {
  return <Loader2 className={`animate-spin text-primary ${size}`} />
}
