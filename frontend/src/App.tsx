import { Routes, Route } from 'react-router-dom'
import Layout from '@/components/layout/Layout'
import Dashboard from '@/pages/Dashboard'
import ProjectDetail from '@/pages/ProjectDetail'
import WorldBuilding from '@/modules/worldbuilding/WorldBuilding'
import ChapterEditor from '@/modules/chapter/ChapterEditor'
import PlotManager from '@/modules/plot/PlotManager'
import KnowledgeBase from '@/modules/knowledge/KnowledgeBase'
import AgentMonitor from '@/modules/agent/AgentMonitor'
import PromptLibrary from '@/modules/prompts/PromptLibrary'
import Settings from '@/pages/Settings'
import NotFound from '@/pages/NotFound'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/project/:id" element={<ProjectDetail />} />
        <Route path="/worldbuilding" element={<WorldBuilding />} />
        <Route path="/chapter" element={<ChapterEditor />} />
        <Route path="/plot" element={<PlotManager />} />
        <Route path="/knowledge" element={<KnowledgeBase />} />
        <Route path="/agent" element={<AgentMonitor />} />
        <Route path="/prompts" element={<PromptLibrary />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Layout>
  )
}

export default App
