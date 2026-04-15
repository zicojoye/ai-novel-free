import React, { useState } from 'react'

interface Tab {
  id: string
  label: string
  icon?: string
  disabled?: boolean
  content?: React.ReactNode
}

interface TabNavigationProps {
  tabs: Tab[]
  defaultTab?: string
  onChange?: (tabId: string) => void
  variant?: 'default' | 'pills' | 'underline'
  className?: string
}

export default function TabNavigation({ 
  tabs, 
  defaultTab,
  onChange,
  variant = 'default',
  className = ''
}: TabNavigationProps) {
  const [activeTab, setActiveTab] = useState(defaultTab || tabs[0]?.id)

  const handleTabChange = (tabId: string) => {
    setActiveTab(tabId)
    onChange?.(tabId)
  }

  const getTabStyle = (tab: Tab, isActive: boolean) => {
    const baseStyle = 'px-4 py-2 transition-colors cursor-pointer'
    
    if (tab.disabled) {
      return `${baseStyle} text-muted-foreground opacity-50 cursor-not-allowed`
    }

    switch (variant) {
      case 'pills':
        return `${baseStyle} rounded-lg ${
          isActive 
            ? 'bg-primary text-primary-foreground' 
            : 'hover:bg-accent'
        }`
      case 'underline':
        return `${baseStyle} border-b-2 ${
          isActive 
            ? 'border-primary text-primary' 
            : 'border-transparent hover:border-muted-foreground'
        }`
      default:
        return `${baseStyle} border-b-2 ${
          isActive 
            ? 'border-primary text-primary' 
            : 'border-transparent hover:border-muted-foreground'
        }`
    }
  }

  return (
    <div className={className}>
      {/* Tab 按钮 */}
      <div className={`flex space-x-1 ${variant === 'pills' ? '' : 'border-b'}`}>
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id
          return (
            <button
              key={tab.id}
              onClick={() => !tab.disabled && handleTabChange(tab.id)}
              className={getTabStyle(tab, isActive)}
              disabled={tab.disabled}
            >
              {tab.icon && <span className="mr-2">{tab.icon}</span>}
              {tab.label}
            </button>
          )
        })}
      </div>

      {/* Tab 内容 */}
      <div className="mt-4">
        {tabs.find((tab) => tab.id === activeTab)?.content}
      </div>
    </div>
  )
}
