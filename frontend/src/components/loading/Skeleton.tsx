import { cn } from '@/lib/utils'

interface SkeletonProps {
  className?: string
}

export function Skeleton({ className }: SkeletonProps) {
  return (
    <div
      className={cn('animate-pulse bg-muted rounded-md', className)}
      role="status"
      aria-label="加载中"
    />
  )
}

// 卡片骨架屏
export function CardSkeleton() {
  return (
    <div className="bg-card border rounded-lg p-6">
      <Skeleton className="h-6 w-3/4 mb-4" />
      <Skeleton className="h-4 w-full mb-2" />
      <Skeleton className="h-4 w-5/6 mb-4" />
      <div className="flex space-x-2">
        <Skeleton className="h-8 w-20" />
        <Skeleton className="h-8 w-20" />
      </div>
    </div>
  )
}

// 项目卡片骨架屏
export function ProjectCardSkeleton() {
  return (
    <div className="bg-card border rounded-lg p-6">
      <div className="flex justify-between items-start mb-4">
        <Skeleton className="h-6 w-1/2" />
        <Skeleton className="h-6 w-20" />
      </div>
      <Skeleton className="h-4 w-full mb-2" />
      <Skeleton className="h-4 w-3/4 mb-4" />
      <div className="flex space-x-2">
        <Skeleton className="h-6 w-16" />
        <Skeleton className="h-6 w-20" />
      </div>
    </div>
  )
}

// 章节列表骨架屏
export function ChapterListSkeleton({ count = 5 }: { count?: number }) {
  return (
    <div className="space-y-2">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="p-4 border rounded-lg">
          <div className="flex justify-between items-center mb-2">
            <Skeleton className="h-5 w-1/3" />
            <Skeleton className="h-6 w-16" />
          </div>
          <Skeleton className="h-4 w-full mb-1" />
          <Skeleton className="h-4 w-1/2" />
        </div>
      ))}
    </div>
  )
}

// 伏笔卡片骨架屏
export function ForeshadowCardSkeleton() {
  return (
    <div className="p-4 border rounded-lg">
      <div className="flex justify-between items-center mb-2">
        <Skeleton className="h-5 w-20" />
        <Skeleton className="h-5 w-16" />
      </div>
      <Skeleton className="h-4 w-3/4 mb-2" />
      <Skeleton className="h-4 w-full" />
      <div className="mt-2 flex justify-between">
        <Skeleton className="h-5 w-16" />
        <Skeleton className="h-4 w-12" />
      </div>
    </div>
  )
}

// Agent卡片骨架屏
export function AgentCardSkeleton() {
  return (
    <div className="bg-card border rounded-lg p-6">
      <div className="flex justify-between items-center mb-4">
        <Skeleton className="h-6 w-1/2" />
        <Skeleton className="h-3 w-3 rounded-full" />
      </div>
      <div className="space-y-2">
        <div className="flex justify-between">
          <Skeleton className="h-4 w-16" />
          <Skeleton className="h-4 w-20" />
        </div>
        <div className="flex justify-between">
          <Skeleton className="h-4 w-16" />
          <Skeleton className="h-4 w-16" />
        </div>
        <div className="flex justify-between">
          <Skeleton className="h-4 w-20" />
          <Skeleton className="h-4 w-12" />
        </div>
      </div>
      <div className="mt-4 flex space-x-2">
        <Skeleton className="h-8 w-full" />
        <Skeleton className="h-8 w-full" />
      </div>
    </div>
  )
}

// 表格骨架屏
export function TableSkeleton({ rows = 5, columns = 4 }: { rows?: number; columns?: number }) {
  return (
    <div className="w-full">
      {/* 表头 */}
      <div className="flex space-x-4 mb-4 pb-2 border-b">
        {Array.from({ length: columns }).map((_, i) => (
          <Skeleton key={i} className="h-6 flex-1" />
        ))}
      </div>
      {/* 表体 */}
      <div className="space-y-3">
        {Array.from({ length: rows }).map((_, i) => (
          <div key={i} className="flex space-x-4">
            {Array.from({ length: columns }).map((_, j) => (
              <Skeleton key={j} className="h-4 flex-1" />
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}

// 侧边栏骨架屏
export function SidebarSkeleton() {
  return (
    <div className="w-64 h-full border-r p-4 space-y-4">
      <Skeleton className="h-8 w-32" />
      <Skeleton className="h-10 w-full" />
      <div className="space-y-2">
        {Array.from({ length: 5 }).map((_, i) => (
          <Skeleton key={i} className="h-10 w-full" />
        ))}
      </div>
    </div>
  )
}

// 仪表盘统计骨架屏
export function StatsCardSkeleton() {
  return (
    <div className="bg-card border rounded-lg p-6">
      <Skeleton className="h-4 w-24 mb-2" />
      <Skeleton className="h-8 w-16" />
    </div>
  )
}
