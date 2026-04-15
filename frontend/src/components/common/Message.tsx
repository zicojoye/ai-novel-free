import { createRoot } from 'react-dom/client'
import { useEffect, useState } from 'react'
import { CheckCircle, XCircle, AlertCircle, Info, X } from 'lucide-react'

type MessageType = 'success' | 'error' | 'warning' | 'info'

interface MessageProps {
  type: MessageType
  content: string
  duration?: number
  onClose?: () => void
}

const MessageComponent = ({ type, content, duration = 3000, onClose }: MessageProps) => {
  const [visible, setVisible] = useState(true)

  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(false)
      setTimeout(() => onClose?.(), 300)
    }, duration)

    return () => clearTimeout(timer)
  }, [duration, onClose])

  const icons = {
    success: <CheckCircle className="w-5 h-5 text-green-500" />,
    error: <XCircle className="w-5 h-5 text-red-500" />,
    warning: <AlertCircle className="w-5 h-5 text-yellow-500" />,
    info: <Info className="w-5 h-5 text-blue-500" />,
  }

  const bgColors = {
    success: 'bg-green-50 border-green-200',
    error: 'bg-red-50 border-red-200',
    warning: 'bg-yellow-50 border-yellow-200',
    info: 'bg-blue-50 border-blue-200',
  }

  if (!visible) return null

  return (
    <div
      className={`fixed top-4 right-4 z-50 flex items-start gap-3 px-4 py-3 rounded-lg border shadow-lg transition-all duration-300 ${bgColors[type]}`}
    >
      {icons[type]}
      <div className="flex-1 text-sm text-gray-800 whitespace-pre-wrap">{content}</div>
      <button
        onClick={() => {
          setVisible(false)
          setTimeout(() => onClose?.(), 300)
        }}
        className="text-gray-400 hover:text-gray-600"
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  )
}

export const message = {
  success: (content: string, duration?: number) => {
    showMessage('success', content, duration)
  },
  error: (content: string, duration?: number) => {
    showMessage('error', content, duration)
  },
  warning: (content: string, duration?: number) => {
    showMessage('warning', content, duration)
  },
  info: (content: string, duration?: number) => {
    showMessage('info', content, duration)
  },
}

let messageCount = 0

function showMessage(type: MessageType, content: string, duration?: number) {
  const containerId = 'message-container'
  let container = document.getElementById(containerId)

  if (!container) {
    container = document.createElement('div')
    container.id = containerId
    container.className = 'fixed top-4 right-4 z-50 flex flex-col gap-2'
    document.body.appendChild(container)
  }

  const wrapper = document.createElement('div')
  container.appendChild(wrapper)

  const root = createRoot(wrapper)

  const handleClose = () => {
    root.unmount()
    container?.removeChild(wrapper)
    messageCount--
    if (messageCount === 0 && container?.childElementCount === 0) {
      document.body.removeChild(container)
    }
  }

  messageCount++
  root.render(
    <MessageComponent type={type} content={content} duration={duration} onClose={handleClose} />
  )
}

export default MessageComponent
