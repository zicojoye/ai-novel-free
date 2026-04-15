export default function ChapterEditor() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold">章节创作</h2>
        <div className="flex space-x-4">
          <button className="px-4 py-2 bg-secondary text-secondary-foreground rounded-lg hover:opacity-90">
            新建章节
          </button>
          <button className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90">
            AI生成
          </button>
        </div>
      </div>

      {/* 章节列表 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* 左侧：章节列表 */}
        <div className="bg-card border rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-4">章节列表</h3>
          <div className="space-y-2">
            {[1, 2, 3, 4, 5].map((num) => (
              <div
                key={num}
                className="p-3 border rounded-lg cursor-pointer hover:border-primary transition-colors"
              >
                <div className="font-medium">第{num}章</div>
                <div className="text-sm text-muted-foreground">章节标题</div>
              </div>
            ))}
          </div>
        </div>

        {/* 右侧：章节编辑器 */}
        <div className="lg:col-span-2 bg-card border rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">章节编辑</h3>

          {/* 章节标题 */}
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">章节标题</label>
            <input
              type="text"
              className="w-full p-3 border rounded-lg"
              placeholder="输入章节标题..."
            />
          </div>

          {/* 章节大纲 */}
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">章节大纲</label>
            <textarea
              className="w-full h-24 p-3 border rounded-lg"
              placeholder="输入章节大纲..."
            />
          </div>

          {/* 章节内容 */}
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">章节内容</label>
            <textarea
              className="w-full h-96 p-3 border rounded-lg"
              placeholder="开始创作你的章节..."
            />
          </div>

          {/* 工具栏 */}
          <div className="flex justify-between items-center">
            <div className="text-sm text-muted-foreground">
              字数: <span className="font-medium">0</span>
            </div>
            <div className="flex space-x-4">
              <button className="px-4 py-2 bg-secondary text-secondary-foreground rounded-lg hover:opacity-90">
                保存
              </button>
              <button className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90">
                AI扩写
              </button>
              <button className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90">
                发布
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
