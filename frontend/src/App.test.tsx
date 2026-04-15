import _React from 'react'


function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          AI Novel Platform
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* 测试卡片 */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">系统状态</h2>
            <div className="space-y-2">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                <span>前端: 正常</span>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                <span>后端: 测试中...</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">快速操作</h2>
            <div className="space-y-3">
              <button className="w-full bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                创建新项目
              </button>
              <button className="w-full bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
                查看文档
              </button>
              <button className="w-full bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600">
                访问API文档
              </button>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 md:col-span-2">
            <h2 className="text-xl font-semibold mb-4">功能列表</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center p-4 bg-gray-50 rounded">
                <div className="text-2xl mb-2">📚</div>
                <div className="text-sm text-gray-600">世界观构建</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded">
                <div className="text-2xl mb-2">✍️</div>
                <div className="text-sm text-gray-600">章节创作</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded">
                <div className="text-2xl mb-2">🎭</div>
                <div className="text-sm text-gray-600">剧情管理</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded">
                <div className="text-2xl mb-2">📖</div>
                <div className="text-sm text-gray-600">知识库</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded">
                <div className="text-2xl mb-2">🤖</div>
                <div className="text-sm text-gray-600">Agent系统</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded">
                <div className="text-2xl mb-2">💡</div>
                <div className="text-sm text-gray-600">提示词库</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded">
                <div className="text-2xl mb-2">🚀</div>
                <div className="text-sm text-gray-600">自动发布</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded">
                <div className="text-2xl mb-2">📊</div>
                <div className="text-sm text-gray-600">统计报表</div>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-2">提示</h3>
          <ul className="list-disc list-inside space-y-1 text-sm text-gray-700">
            <li>确保已配置.env文件中的API Keys</li>
            <li>后端服务运行在 http://localhost:8000</li>
            <li>API文档: http://localhost:8000/docs</li>
            <li>查看 <code>docs/启动指南.md</code> 获取详细帮助</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default App
