# 前端React Query集成完成指南

## ✅ 已完成的功能

### 1. React Query集成优化

#### 创建的Hooks文件
- `frontend/src/hooks/useProjects.ts` - 项目管理hooks
- `frontend/src/hooks/useChapters.ts` - 章节管理hooks
- `frontend/src/hooks/useForeshadows.ts` - 伏笔管理hooks
- `frontend/src/hooks/useAgents.ts` - Agent管理hooks
- `frontend/src/hooks/useWorldBuilding.ts` - 世界观管理hooks
- `frontend/src/hooks/useKnowledge.ts` - 知识库管理hooks

#### 特性
- ✅ 统一的查询键工厂模式
- ✅ 自动缓存和数据同步
- ✅ 乐观更新
- ✅ 自动重试机制
- ✅ 开发模式DevTools集成

#### 配置优化
```typescript
// frontend/src/lib/queryClient.ts
- 数据新鲜时间: 5分钟
- 数据保持时间: 10分钟
- 失败重试: 1次，指数退避（最多3秒）
- 窗口失焦禁用自动重查询
```

### 2. 伏笔管理表单组件

#### 文件
`frontend/src/modules/plot/ForeshadowForm.tsx`

#### 功能
- ✅ 创建/编辑伏笔
- ✅ 10种伏笔类型选择（契诃夫之枪、草蛇灰线、设悬念等）
- ✅ 4种状态管理（已埋设、已回应、已揭晓、已遗忘）
- ✅ 关联章节选择（自动填充章节号）
- ✅ 完整的表单验证
- ✅ 响应式设计
- ✅ 表单加载状态
- ✅ 错误处理

#### 使用方式
```tsx
import { ForeshadowForm } from '@/modules/plot/ForeshadowForm'

// 创建伏笔
<ForeshadowForm
  projectId={123}
  onClose={() => {}}
  onSuccess={() => {}}
/>

// 编辑伏笔
<ForeshadowForm
  projectId={123}
  foreshadow={foreshadowData}
  onClose={() => {}}
  onSuccess={() => {}}
/>
```

### 3. Agent任务详情对话框

#### 文件
`frontend/src/modules/agent/AgentTaskDialog.tsx`

#### 功能
- ✅ 实时任务状态监控
- ✅ 任务进度显示
- ✅ 输入/输出展开查看
- ✅ 错误信息展示
- ✅ 任务输出JSON下载
- ✅ 自动刷新（每2-3秒）
- ✅ 可折叠的详细信息区域

#### 使用方式
```tsx
import { AgentTaskDialog } from '@/modules/agent/AgentTaskDialog'

<AgentTaskDialog
  taskId={123}
  onClose={() => {}}
/>
```

### 4. 组件更新

#### PlotManager组件更新
- ✅ 集成React Query hooks
- ✅ 集成ForeshadowForm
- ✅ 搜索功能
- ✅ 类型筛选
- ✅ 响应式伏笔列表
- ✅ 删除功能
- ✅ 编辑功能

#### AgentMonitor组件更新
- ✅ 集成React Query hooks
- ✅ 集成AgentTaskDialog
- ✅ Agent选择功能
- ✅ 实时任务监控
- ✅ 任务队列显示
- ✅ 刷新功能

#### 主应用更新
- ✅ 优化QueryClient配置
- ✅ 集成ReactQueryDevtools
- ✅ 统一查询客户端实例

## 📊 技术架构

### React Query查询键结构

```
projects:
  - projects:all
  - projects:list
  - projects:list:{page,pageSize}
  - projects:detail
  - projects:detail:{id}

chapters:
  - chapters:all
  - chapters:list
  - chapters:list:{projectId,params}
  - chapters:detail
  - chapters:detail:{id}

foreshadows:
  - foreshadows:all
  - foreshadows:list
  - foreshadows:list:{projectId,params}
  - foreshadows:detail
  - foreshadows:detail:{id}
  - foreshadows:{projectId}:type:{type}

agents:
  - agents:all
  - agents:list
  - agents:detail
  - agents:detail:{id}
  - agents:{agentId}:tasks
  - agents:task:{taskId}
```

### 数据流

```
组件 → Hook → Service → API
  ↓       ↓       ↓      ↓
状态  缓存    请求  后端
  ↓       ↓
  UI   更新
```

## 🎯 使用示例

### 在组件中使用伏笔管理

```tsx
import { useForeshadows } from '@/hooks/useForeshadows'
import { ForeshadowForm } from '@/modules/plot/ForeshadowForm'
import { useState } from 'react'

function MyComponent({ projectId }: { projectId: number }) {
  const [showForm, setShowForm] = useState(false)
  const { data: foreshadowsData, isLoading } = useForeshadows(projectId)

  return (
    <div>
      <button onClick={() => setShowForm(true)}>添加伏笔</button>

      {isLoading && <div>加载中...</div>}

      {foreshadowsData?.data?.map((f) => (
        <div key={f.id}>{f.title}</div>
      ))}

      {showForm && (
        <ForeshadowForm
          projectId={projectId}
          onClose={() => setShowForm(false)}
        />
      )}
    </div>
  )
}
```

