import { Link } from 'react-router-dom'
import type { Project } from '@/types'

interface ProjectCardProps {
  project: Project
}

export function ProjectCard({ project }: ProjectCardProps) {
  const statusColors = {
    draft: 'bg-gray-100 text-gray-800',
    active: 'bg-green-100 text-green-800',
    completed: 'bg-blue-100 text-blue-800',
    archived: 'bg-purple-100 text-purple-800',
  }

  return (
    <Link
      to={`/project/${project.id}`}
      className="block p-6 bg-card border rounded-lg hover:border-primary hover:shadow-md transition-all duration-200"
    >
      <div className="flex items-start justify-between mb-3">
        <h4 className="text-lg font-semibold line-clamp-1">{project.name}</h4>
        <span className={`text-xs px-2 py-1 rounded-full ${statusColors[project.status]}`}>
          {project.status === 'draft' && '草稿'}
          {project.status === 'active' && '进行中'}
          {project.status === 'completed' && '已完成'}
          {project.status === 'archived' && '已归档'}
        </span>
      </div>
      {project.description && (
        <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
          {project.description}
        </p>
      )}
      <div className="flex items-center justify-between text-xs text-muted-foreground">
        <span className="px-2 py-1 bg-secondary rounded">{project.genre}</span>
        <span>{new Date(project.created_at).toLocaleDateString()}</span>
      </div>
    </Link>
  )
}
