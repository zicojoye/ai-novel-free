import { Link } from 'react-router-dom'
import { Home, Search, ArrowLeft } from 'lucide-react'

/**
 * 404页面 - 页面不存在
 */
export default function NotFound() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-lg w-full">
        <div className="text-center mb-8">
          <h1 className="text-9xl font-bold text-blue-600 mb-4">404</h1>
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            页面不存在
          </h2>
          <p className="text-gray-600 text-lg">
            抱歉,您访问的页面不存在或已被移除。
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-8">
          <div className="space-y-4 mb-8">
            <div className="flex items-center gap-3 text-gray-700">
              <Search className="w-5 h-5 text-blue-600" />
              <span>检查URL是否输入正确</span>
            </div>
            <div className="flex items-center gap-3 text-gray-700">
              <Search className="w-5 h-5 text-blue-600" />
              <span>该页面可能已被移动或删除</span>
            </div>
            <div className="flex items-center gap-3 text-gray-700">
              <Search className="w-5 h-5 text-blue-600" />
              <span>返回首页重新导航</span>
            </div>
          </div>

          <div className="flex gap-3">
            <Link
              to="/"
              className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              <Home className="w-5 h-5" />
              返回首页
            </Link>
            <button
              onClick={() => window.history.back()}
              className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors font-medium"
            >
              <ArrowLeft className="w-5 h-5" />
              返回上一页
            </button>
          </div>
        </div>

        <p className="text-center text-gray-500 mt-6 text-sm">
          如果您认为这是一个错误,请联系管理员
        </p>
      </div>
    </div>
  )
}