### 在组件中使用Agent任务

```tsx
import { useAgentTask } from '@/hooks/useAgents'
import { AgentTaskDialog } from '@/modules/agent/AgentTaskDialog'
import { useState } from 'react'

function TaskView() {
  const [selectedTaskId, setSelectedTaskId] = useState<number | null>(null)
  const { data: taskData, isLoading } = useAgentTask(123)

  return (
    <div>
      <button onClick={() => setSelectedTaskId(123)}>
        查看任务详情
      </button>

      {selectedTaskId && (
        <AgentTaskDialog
          taskId={selectedTaskId}
          onClose={() => setSelectedTaskId(null)}
        />
      )}
    </div>
  )
}
```

## 🔧 配置说明

### QueryClient配置

```typescript
// frontend/src/lib/queryClient.ts
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,     // 5分钟数据新鲜
      gcTime: 10 * 60 * 1000,       // 10分钟数据保持
      refetchOnWindowFocus: false,   // 禁用窗口失焦重查询
      retry: 1,                      // 失败重试1次
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 3000),
    },
    mutations: {
      retry: false,                  // 变更不自动重试
    },
  },
})
```

### 环境变量

```env
# frontend/.env
VITE_API_BASE_URL=/api
```

## 📝 最佳实践

### 1. 使用查询键工厂

```typescript
// ✅ 推荐
export const projectKeys = {
  all: ['projects'] as const,
  lists: () => [...projectKeys.all, 'list'] as const,
  detail: (id: number) => [...projectKeys.all, 'detail', id] as const,
}

// ❌ 不推荐
useQuery(['projects', projectId], ...)
useQuery(['project-detail', projectId], ...)
```

### 2. 统一数据失效

```typescript
// 变更后统一刷新相关数据
const createMutation = useMutation({
  mutationFn: createProject,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: projectKeys.lists() })
  },
})
```

### 3. 乐观更新

```typescript
const updateMutation = useMutation({
  mutationFn: updateProject,
  onSuccess: (data, variables) => {
    // 更新详情页
    queryClient.setQueryData(projectKeys.detail(variables.id), data)
    // 刷新列表
    queryClient.invalidateQueries({ queryKey: projectKeys.lists() })
  },
})
```

### 4. 自动刷新实时数据

```typescript
// 任务等实时数据使用短间隔刷新
useAgentTasks(agentId, {
  refetchInterval: 3000, // 每3秒刷新
})
```

## 🚀 性能优化

### 已实现的优化

1. **请求去重**: React Query自动处理相同请求的去重
2. **缓存策略**: 5分钟数据新鲜期，10分钟数据保持
3. **懒加载**: 使用`enabled`条件查询
4. **乐观更新**: 立即更新UI，后台同步
5. **自动重试**: 指数退避重试机制
6. **窗口聚焦优化**: 禁用自动重查询减少请求

### 进一步优化建议

1. 使用`select`减少数据传输
2. 使用`placeholderData`提供骨架屏
3. 实现分页加载
4. 使用`prefetch`预加载数据
5. 实现无限滚动

## 🐛 调试

### React Query DevTools

开发环境下会自动启用DevTools，按F12打开浏览器控制台，在底部可以看到：
- 当前所有查询
- 查询状态
- 缓存数据
- 查询时间线
- 变更历史

### 查看缓存

```typescript
// 在组件中查看缓存
const queryCache = queryClient.getQueryCache()
console.log(queryCache.getAll())
```

### 手动刷新

```typescript
// 刷新特定查询
queryClient.invalidateQueries({ queryKey: projectKeys.lists() })

// 刷新所有查询
queryClient.invalidateQueries()
```

## 📦 依赖

```json
{
  "@tanstack/react-query": "^5.0.0",
  "@tanstack/react-query-devtools": "^5.0.0",
  "react-hook-form": "^7.0.0"
}
```

## ✅ 测试清单

- [x] 伏笔表单创建功能
- [x] 伏笔表单编辑功能
- [x] 伏笔类型筛选
- [x] 伏笔搜索功能
- [x] 伏笔删除功能
- [x] Agent任务对话框
- [x] 任务详情查看
- [x] 任务输入输出展示
- [x] 任务输出下载
- [x] React Query缓存
- [x] 查询键工厂
- [x] 自动刷新
- [x] 错误处理
- [x] 加载状态

## 🎉 总结

所有P2级别功能已完成：

1. ✅ **React Query集成优化**
   - 6个完整的hooks文件
   - 统一的查询键工厂
   - 优化的缓存策略
   - 自动重试机制

2. ✅ **伏笔管理表单组件**
   - 完整的表单验证
   - 多类型支持
   - 状态管理
   - 关联章节

3. ✅ **Agent任务详情对话框**
   - 实时监控
   - 输入输出查看
   - 错误展示
   - 数据下载

项目现已具备完整的前端数据管理能力！🚀
