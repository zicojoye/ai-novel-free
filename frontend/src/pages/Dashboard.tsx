import { useState } from 'react'
import { useProjectStore } from '@/stores/projectStore'
import { projectService } from '@/services/projectService'
import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { ConfirmDialog } from '@/components/common'
import { ProjectForm } from '@/components/project'
import { toast } from '@/lib/toast'

export default function Dashboard() {
  const projects = useProjectStore((state) => state.projects)
  const setProjects = useProjectStore((state) => state.setProjects)
  const setLoading = useProjectStore((state) => state.setLoading)
  const addProject = useProjectStore((state) => state.addProject)

  const [showCreateDialog, setShowCreateDialog] = useState(false)
  const [showDeleteDialog, setShowDeleteDialog] = useState(false)
  const [projectToDelete, setProjectToDelete] = useState<number | null>(null)

  useEffect(() => {
    loadProjects()
  }, [])

  const loadProjects = async () => {
    try {
      setLoading(true)
      const response = await projectService.getProjects({ page: 1, pageSize: 10 })
      if (Array.isArray(response)) {
        setProjects(response)
      } else if (response.success && response.data) {
        setProjects(Array.isArray(response.data) ? response.data : response.data.items || [])
      }
    } catch (error) {
      toast.error('加载项目失败,请稍后重试')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateProject = async (data: any) => {
    try {
      const response = await projectService.createProject(data)
      if (response.data) {
        addProject(response.data)
        setShowCreateDialog(false)
        toast.success('项目创建成功')
      }
    } catch (error) {
      toast.error('创建项目失败,请稍后重试')
    }
  }

  const handleDeleteProject = async () => {
    if (!projectToDelete) return
    try {
      await projectService.deleteProject(projectToDelete.toString())
      setProjects(projects.filter((p) => p.id !== projectToDelete))
      setShowDeleteDialog(false)
      setProjectToDelete(null)
      toast.success('项目删除成功')
    } catch (error) {
      toast.error('删除项目失败,请稍后重试')
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold">仪表盘</h2>
        <button
          onClick={() => setShowCreateDialog(true)}
          className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90"
        >
          新建项目
        </button>
      </div>

      {/* 统计卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-6 bg-card border rounded-lg">
          <div className="text-sm text-muted-foreground">总项目数</div>
          <div className="text-2xl font-bold mt-2">{projects.length}</div>
        </div>
        <div className="p-6 bg-card border rounded-lg">
          <div className="text-sm text-muted-foreground">活跃项目</div>
          <div className="text-2xl font-bold mt-2">
            {projects.filter((p) => p.status === 'active').length}
          </div>
        </div>
        <div className="p-6 bg-card border rounded-lg">
          <div className="text-sm text-muted-foreground">总章节数</div>
          <div className="text-2xl font-bold mt-2">0</div>
        </div>
        <div className="p-6 bg-card border rounded-lg">
          <div className="text-sm text-muted-foreground">总字数</div>
          <div className="text-2xl font-bold mt-2">0</div>
        </div>
      </div>

      {/* 项目列表 */}
      <div className="bg-card border rounded-lg p-6">
        <h3 className="text-xl font-semibold mb-4">最近项目</h3>
        {projects.length === 0 ? (
          <div className="text-center py-12 text-muted-foreground">
            <p>还没有项目</p>
            <p className="mt-2">点击"新建项目"开始创作</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {projects.map((project) => (
              <Link
                key={project.id}
                to={`/project/${project.id}`}
                className="block p-4 border rounded-lg hover:border-primary transition-colors"
              >
                <h4 className="font-semibold text-lg">{project.name}</h4>
                <p className="text-sm text-muted-foreground mt-1">{project.genre}</p>
                <div className="mt-2 flex items-center justify-between">
                  <span className="text-xs px-2 py-1 bg-secondary rounded">
                    {project.status}
                  </span>
                  <span className="text-xs text-muted-foreground">
                    {new Date(project.created_at).toLocaleDateString()}
                  </span>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>

      {/* 创建项目对话框 */}
      {showCreateDialog && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="bg-card border rounded-lg shadow-lg max-w-lg w-full mx-4 p-6">
            <h3 className="text-xl font-semibold mb-4">创建新项目</h3>
            <ProjectForm
              onSubmit={handleCreateProject}
              onCancel={() => setShowCreateDialog(false)}
            />
          </div>
        </div>
      )}

      {/* 删除确认对话框 */}
      <ConfirmDialog
        isOpen={showDeleteDialog}
        title="确认删除项目"
        message="删除后将无法恢复,是否继续?"
        confirmText="删除"
        cancelText="取消"
        type="danger"
        onConfirm={handleDeleteProject}
        onCancel={() => {
          setShowDeleteDialog(false)
          setProjectToDelete(null)
        }}
      />
    </div>
  )
}
