import { Link, useLocation } from 'react-router-dom'

const navItems = [
  { path: '/', label: '仪表盘', icon: '📊' },
  { path: '/worldbuilding', label: '世界观', icon: '🌍' },
  { path: '/chapter', label: '章节', icon: '📝' },
  { path: '/plot', label: '剧情', icon: '📖' },
  { path: '/knowledge', label: '知识库', icon: '📚' },
  { path: '/agent', label: 'Agent', icon: '🤖' },
]

interface MobileNavProps {
  isOpen: boolean
  onClose: () => void
}

export default function MobileNav({ isOpen, onClose }: MobileNavProps) {
  const location = useLocation()

  if (!isOpen) return null

  return (
    <>
      {/* 遮罩层 */}
      <div 
        className="fixed inset-0 bg-black/50 z-40 md:hidden"
        onClick={onClose}
      />
      
      {/* 移动端侧边栏 */}
      <aside className="fixed left-0 top-0 bottom-0 w-64 bg-card border-r z-50 md:hidden">
        {/* 关闭按钮 */}
        <div className="p-4 border-b flex items-center justify-between">
          <div className="font-bold text-lg">📚 AI Novel</div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-accent transition-colors"
          >
            ✕
          </button>
        </div>

        {/* 导航菜单 */}
        <nav className="p-4 space-y-2">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path
            return (
              <Link
                key={item.path}
                to={item.path}
                onClick={onClose}
                className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                  isActive
                    ? 'bg-primary text-primary-foreground'
                    : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                }`}
              >
                <span className="text-lg">{item.icon}</span>
                <span>{item.label}</span>
              </Link>
            )
          })}
        </nav>
      </aside>
    </>
  )
}
