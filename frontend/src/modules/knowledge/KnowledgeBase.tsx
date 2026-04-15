export default function KnowledgeBase() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold">知识库</h2>
        <button className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90">
          添加知识
        </button>
      </div>

      {/* 搜索栏 */}
      <div className="flex space-x-4">
        <input
          type="text"
          className="flex-1 p-3 border rounded-lg"
          placeholder="搜索知识库..."
        />
        <button className="px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:opacity-90">
          搜索
        </button>
      </div>

      {/* 知识分类 */}
      <div className="flex flex-wrap gap-2">
        {['全部', '角色', '剧情', '设定', '系统', '其他'].map((category) => (
          <button
            key={category}
            className="px-4 py-2 border rounded-lg hover:bg-accent"
          >
            {category}
          </button>
        ))}
      </div>

      {/* 知识列表 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[1, 2, 3, 4, 5, 6].map((id) => (
          <div key={id} className="bg-card border rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs px-2 py-1 bg-primary text-primary-foreground rounded">
                角色
              </span>
              <button className="text-sm text-muted-foreground hover:text-foreground">
                编辑
              </button>
            </div>
            <h4 className="font-medium">知识条目标题 {id}</h4>
            <p className="text-sm text-muted-foreground mt-2">
              这是知识条目的详细内容...
            </p>
            <div className="mt-3 flex flex-wrap gap-1">
              {['标签1', '标签2'].map((tag) => (
                <span key={tag} className="text-xs px-2 py-1 bg-secondary rounded">
                  {tag}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* AI提取 */}
      <div className="bg-card border rounded-lg p-6">
        <h3 className="text-xl font-semibold mb-4">AI知识提取</h3>
        <p className="text-muted-foreground mb-4">
          从已有章节中自动提取知识条目
        </p>
        <button className="px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:opacity-90">
          开始提取
        </button>
      </div>
    </div>
  )
}
