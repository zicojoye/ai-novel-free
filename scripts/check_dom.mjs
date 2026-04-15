// 用 http 请求获取页面，然后解析初始 HTML 检查是否有 #root 内容
import http from 'http'

function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    http.get(url, (res) => {
      let data = ''
      res.on('data', d => data += d)
      res.on('end', () => resolve({ status: res.statusCode, body: data }))
    }).on('error', reject)
  })
}

// 检查前端服务
const front = await fetchUrl('http://localhost:3000')
console.log('前端状态:', front.status)
console.log('前端HTML长度:', front.body.length)
const hasRoot = front.body.includes('id="root"')
const hasMainScript = front.body.includes('/src/main.tsx')
console.log('有 #root:', hasRoot)
console.log('有 main.tsx script:', hasMainScript)

// 检查后端
const back = await fetchUrl('http://localhost:8000/health')
console.log('\n后端状态:', back.status)
console.log('后端响应:', back.body)

const proj = await fetchUrl('http://localhost:8000/api/projects')
console.log('\n/api/projects 状态:', proj.status)
console.log('/api/projects 响应:', proj.body)
