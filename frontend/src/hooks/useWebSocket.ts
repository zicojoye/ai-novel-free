import { useEffect, useState, useCallback } from 'react'
import { io, Socket } from 'socket.io-client'

interface WebSocketMessage {
  type: 'message' | 'event' | 'mention' | 'task_update' | 'pong'
  [key: string]: any
}

interface UseWebSocketOptions {
  projectId: number
  roomId: string
  onMessage?: (message: WebSocketMessage) => void
  onEvent?: (event: any) => void
  onMention?: (mention: any) => void
}

interface UseWebSocketReturn {
  isConnected: boolean
  messages: any[]
  typingUsers: any[]
  sendMessage: (data: any) => Promise<void>
  sendMention: (agentId: number) => Promise<void>
  disconnect: () => void
}

export function useWebSocket({
  projectId,
  roomId,
  onMessage,
  onEvent,
  onMention
}: UseWebSocketOptions): UseWebSocketReturn {
  const [socket, setSocket] = useState<Socket | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [messages, setMessages] = useState<any[]>([])
  const [typingUsers, setTypingUsers] = useState<any[]>([])
  const [pingInterval, setPingInterval] = useState<NodeJS.Timeout | null>(null)

  // 连接WebSocket
  useEffect(() => {
    // 使用原生WebSocket而不是socket.io（后端实现）
    const clientId = `client_${Math.random().toString(36).substr(2, 9)}`
    const wsUrl = `ws://localhost:8000/ws/${clientId}`
    
    const ws = new WebSocket(wsUrl)
    
    ws.onopen = () => {
      console.log('WebSocket connected')
      setIsConnected(true)
      
      // 订阅项目
      ws.send(JSON.stringify({
        type: 'subscribe',
        project_id: projectId
      }))
      
      // 开始心跳
      const interval = setInterval(() => {
        ws.send(JSON.stringify({ type: 'ping' }))
      }, 30000)
      setPingInterval(interval)
    }
    
    ws.onmessage = (event) => {
      try {
        const data: WebSocketMessage = JSON.parse(event.data)
        
        switch (data.type) {
          case 'message':
            setMessages(prev => [...prev, data])
            onMessage?.(data)
            break
            
          case 'event':
            onEvent?.(data)
            break
            
          case 'mention':
            onMention?.(data)
            break
            
          case 'typing':
            // 处理正在输入
            setTypingUsers(data.users || [])
            break
            
          case 'pong':
            // 心跳响应
            break
            
          case 'message_sent':
          case 'agent_message_sent':
            // 消息发送成功确认
            break
            
          case 'error':
            console.error('WebSocket error:', data.error)
            break
            
          default:
            console.log('Unknown message type:', data.type)
        }
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error)
      }
    }
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
      setIsConnected(false)
    }
    
    ws.onclose = () => {
      console.log('WebSocket disconnected')
      setIsConnected(false)
      
      // 清理心跳
      if (pingInterval) {
        clearInterval(pingInterval)
        setPingInterval(null)
      }
    }
    
    setSocket(ws as any)
    
    return () => {
      ws.close()
      if (pingInterval) {
        clearInterval(pingInterval)
      }
    }
  }, [projectId, roomId, onMessage, onEvent, onMention])

  // 发送消息
  const sendMessage = useCallback(async (data: any) => {
    if (!socket || !isConnected) {
      console.warn('WebSocket not connected')
      return
    }
    
    try {
      socket.send(JSON.stringify(data))
    } catch (error) {
      console.error('Failed to send message:', error)
      throw error
    }
  }, [socket, isConnected])

  // 发送艾特
  const sendMention = useCallback(async (agentId: number) => {
    // 发送消息会自动处理艾特
    console.log('Mention triggered for agent:', agentId)
  }, [])

  // 断开连接
  const disconnect = useCallback(() => {
    if (socket) {
      socket.close()
      setSocket(null)
      setIsConnected(false)
      
      if (pingInterval) {
        clearInterval(pingInterval)
        setPingInterval(null)
      }
    }
  }, [socket, pingInterval])

  return {
    isConnected,
    messages,
    typingUsers,
    sendMessage,
    sendMention,
    disconnect
  }
}
