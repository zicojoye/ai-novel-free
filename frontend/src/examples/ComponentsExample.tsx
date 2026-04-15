import { useState } from 'react'
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
  Progress,
  toast,
} from '@/components/ui'

export function ComponentsExample() {
  const [dialogOpen, setDialogOpen] = useState(false)
  const [inputValue, setInputValue] = useState('')
  const [textareaValue, setTextareaValue] = useState('')
  const [selectValue, setSelectValue] = useState('')

  const handleSuccessToast = () => {
    toast.success('操作成功！')
  }

  const handleErrorToast = () => {
    toast.error('操作失败！')
  }

  const handleInfoToast = () => {
    toast.info('这是一条信息')
  }

  const handleWarningToast = () => {
    toast.warning('请注意！')
  }

  return (
    <div className="space-y-8 p-6">
      {/* 按钮示例 */}
      <section>
        <h2 className="text-2xl font-bold mb-4">按钮组件</h2>
        <div className="flex flex-wrap gap-3">
          <Button variant="default">默认按钮</Button>
          <Button variant="destructive">危险按钮</Button>
          <Button variant="outline">轮廓按钮</Button>
          <Button variant="secondary">次要按钮</Button>
          <Button variant="ghost">幽灵按钮</Button>
          <Button variant="link">链接按钮</Button>
          <Button loading>加载中</Button>
          <Button disabled>禁用</Button>
          <Button size="sm">小</Button>
          <Button size="lg">大</Button>
        </div>
      </section>

      {/* 输入框示例 */}
      <section>
        <h2 className="text-2xl font-bold mb-4">输入组件</h2>
        <div className="space-y-4 max-w-md">
          <Input
            placeholder="请输入内容..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />
          <Textarea
            placeholder="请输入多行内容..."
            rows={4}
            value={textareaValue}
            onChange={(e) => setTextareaValue(e.target.value)}
          />
          <Select
            placeholder="请选择..."
            value={selectValue}
            onChange={(e) => setSelectValue(e.target.value)}
            options={[
              { value: 'option1', label: '选项1' },
              { value: 'option2', label: '选项2' },
              { value: 'option3', label: '选项3' },
            ]}
          />
        </div>
      </section>

      {/* 卡片示例 */}
      <section>
        <h2 className="text-2xl font-bold mb-4">卡片组件</h2>
        <Card className="max-w-md">
          <CardHeader>
            <CardTitle>卡片标题</CardTitle>
            <CardDescription>这是卡片的描述信息</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              这是卡片的主要内容区域。您可以在这里放置任何您想要展示的内容。
            </p>
          </CardContent>
          <CardFooter>
            <Button>确定</Button>
            <Button variant="outline">取消</Button>
          </CardFooter>
        </Card>
      </section>

      {/* 徽章示例 */}
      <section>
        <h2 className="text-2xl font-bold mb-4">徽章组件</h2>
        <div className="flex flex-wrap gap-2">
          <Badge variant="default">默认</Badge>
          <Badge variant="secondary">次要</Badge>
          <Badge variant="destructive">危险</Badge>
          <Badge variant="outline">轮廓</Badge>
          <Badge variant="success">成功</Badge>
          <Badge variant="warning">警告</Badge>
        </div>
      </section>

      {/* 标签页示例 */}
      <section>
        <h2 className="text-2xl font-bold mb-4">标签页组件</h2>
        <Tabs defaultValue="tab1">
          <TabsList>
            <TabsTrigger value="tab1">标签页1</TabsTrigger>
            <TabsTrigger value="tab2">标签页2</TabsTrigger>
            <TabsTrigger value="tab3">标签页3</TabsTrigger>
          </TabsList>
          <TabsContent value="tab1">
            <p>这是标签页1的内容</p>
          </TabsContent>
          <TabsContent value="tab2">
            <p>这是标签页2的内容</p>
          </TabsContent>
          <TabsContent value="tab3">
            <p>这是标签页3的内容</p>
          </TabsContent>
        </Tabs>
      </section>

      {/* 进度条示例 */}
      <section>
        <h2 className="text-2xl font-bold mb-4">进度条组件</h2>
        <div className="space-y-4 max-w-md">
          <div>
            <div className="flex justify-between mb-2">
              <span className="text-sm">进度</span>
              <span className="text-sm">25%</span>
            </div>
            <Progress value={25} />
          </div>
          <div>
            <div className="flex justify-between mb-2">
              <span className="text-sm">进度</span>
              <span className="text-sm">50%</span>
            </div>
            <Progress value={50} />
          </div>
          <div>
            <div className="flex justify-between mb-2">
              <span className="text-sm">进度</span>
              <span className="text-sm">75%</span>
            </div>
            <Progress value={75} />
          </div>
          <div>
            <div className="flex justify-between mb-2">
              <span className="text-sm">进度</span>
              <span className="text-sm">100%</span>
            </div>
            <Progress value={100} />
          </div>
        </div>
      </section>

      {/* Toast示例 */}
      <section>
        <h2 className="text-2xl font-bold mb-4">Toast通知</h2>
        <div className="flex flex-wrap gap-3">
          <Button onClick={handleSuccessToast}>成功提示</Button>
          <Button onClick={handleErrorToast}>错误提示</Button>
          <Button onClick={handleInfoToast}>信息提示</Button>
          <Button onClick={handleWarningToast}>警告提示</Button>
        </div>
      </section>

      {/* 对话框示例 */}
      <section>
        <h2 className="text-2xl font-bold mb-4">对话框组件</h2>
        <Button onClick={() => setDialogOpen(true)}>打开对话框</Button>

        <Dialog
          open={dialogOpen}
          onClose={() => setDialogOpen(false)}
          title="对话框标题"
        >
          <div className="space-y-4">
            <p>这是对话框的内容区域。</p>
            <Input placeholder="请输入..." />
            <Textarea placeholder="请输入详细信息..." rows={4} />
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setDialogOpen(false)}>
              取消
            </Button>
            <Button onClick={() => setDialogOpen(false)}>
              确定
            </Button>
          </DialogFooter>
        </Dialog>
      </section>
    </div>
  )
}
