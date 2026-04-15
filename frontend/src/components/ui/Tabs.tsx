import React from 'react'
import { cn } from '@/lib/utils'
import { HTMLAttributes, ReactNode, useState } from 'react'

interface TabsProps {
  defaultValue: string
  children: ReactNode
  className?: string
}

interface TabsListProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode
}

interface TabsTriggerProps extends HTMLAttributes<HTMLButtonElement> {
  value: string
  isActive: boolean
  onValueChange: (value: string) => void
  children: ReactNode
}

interface TabsContentProps extends HTMLAttributes<HTMLDivElement> {
  value: string
  activeValue: string
  children: ReactNode
}

export function Tabs({ defaultValue, children, className }: TabsProps) {
  const [activeValue, setActiveValue] = useState(defaultValue)

  return (
    <div className={className}>
      {React.Children.map(children, (child) => {
        if (React.isValidElement(child)) {
          if (child.type === TabsList) {
            return React.cloneElement(child, {
              ...child.props,
              children: React.Children.map(child.props.children, (triggerChild) => {
                if (React.isValidElement(triggerChild)) {
                  return React.cloneElement(triggerChild, {
                    ...triggerChild.props,
                    isActive: activeValue === triggerChild.props.value,
                    onValueChange: setActiveValue,
                  } as any)
                }
                return triggerChild
              }),
            })
          } else if (child.type === TabsContent) {
            return React.cloneElement(child, {
              ...child.props,
              activeValue,
            } as any)
          }
        }
        return child
      })}
    </div>
  )
}

export function TabsList({ children, className, ...props }: TabsListProps) {
  return (
    <div className={cn('inline-flex h-10 items-center justify-center rounded-lg bg-muted p-1', className)} {...props}>
      {children}
    </div>
  )
}

export function TabsTrigger({ value, isActive, onValueChange, children, className, ...props }: TabsTriggerProps) {
  return (
    <button
      type="button"
      onClick={() => onValueChange(value)}
      className={cn(
        'inline-flex items-center justify-center whitespace-nowrap rounded-md px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
        isActive
          ? 'bg-background text-foreground shadow'
          : 'text-muted-foreground hover:text-foreground',
        className
      )}
      {...props}
    >
      {children}
    </button>
  )
}

export function TabsContent({ value, activeValue, children, className, ...props }: TabsContentProps) {
  if (value !== activeValue) return null

  return (
    <div className={cn('mt-2', className)} {...props}>
      {children}
    </div>
  )
}
