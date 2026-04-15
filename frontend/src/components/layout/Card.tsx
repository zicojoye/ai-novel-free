import React from 'react'

interface CardProps {
  children: React.ReactNode
  className?: string
  title?: string
  headerActions?: React.ReactNode
  footer?: React.ReactNode
}

export default function Card({ 
  children, 
  className = '',
  title,
  headerActions,
  footer
}: CardProps) {
  return (
    <div className={`bg-card border rounded-lg ${className}`}>
      {/* 卡片头部 */}
      {(title || headerActions) && (
        <div className="px-6 py-4 border-b">
          <div className="flex items-center justify-between">
            {title && <h3 className="text-lg font-semibold">{title}</h3>}
            {headerActions && <div className="flex items-center space-x-2">{headerActions}</div>}
          </div>
        </div>
      )}

      {/* 卡片内容 */}
      <div className="p-6">
        {children}
      </div>

      {/* 卡片底部 */}
      {footer && (
        <div className="px-6 py-4 border-t bg-muted/50">
          {footer}
        </div>
      )}
    </div>
  )
}
