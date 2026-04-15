import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig(({ mode }) => {
  // 加载环境变量
  const env = loadEnv(mode, process.cwd(), '')

  console.log(`\n📦 Vite Mode: ${mode}`)
  console.log(`🔗 API Base URL: ${env.VITE_API_BASE_URL}`)
  console.log(`🌐 Port: ${env.VITE_PORT}`)
  console.log(`\n`)

  return {
    plugins: [react()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    server: {
      // 前端开发服务器端口
      port: parseInt(env.VITE_PORT) || 3000,
      host: true, // 监听所有地址,支持局域网访问
      strictPort: false, // 端口被占用时自动尝试下一个端口

      // 代理配置
      proxy: {
        // API代理到后端
        '/api': {
          // 如果VITE_API_BASE_URL是完整URL(如http://localhost:8000),则使用它
          // 如果是相对路径(如/api),则默认使用http://localhost:8000
          target: env.VITE_API_BASE_URL?.startsWith('http')
            ? env.VITE_API_BASE_URL
            : 'http://localhost:8000',
          changeOrigin: true,
          // 路径重写: 前端请求 /api/xxx -> 后端接收 /api/xxx
          // 直接透传路径,不做修改,因为后端路由就是 /api/xxx
          rewrite: (path) => path,
          // 代理超时时间
          proxyTimeout: 60000,
          // WebSocket支持
          ws: true,
          // 配置请求头
          configure: (proxy, options) => {
            proxy.on('proxyReq', (proxyReq, req, res) => {
              console.log(`[Proxy] ${req.method} ${req.url} -> ${options.target}${req.url}`)
            })
            proxy.on('proxyRes', (proxyRes, req, res) => {
              console.log(`[Proxy] Response ${req.url} -> ${proxyRes.statusCode}`)
            })
          },
        },

        // 健康检查接口代理
        '/health': {
          target: env.VITE_API_BASE_URL?.startsWith('http')
            ? env.VITE_API_BASE_URL
            : 'http://localhost:8000',
          changeOrigin: true,
        },

        // 文档接口代理
        '/docs': {
          target: env.VITE_API_BASE_URL?.startsWith('http')
            ? env.VITE_API_BASE_URL
            : 'http://localhost:8000',
          changeOrigin: true,
        },

        // 静态文件代理 (如果需要)
        '/static': {
          target: env.VITE_API_BASE_URL?.startsWith('http')
            ? env.VITE_API_BASE_URL
            : 'http://localhost:8000',
          changeOrigin: true,
        },
      },

      // HMR配置
      hmr: {
        overlay: true, // 显示错误覆盖层
      },

      // CORS配置 (开发环境)
      cors: {
        origin: true,
        credentials: true,
      },

      // 监听文件变化
      watch: {
        usePolling: false, // 在某些网络共享环境下可能需要设为true
      },
    },

    // 构建配置
    build: {
      outDir: 'dist',
      assetsDir: 'assets',
      sourcemap: mode === 'development', // 开发环境生成sourcemap
      minify: 'esbuild',
      esbuildOptions: {
        drop: mode === 'production' ? ['console', 'debugger'] : [],
      },
      rollupOptions: {
        output: {
          manualChunks: {
            // 分包优化
            'react-vendor': ['react', 'react-dom', 'react-router-dom'],
            'ui-vendor': ['framer-motion', 'lucide-react'],
            'utils-vendor': ['axios', 'zustand', '@tanstack/react-query'],
          },
        },
      },
      // 限制chunk大小
      chunkSizeWarningLimit: 1000,
    },

    // 预览服务器配置
    preview: {
      port: 4173,
      host: true,
      proxy: {
        '/api': {
          target: env.VITE_API_BASE_URL?.startsWith('http')
            ? env.VITE_API_BASE_URL
            : 'http://localhost:8000',
          changeOrigin: true,
          rewrite: (path) => path,
        },
      },
    },

    // 依赖优化
    optimizeDeps: {
      include: [
        'react',
        'react-dom',
        'react-router-dom',
        'zustand',
        'axios',
        '@tanstack/react-query',
      ],
    },

    // 定义全局常量
    define: {
      __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
      __BUILD_TIME__: JSON.stringify(new Date().toISOString()),
    },
  }
})
