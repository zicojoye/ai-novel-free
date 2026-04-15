# UI组件库集成完成指南

## ✅ 已完成的组件

### 1. 错误边界组件

#### 文件
- `frontend/src/components/error/ErrorBoundary.tsx`
- `frontend/src/components/error/AsyncErrorBoundary.tsx`

#### 功能特性
- ✅ 捕获组件树中的JavaScript错误
- ✅ 显示友好的错误页面
- ✅ 开发环境显示详细错误堆栈
- ✅ 提供重试和返回首页选项
- ✅ 支持自定义fallback
- ✅ 异步错误边界
- ✅ 错误回调支持

#### 使用方式

```tsx
import { ErrorBoundary } from '@/components/ui'

// 包裹整个应用
<ErrorBoundary>
  <App />
</ErrorBoundary>

// 包裹特定组件
<ErrorBoundary fallback={<CustomError />}>
  <MyComponent />
</ErrorBoundary>

// 使用异步错误边界
import { AsyncErrorBoundary } from '@/components/ui'

<AsyncErrorBoundary onError={(error) => console.error(error)}>
  <AsyncComponent />
</AsyncErrorBoundary>
```

---

### 2. Toast通知系统

#### 文件
- `frontend/src/lib/toast.ts`
- `frontend/src/components/ui/ToastContainer.tsx`
- `frontend/src/components/ui/Toast.tsx`

#### 功能特性
- ✅ 4种通知类型（成功、错误、信息、警告）
- ✅ 加载中状态
- ✅ 自定义通知
- ✅ 位置控制（4个角落）
- ✅ 自动关闭
- ✅ 点击关闭
- ✅ 暂停悬停
- ✅ 拖拽移动
- ✅ 主题支持

#### 使用方式

```tsx
import { toast, ToastContainer } from '@/components/ui'

// 基本使用
toast.success('操作成功！')
toast.error('操作失败！')
toast.info('这是一条信息')
toast.warning('请注意！')

// 自定义配置
toast.success('保存成功', {
  duration: 5000,
  position: 'bottom-left'
})

// 加载状态
const toastId = toast.loading('正在保存...')

// 更新Toast
toast.update(toastId, {
  render: '保存完成！',
  type: 'success',
  autoClose: 3000
})

// 关闭所有
toast.dismiss()

// 关闭指定Toast
toast.dismissToast(toastId)
```

---

### 3. 加载骨架屏

#### 文件
- `frontend/src/components/loading/LoadingSpinner.tsx`
- `frontend/src/components/loading/Skeleton.tsx`
- `frontend/src/components/loading/LoadingState.tsx`

#### 组件列表

**LoadingSpinner**
- ✅ 3种尺寸（sm, md, lg）
- ✅ 全屏加载
- ✅ 带文本提示

**Skeleton组件**
- ✅ 基础骨架屏
- ✅ 卡片骨架屏 (CardSkeleton)
- ✅ 项目卡片骨架屏 (ProjectCardSkeleton)
- ✅ 章节列表骨架屏 (ChapterListSkeleton)
- ✅ 伏笔卡片骨架屏 (ForeshadowCardSkeleton)
- ✅ Agent卡片骨架屏 (AgentCardSkeleton)
- ✅ 表格骨架屏 (TableSkeleton)
- ✅ 侧边栏骨架屏 (SidebarSkeleton)
- ✅ 统计卡片骨架屏 (StatsCardSkeleton)

**LoadingState**
- ✅ 加载状态
- ✅ 错误状态
- ✅ 重试功能
- ✅ 自定义加载和错误组件

**EmptyState**
- ✅ 空状态展示
- ✅ 自定义图标
- ✅ 操作按钮

#### 使用方式

```tsx
import {
  LoadingSpinner,
  Skeleton,
  CardSkeleton,
  ProjectCardSkeleton,
  ChapterListSkeleton,
  LoadingState,
  EmptyState
} from '@/components/ui'

// 加载旋转器
<LoadingSpinner size="lg" text="加载中..." />
<LoadingSpinner fullScreen />

// 基础骨架屏
<Skeleton className="h-4 w-full" />
<Skeleton className="h-32 w-full" />

// 组件骨架屏
<CardSkeleton />
<ProjectCardSkeleton />
<ChapterListSkeleton count={5} />

// 加载状态组件
<LoadingState
  loading={isLoading}
  error={error}
  onRetry={() => refetch()}
>
  {data && <Content data={data} />}
</LoadingState>

// 空状态
<EmptyState
  title="暂无数据"
  description="点击按钮添加新项目"
  action={<Button onClick={onAdd}>添加</Button>}
/>
```

