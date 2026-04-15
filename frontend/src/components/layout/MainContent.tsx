import React from 'react'

interface MainContentProps {
  children: React.ReactNode
  className?: string
}

export default function MainContent({ children, className = '' }: MainContentProps) {
  return (
    <main className={`flex-1 p-6 overflow-auto ${className}`}>
      <div className="max-w-7xl mx-auto">
        {children}
      </div>
    </main>
  )
}
