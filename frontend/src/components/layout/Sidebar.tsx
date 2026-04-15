import { Link, useLocation } from 'react-router-dom'
import { useProjectStore } from '@/stores/projectStore'


const navItems = [
  { path: '/', label: '仪表盘', icon: '📊', requiresProject: false },
  { path: '/worldbuilding', label: '世界观', icon: '🌍', requiresProject: true },
  { path: '/chapter', label: '章节', icon: '📝', requiresProject: true },
  { path: '/plot', label: '剧情', icon: '📖', requiresProject: true },
  { path: '/knowledge', label: '知识库', icon: '📚', requiresProject: true },
  { path: '/agent', label: 'Agent', icon: '🤖', requiresProject: true },
  { path: '/prompts', label: '提示词', icon: '💬', requiresProject: false },
  { path: '/settings', label: '设置', icon: '⚙️', requiresProject: false },
]

interface SidebarProps {
  collapsed?: boolean
  onCollapse?: () => void
}

export default function Sidebar({ collapsed = false, onCollapse }: SidebarProps) {
  const location = useLocation()
  const currentProject = useProjectStore((state) => state.currentProject)

  return (
    <aside 
      className={`border-r bg-card min-h-screen transition-all duration-300 ${
        collapsed ? 'w-20' : 'w-64'
      }`}
    >
      {/* 折叠按钮 */}
      <div className="p-4 border-b">
        <button
          onClick={onCollapse}
          className="w-full flex items-center justify-center p-2 rounded-lg hover:bg-accent transition-colors"
          title={collapsed ? '展开侧边栏' : '收起侧边栏'}
        >
          {collapsed ? '▶' : '◀'}
        </button>
      </div>

      {/* 当前项目信息 */}
      {!collapsed && currentProject && (
        <div className="p-4 border-b">
          <div className="text-xs text-muted-foreground mb-1">当前项目</div>
          <div className="font-semibold text-sm truncate">{currentProject.name}</div>
          <div className="text-xs text-muted-foreground truncate">{currentProject.genre}</div>
        </div>
      )}

      {/* 导航菜单 */}
      <nav className="p-4 space-y-2">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path
          const isDisabled = item.requiresProject && !currentProject

          return (
            <Link
              key={item.path}
              to={item.path}
              onClick={(e) => isDisabled && e.preventDefault()}
              className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-primary text-primary-foreground'
                  : isDisabled
                  ? 'text-muted-foreground opacity-50 cursor-not-allowed'
                  : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
              }`}
              title={collapsed ? item.label : undefined}
            >
              <span className="text-lg">{item.icon}</span>
              {!collapsed && <span>{item.label}</span>}
              {!collapsed && isDisabled && (
                <span className="ml-auto text-xs">🔒</span>
              )}
            </Link>
          )
        })}
      </nav>
    </aside>
  )
}
