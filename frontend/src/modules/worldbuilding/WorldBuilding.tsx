export default function WorldBuilding() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold">世界观构建</h2>
      </div>

      {/* 10维度编辑器 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 核心设定 */}
        <div className="bg-card border rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-4">核心设定</h3>
          <textarea
            className="w-full h-32 p-3 border rounded-lg"
            placeholder="描述故事的核心概念..."
          />
        </div>

        {/* 世界观 */}
        <div className="bg-card border rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-4">世界观</h3>
          <textarea
            className="w-full h-32 p-3 border rounded-lg"
            placeholder="描述世界的整体设定..."
          />
        </div>

        {/* 角色系统 */}
        <div className="bg-card border rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-4">角色系统</h3>
          <textarea
            className="w-full h-32 p-3 border rounded-lg"
            placeholder="描述主要角色和角色关系..."
          />
        </div>

        {/* 势力体系 */}
        <div className="bg-card border rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-4">势力体系</h3>
          <textarea
            className="w-full h-32 p-3 border rounded-lg"
            placeholder="描述各势力和组织..."
          />
        </div>

        {/* 力量体系 */}
        <div className="bg-card border rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-4">力量体系</h3>
          <textarea
            className="w-full h-32 p-3 border rounded-lg"
            placeholder="描述力量体系和修炼等级..."
          />
        </div>

        {/* 地理环境 */}
        <div className="bg-card border rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-4">地理环境</h3>
          <textarea
            className="w-full h-32 p-3 border rounded-lg"
            placeholder="描述世界地理和环境..."
          />
        </div>

        {/* 历史背景 */}
        <div className="bg-card border rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-4">历史背景</h3>
          <textarea
            className="w-full h-32 p-3 border rounded-lg"
            placeholder="描述世界历史和背景..."
          />
        </div>

        {/* 道具物品 */}
        <div className="bg-card border rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-4">道具物品</h3>
          <textarea
            className="w-full h-32 p-3 border rounded-lg"
            placeholder="描述重要道具和物品..."
          />
        </div>

        {/* 剧情主线 */}
        <div className="bg-card border rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-4">剧情主线</h3>
          <textarea
            className="w-full h-32 p-3 border rounded-lg"
            placeholder="描述主要剧情线和故事走向..."
          />
        </div>

        {/* 世界规则 */}
        <div className="bg-card border rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-4">世界规则</h3>
          <textarea
            className="w-full h-32 p-3 border rounded-lg"
            placeholder="描述世界的基本规则..."
          />
        </div>
      </div>

      {/* AI生成按钮 */}
      <div className="flex justify-end space-x-4">
        <button className="px-6 py-3 bg-secondary text-secondary-foreground rounded-lg hover:opacity-90">
          保存草稿
        </button>
        <button className="px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:opacity-90">
          AI生成世界观
        </button>
      </div>
    </div>
  )
}
