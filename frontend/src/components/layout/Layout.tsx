import { useState } from 'react'
import { useProjectStore } from '@/stores/projectStore'
import { Sidebar, Header, MainContent, MobileNav } from './'

export default function Layout({ children }: { children: React.ReactNode }) {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [mobileNavOpen, setMobileNavOpen] = useState(false)
  const currentProject = useProjectStore((state) => state.currentProject)

  const handleCreateProject = () => {
    // 触发创建项目对话框
    window.dispatchEvent(new CustomEvent('open-create-project'))
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <Header onCreateProject={handleCreateProject} />

      {/* 主体布局 */}
      <div className="flex">
        {/* Desktop Sidebar */}
        <div className="hidden md:block">
          <Sidebar 
            collapsed={sidebarCollapsed} 
            onCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
          />
        </div>

        {/* Mobile Navigation */}
        <MobileNav 
          isOpen={mobileNavOpen}
          onClose={() => setMobileNavOpen(false)}
        />

        {/* Mobile Menu Toggle */}
        <div className="fixed bottom-4 left-4 md:hidden z-40">
          <button
            onClick={() => setMobileNavOpen(!mobileNavOpen)}
            className="w-12 h-12 bg-primary text-primary-foreground rounded-full shadow-lg flex items-center justify-center"
          >
            ☰
          </button>
        </div>

        {/* Main Content */}
        <MainContent>
          {/* 无项目提示 */}
          {!currentProject && !['/', '/settings', '/prompts'].includes(window.location.pathname) && (
            <div className="flex flex-col items-center justify-center py-20 text-center">
              <div className="text-6xl mb-4">📋</div>
              <h2 className="text-2xl font-bold mb-2">请先选择一个项目</h2>
              <p className="text-muted-foreground mb-4 max-w-md">
                您需要先创建或选择一个项目才能使用此功能
              </p>
              <button
                onClick={handleCreateProject}
                className="px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:opacity-90"
              >
                创建新项目
              </button>
            </div>
          )}
          {children}
        </MainContent>
      </div>
    </div>
  )
}
