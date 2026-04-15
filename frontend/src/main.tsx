import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { ErrorBoundary } from '@/components/error/ErrorBoundary'
import { ToastContainer } from '@/components/ui/ToastContainer'
import App from './App'
import { queryClient } from './lib/queryClient'
import './index.css'

// 全局错误捕获 - 白屏诊断
window.addEventListener('error', (e) => {
  console.error('[GlobalError]', e.message, e.filename, e.lineno)
  const root = document.getElementById('root')
  if (root && root.innerHTML === '') {
    root.innerHTML = `<div style="padding:20px;font-family:monospace;background:#fee;border:2px solid red;margin:20px;border-radius:8px">
      <h2 style="color:red">渲染错误（白屏诊断）</h2>
      <p><b>错误信息：</b>${e.message}</p>
      <p><b>文件：</b>${e.filename}</p>
      <p><b>行号：</b>${e.lineno}</p>
      <p><b>错误详情：</b>${e.error?.stack || '无'}</p>
    </div>`
  }
})

window.addEventListener('unhandledrejection', (e) => {
  console.error('[UnhandledPromise]', e.reason)
  const root = document.getElementById('root')
  if (root && root.innerHTML === '') {
    root.innerHTML = `<div style="padding:20px;font-family:monospace;background:#fee;border:2px solid red;margin:20px;border-radius:8px">
      <h2 style="color:red">Promise 错误（白屏诊断）</h2>
      <p>${e.reason?.message || String(e.reason)}</p>
      <p>${e.reason?.stack || ''}</p>
    </div>`
  }
})

try {
  ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
      <ErrorBoundary>
        <QueryClientProvider client={queryClient}>
          <BrowserRouter>
            <App />
          </BrowserRouter>
          <ToastContainer />
          {process.env.NODE_ENV === 'development' && (
            <ReactQueryDevtools
              initialIsOpen={false}
              position="bottom-right"
            />
          )}
        </QueryClientProvider>
      </ErrorBoundary>
    </React.StrictMode>,
  )
} catch (e: any) {
  document.getElementById('root')!.innerHTML = `<div style="padding:20px;font-family:monospace;background:#fee;border:2px solid red;margin:20px;border-radius:8px">
    <h2 style="color:red">React 启动失败（白屏诊断）</h2>
    <p><b>错误：</b>${e?.message}</p>
    <pre style="overflow:auto;background:#fff;padding:10px;border-radius:4px">${e?.stack}</pre>
  </div>`
}