---

### 4. shadcn/ui组件库

#### 文件
- `frontend/src/components/ui/Button.tsx`
- `frontend/src/components/ui/Input.tsx`
- `frontend/src/components/ui/Textarea.tsx`
- `frontend/src/components/ui/Select.tsx`
- `frontend/src/components/ui/Card.tsx`
- `frontend/src/components/ui/Dialog.tsx`
- `frontend/src/components/ui/Badge.tsx`
- `frontend/src/components/ui/Tabs.tsx`
- `frontend/src/components/ui/Progress.tsx`
- `frontend/src/components/ui/index.ts`

#### 组件清单

**Button**
- 6种变体：default, destructive, outline, secondary, ghost, link
- 4种尺寸：default, sm, lg, icon
- 加载状态
- 禁用状态

**Input**
- 标准输入框
- 完整的focus样式
- 禁用状态

**Textarea**
- 多行文本输入
- 可调整高度
- 完整的focus样式

**Select**
- 下拉选择框
- 选项数组
- 完整的focus样式

**Card**
- Card - 卡片容器
- CardHeader - 卡片头部
- CardTitle - 卡片标题
- CardDescription - 卡片描述
- CardContent - 卡片内容
- CardFooter - 卡片底部

**Dialog**
- 模态对话框
- 背景遮罩
- 关闭按钮
- DialogFooter - 底部按钮区

**Badge**
- 6种变体：default, secondary, destructive, outline, success, warning
- 圆角样式
- 自定义内容

**Tabs**
- Tabs - 标签页容器
- TabsList - 标签列表
- TabsTrigger - 标签触发器
- TabsContent - 标签内容
- 活动状态管理

**Progress**
- 进度条
- 自定义最大值
- 动画过渡

#### 使用方式

```tsx
import {
  Button,
  Input,
  Textarea,
  Select,
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
  Dialog,
  DialogFooter,
  Badge,
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent,
  Progress
} from '@/components/ui'

// 按钮
<Button>点击</Button>
<Button variant="destructive">删除</Button>
<Button loading>保存</Button>

// 输入框
<Input placeholder="请输入..." />
<Textarea placeholder="请输入..." rows={4} />
<Select
  options={[
    { value: '1', label: '选项1' },
    { value: '2', label: '选项2' }
  ]}
/>

// 卡片
<Card>
  <CardHeader>
    <CardTitle>标题</CardTitle>
    <CardDescription>描述</CardDescription>
  </CardHeader>
  <CardContent>内容</CardContent>
  <CardFooter>底部</CardFooter>
</Card>

// 对话框
<Dialog open={open} onClose={onClose} title="标题">
  <p>内容</p>
  <DialogFooter>
    <Button onClick={onClose}>取消</Button>
    <Button onClick={onConfirm}>确定</Button>
  </DialogFooter>
</Dialog>

// 徽章
<Badge>标签</Badge>
<Badge variant="success">成功</Badge>

// 标签页
<Tabs defaultValue="tab1">
  <TabsList>
    <TabsTrigger value="tab1">标签1</TabsTrigger>
    <TabsTrigger value="tab2">标签2</TabsTrigger>
  </TabsList>
  <TabsContent value="tab1">内容1</TabsContent>
  <TabsContent value="tab2">内容2</TabsContent>
</Tabs>

// 进度条
<Progress value={75} />
```

---

## 🔧 工具函数

#### 文件
`frontend/src/lib/utils.ts`

#### 功能函数

- `cn()` - 合并Tailwind CSS类名
- `formatDate()` - 格式化日期
- `formatFileSize()` - 格式化文件大小
- `formatNumber()` - 格式化数字
- `truncate()` - 截断文本
- `generateId()` - 生成随机ID
- `debounce()` - 防抖函数
- `throttle()` - 节流函数
- `deepClone()` - 深拷贝
- `isEmpty()` - 检查是否为空
- `delay()` - 延迟执行
- `safeParseJSON()` - 安全解析JSON
- `getErrorMessage()` - 获取错误信息
- `downloadFile()` - 下载文件
- `copyToClipboard()` - 复制到剪贴板
- `getQueryParam()` - 获取URL参数
- `setQueryParam()` - 设置URL参数

#### 使用方式

