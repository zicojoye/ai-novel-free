import { useParams, useNavigate } from 'react-router-dom'
import PlotManager from '@/modules/plot/PlotManager'

export default function ProjectDetail() {
  const { id } = useParams<{ id: string }>()
  const projectId = parseInt(id || '0')
  const navigate = useNavigate()

  if (!id || isNaN(projectId)) {
    return (
      <div className="flex flex-col items-center justify-center h-64 text-center">
        <div className="text-6xl mb-4">😕</div>
        <h3 className="text-lg font-semibold mb-2">项目ID无效</h3>
        <button
          onClick={() => navigate('/')}
          className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90"
        >
          返回仪表盘
        </button>
      </div>
    )
  }

  return <PlotManager projectId={projectId} />
}
