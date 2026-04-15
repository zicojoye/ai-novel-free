import { useNavigate } from 'react-router-dom'
import { useProjectStore } from '@/stores/projectStore'
import { useAuthStore } from '@/stores/authStore'
import { useState } from 'react'

interface HeaderProps {
  onCreateProject?: () => void
}

export default function Header({ onCreateProject }: HeaderProps) {
  const navigate = useNavigate()
  const currentProject = useProjectStore((state) => state.currentProject)
  const projects = useProjectStore((state) => state.projects)
  const { user, logout } = useAuthStore()
  const [showUserMenu, setShowUserMenu] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="border-b bg-card sticky top-0 z-40">
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          {/* 左侧：Logo 和 项目信息 */}
          <div className="flex items-center space-x-4">
            <div 
              className="text-2xl font-bold text-primary cursor-pointer hover:opacity-90"
              onClick={() => navigate('/')}
            >
              📚 AI Novel Platform
            </div>
            
            {/* 项目选择器 */}
            {projects.length > 0 && (
              <div className="hidden md:flex items-center space-x-2">
                <select
                  value={currentProject?.id || ''}
                  onChange={(e) => {
                    const project = projects.find((p) => p.id === Number(e.target.value))
                    if (project) {
                      useProjectStore.getState().setCurrentProject(project)
                      navigate(`/project/${project.id}`)
                    }
                  }}
                  className="px-3 py-1.5 text-sm border rounded-md bg-background"
                >
                  <option value="">选择项目</option>
                  {projects.map((project) => (
                    <option key={project.id} value={project.id}>
                      {project.name}
                    </option>
                  ))}
                </select>
              </div>
            )}
          </div>

          {/* 右侧：操作按钮和用户菜单 */}
          <div className="flex items-center space-x-3">
            {/* 新建项目按钮 */}
            <button
              onClick={onCreateProject}
              className="hidden sm:flex items-center space-x-2 px-4 py-2 text-sm bg-primary text-primary-foreground rounded-lg hover:opacity-90 transition-opacity"
            >
              <span>➕</span>
              <span>新建项目</span>
            </button>

            {/* 用户菜单 */}
            <div className="relative">
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="flex items-center space-x-2 px-3 py-2 rounded-lg hover:bg-accent transition-colors"
              >
                <div className="w-8 h-8 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-sm font-medium">
                  {user?.username?.charAt(0).toUpperCase() || 'U'}
                </div>
                <span className="hidden md:inline text-sm">{user?.username || '用户'}</span>
                <span className="text-xs">▼</span>
              </button>

              {/* 下拉菜单 */}
              {showUserMenu && (
                <>
                  <div 
                    className="fixed inset-0 z-10"
                    onClick={() => setShowUserMenu(false)}
                  />
                  <div className="absolute right-0 mt-2 w-48 bg-card border rounded-lg shadow-lg z-20">
                    <div className="p-3 border-b">
                      <div className="text-sm font-medium">{user?.username || '用户'}</div>
                      <div className="text-xs text-muted-foreground">{user?.email || 'user@example.com'}</div>
                    </div>
                    <div className="py-1">
                      <button
                        onClick={() => {
                          setShowUserMenu(false)
                          navigate('/settings')
                        }}
                        className="w-full text-left px-4 py-2 text-sm hover:bg-accent transition-colors"
                      >
                        ⚙️ 设置
                      </button>
                      <button
                        onClick={handleLogout}
                        className="w-full text-left px-4 py-2 text-sm text-destructive hover:bg-accent transition-colors"
                      >
                        🚪 退出登录
                      </button>
                    </div>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}
