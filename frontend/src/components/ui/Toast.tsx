import { X, CheckCircle2, AlertCircle, Info, AlertTriangle, Loader2 } from 'lucide-react'

interface ToastProps {
  type: 'success' | 'error' | 'info' | 'warning' | 'loading'
  message: string
  onClose?: () => void
}

const icons = {
  success: CheckCircle2,
  error: AlertCircle,
  info: Info,
  warning: AlertTriangle,
  loading: Loader2,
}

const colors = {
  success: 'text-green-500',
  error: 'text-red-500',
  info: 'text-blue-500',
  warning: 'text-yellow-500',
  loading: 'text-primary',
}

export function Toast({ type, message, onClose }: ToastProps) {
  const Icon = icons[type]

  return (
    <div className="flex items-start space-x-3 p-4 bg-card border rounded-lg shadow-lg">
      <div className={`flex-shrink-0 ${colors[type]} ${type === 'loading' ? 'animate-spin' : ''}`}>
        <Icon className="w-5 h-5" />
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-foreground">{message}</p>
      </div>
      {onClose && (
        <button
          onClick={onClose}
          className="flex-shrink-0 text-muted-foreground hover:text-foreground transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      )}
    </div>
  )
}

// Toast类型组件
export function SuccessToast({ message, onClose }: { message: string; onClose?: () => void }) {
  return <Toast type="success" message={message} onClose={onClose} />
}

export function ErrorToast({ message, onClose }: { message: string; onClose?: () => void }) {
  return <Toast type="error" message={message} onClose={onClose} />
}

export function InfoToast({ message, onClose }: { message: string; onClose?: () => void }) {
  return <Toast type="info" message={message} onClose={onClose} />
}

export function WarningToast({ message, onClose }: { message: string; onClose?: () => void }) {
  return <Toast type="warning" message={message} onClose={onClose} />
}

export function LoadingToast({ message }: { message: string }) {
  return <Toast type="loading" message={message} />
}