```tsx
import {
  cn,
  formatDate,
  formatFileSize,
  debounce,
  isEmpty,
  downloadFile
} from '@/lib/utils'

// 合并类名
<div className={cn('base-class', condition && 'conditional-class')} />

// 格式化日期
formatDate(new Date(), 'full')
// 2026年4月14日 上午8:11

// 格式化文件大小
formatFileSize(1024 * 1024)
// 1.00 MB

// 防抖
const debouncedSearch = debounce((query) => {
  search(query)
}, 300)

// 检查是否为空
isEmpty('') // true
isEmpty([]) // true
isEmpty({}) // true

// 下载文件
downloadFile('content', 'file.txt')
```

---

## 📦 依赖包

```json
{
  "react-toastify": "^10.0.0",
  "clsx": "^2.0.0",
  "tailwind-merge": "^2.0.0",
  "lucide-react": "^0.300.0"
}
```

---

## 🎨 样式系统

### 颜色变量

使用Tailwind CSS的语义化颜色：

- `bg-primary` - 主色
- `bg-secondary` - 次要色
- `bg-accent` - 强调色
- `bg-muted` - 柔和色
- `bg-background` - 背景色
- `bg-card` - 卡片色
- `text-foreground` - 前景色
- `text-muted-foreground` - 弱化前景色
- `border-input` - 边框色
- `ring-ring` - 焦点环色

### 圆角

- `rounded` - 标准圆角
- `rounded-lg` - 大圆角
- `rounded-md` - 中圆角
- `rounded-full` - 完全圆角

### 阴影

- `shadow-sm` - 小阴影
- `shadow-lg` - 大阴影
- `shadow-none` - 无阴影

---

## 🎯 使用示例

### 完整表单示例

```tsx
import { useState } from 'react'
import { Button, Input, Textarea, Select, Card, toast } from '@/components/ui'

function ProjectForm() {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [type, setType] = useState('')

  const handleSubmit = async () => {
    try {
      await createProject({ name, description, type })
      toast.success('项目创建成功！')
    } catch (error) {
      toast.error('创建失败，请重试')
    }
  }

  return (
    <Card className="max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>创建项目</CardTitle>
        <CardDescription>填写项目信息</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <Input
          placeholder="项目名称"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <Textarea
          placeholder="项目描述"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={4}
        />
        <Select
          placeholder="选择类型"
          value={type}
          onChange={(e) => setType(e.target.value)}
          options={[
            { value: 'novel', label: '小说' },
            { value: 'story', label: '故事' }
          ]}
        />
      </CardContent>
      <CardFooter>
        <Button onClick={handleSubmit}>创建</Button>
      </CardFooter>
    </Card>
  )
}
```

### 列表页面示例

```tsx
import { LoadingState, EmptyState, Skeleton, CardSkeleton } from '@/components/ui'

function ProjectList() {
  const { data, isLoading, error, refetch } = useProjects()

  return (
    <LoadingState loading={isLoading} error={error} onRetry={refetch}>
      {data?.length === 0 ? (
        <EmptyState
          title="暂无项目"
          description="创建您的第一个项目吧"
          action={<Button onClick={onCreate}>创建项目</Button>}
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {data?.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      )}
    </LoadingState>
  )
}

// 骨架屏版本
function ProjectListSkeleton() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <ProjectCardSkeleton />
      <ProjectCardSkeleton />
      <ProjectCardSkeleton />
    </div>
  )
}
```

---

## 🐛 常见问题

### Toast不显示

确保在应用根部添加了`ToastContainer`：

```tsx
import { ToastContainer } from '@/components/ui'

function App() {
  return (
    <>
      <AppContent />
      <ToastContainer />
    </>
  )
}
```

### 错误边界不工作

确保错误边界包裹在错误组件的父级：

```tsx
<ErrorBoundary>
  <ProblematicComponent />
</ErrorBoundary>
```

### 样式不生效

确保正确导入了Tailwind CSS：

```tsx
// main.tsx
import './index.css'
```

---

## 📚 更多资源

- [Tailwind CSS文档](https://tailwindcss.com/docs)
- [React文档](https://react.dev)
- [shadcn/ui](https://ui.shadcn.com)
- [Lucide Icons](https://lucide.dev)

---

## ✅ 完成清单

- [x] 错误边界组件
- [x] Toast通知系统
- [x] 加载骨架屏
- [x] shadcn/ui组件库
- [x] 工具函数库
- [x] 使用示例
- [x] 完整文档

所有P3体验优化功能已完成！🎉
