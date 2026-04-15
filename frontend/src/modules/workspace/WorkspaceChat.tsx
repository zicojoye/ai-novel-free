import { useEffect, useState, useRef } from 'react'
import { Send, Paperclip, Smile, MoreVertical, Users, Clock, Activity } from 'lucide-react'
import { useWebSocket } from '@/hooks/useWebSocket'
import { parseMentions } from '@/lib/chat'

interface ChatMessage {
  id: number
  room_id: string
  sender_id: number
  sender_type: 'agent' | 'user'
  content: string
  mentions?: number[]
  message_type: 'text' | 'image' | 'file'
  timestamp: string
  reply_to_id?: number
}

interface Agent {
  id: number
  name: string
  role: string
  status: 'idle' | 'active' | 'completed' | 'error'
  avatar?: string
}

interface WorkspaceChatProps {
  projectId: number
  roomType: 'workspace' | 'team'
  teamId?: string
}

export default function WorkspaceChat({ projectId, roomType, teamId }: WorkspaceChatProps) {
  const roomId = roomType === 'workspace' ? 'workspace' : `team_${teamId}`
  
  // WebSocket连接
  const { isConnected, messages, sendMessage, typingUsers } = useWebSocket({
    projectId,
    roomId
  })
  
  const [messageInput, setMessageInput] = useState('')
  const [replyingTo, setReplyingTo] = useState<ChatMessage | null>(null)
  const [showMentions, setShowMentions] = useState(false)
  const [mentionedAgents] = useState<Agent[]>([])
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  // 自动滚动到最新消息
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // 处理输入变化
  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value
    setMessageInput(value)
    
    // 检测@符号，显示艾特列表
    const lastChar = value.slice(-1)
    if (lastChar === '@') {
      setShowMentions(true)
    } else if (lastChar === ' ' && showMentions) {
      setShowMentions(false)
    }
  }

  // 发送消息
  const handleSendMessage = async () => {
    if (!messageInput.trim()) return

    // 解析艾特
    const mentions = parseMentions(messageInput)
    
    await sendMessage({
      type: 'message',
      room_id: roomId,
      sender_type: 'user',
      content: messageInput,
      mentions: mentions,
      reply_to_id: replyingTo?.id,
      message_type: 'text'
    })

    setMessageInput('')
    setReplyingTo(null)
    setShowMentions(false)
  }

  // 按Enter发送
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  // 选择艾特
  const handleMentionSelect = (agent: Agent) => {
    const currentInput = messageInput
    const lastAtIndex = currentInput.lastIndexOf('@')
    const newInput = currentInput.slice(0, lastAtIndex) + `@${agent.name} `
    setMessageInput(newInput)
    setShowMentions(false)
    inputRef.current?.focus()
  }

  // 回复消息
  const handleReply = (message: ChatMessage) => {
    setReplyingTo(message)
    inputRef.current?.focus()
  }

  // 渲染消息
  const renderMessage = (message: ChatMessage) => {
    const isOwn = message.sender_type === 'user'
    const agent = getAgentInfo(message.sender_id)
    
    return (
      <div
        key={message.id}
        className={`flex flex-col mb-4 ${isOwn ? 'items-end' : 'items-start'}`}
      >
        {/* 头像和发送者 */}
        {!isOwn && (
          <div className="flex items-end gap-2">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white font-bold">
              {agent?.name?.[0] || 'A'}
            </div>
            <div className="flex flex-col">
              <div className="font-semibold text-sm">{agent?.name || 'Unknown'}</div>
              <div className="text-xs text-muted-foreground">
                {new Date(message.timestamp).toLocaleTimeString()}
              </div>
            </div>
          </div>
        )}

        {/* 消息内容 */}
        <div
          className={`max-w-md rounded-2xl p-4 ${
            isOwn
              ? 'bg-primary text-primary-foreground'
              : 'bg-card border'
          }`}
        >
          {message.reply_to_id && (
            <div className="text-xs opacity-60 mb-2">
              回复某条消息
            </div>
          )}

          <div className="break-words">
            {renderContentWithMentions(message.content, message.mentions, isOwn)}
          </div>
        </div>

        {/* 操作按钮 */}
        <div className="flex gap-2 text-xs text-muted-foreground mt-1">
          <button
            onClick={() => handleReply(message)}
            className="hover:text-foreground"
          >
            回复
          </button>
          <button
            className="hover:text-foreground"
          >
            转发
          </button>
        </div>

        {/* 自己的头像 */}
        {isOwn && (
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center text-white font-bold">
            我
          </div>
        )}
      </div>
    )
  }

  // 渲染包含艾特的内容
  const renderContentWithMentions = (
    content: string,
    mentions: number[] | undefined,
    _isOwn: boolean
  ) => {
    if (!mentions || mentions.length === 0) return content

    // TODO: 实现@替换为Agent名字
    return content
  }

  // 获取Agent信息
  const getAgentInfo = (_agentId: number): Agent | undefined => {
    // TODO: 从状态或API获取Agent信息
    return undefined
  }

  return (
    <div className="flex flex-col h-full">
      {/* 头部 */}
      <div className="border-b p-4 flex items-center justify-between bg-card">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <Users className="w-5 h-5 text-muted-foreground" />
            <h2 className="text-lg font-semibold">
              {roomType === 'workspace' ? '工作室' : '团队'}群聊
            </h2>
          </div>
          <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
        </div>

        <div className="flex items-center gap-2">
          {/* 在线Agent列表 */}
          <div className="flex -space-x-2">
            {[1, 2, 3, 4].map(id => (
              <div
                key={id}
                className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white text-xs font-bold border-2 border-background"
                title={`Agent ${id}`}
              >
                {id}
              </div>
            ))}
          </div>

          <button className="p-2 hover:bg-accent rounded-lg transition-colors">
            <MoreVertical className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* 正在输入 */}
      {typingUsers.length > 0 && (
        <div className="px-4 py-2 bg-accent/50 text-sm text-muted-foreground">
          {typingUsers.map(agent => agent.name).join(', ')} 正在输入...
        </div>
      )}

      {/* 消息列表 */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-muted-foreground py-8">
            <Users className="w-16 h-16 mx-auto mb-4 opacity-50" />
            <p className="text-lg mb-2">欢迎来到{roomType === 'workspace' ? '工作室' : '团队'}群聊</p>
            <p className="text-sm">Agent们可以在这里实时协作、讨论创作问题</p>
          </div>
        ) : (
          <>
            {messages.map(renderMessage)}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* 艾特列表 */}
      {showMentions && mentionedAgents.length > 0 && (
        <div className="absolute bottom-24 left-4 right-4 bg-card border rounded-lg shadow-lg max-h-48 overflow-y-auto">
          <div className="p-2">
            {mentionedAgents.map(agent => (
              <button
                key={agent.id}
                onClick={() => handleMentionSelect(agent)}
                className="w-full text-left px-3 py-2 hover:bg-accent rounded transition-colors flex items-center gap-3"
              >
                <div className={`w-8 h-8 rounded-full ${
                  agent.status === 'active' ? 'bg-green-500' :
                  agent.status === 'idle' ? 'bg-gray-400' :
                  'bg-red-500'
                } flex items-center justify-center text-white text-xs font-bold`}>
                  {agent.name[0]}
                </div>
                <div className="flex-1">
                  <div className="font-medium">{agent.name}</div>
                  <div className="text-xs text-muted-foreground">{agent.role}</div>
                </div>
                <div className={`w-2 h-2 rounded-full ${
                  agent.status === 'active' ? 'bg-green-500' :
                  agent.status === 'idle' ? 'bg-gray-400' :
                  'bg-red-500'
                }`} />
              </button>
            ))}
          </div>
        </div>
      )}

      {/* 回复预览 */}
      {replyingTo && (
        <div className="px-4 py-2 bg-accent/50 text-sm flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-full bg-muted flex items-center justify-center">
              <Clock className="w-3 h-3" />
            </div>
            <span>回复: {replyingTo.content.slice(0, 50)}...</span>
          </div>
          <button
            onClick={() => setReplyingTo(null)}
            className="text-muted-foreground hover:text-foreground"
          >
            ✕
          </button>
        </div>
      )}

      {/* 输入框 */}
      <div className="border-t p-4 bg-card">
        <div className="flex gap-2">
          {/* 附件按钮 */}
          <button className="p-2 hover:bg-accent rounded-lg transition-colors">
            <Paperclip className="w-5 h-5 text-muted-foreground" />
          </button>

          {/* 输入框 */}
          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              value={messageInput}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              placeholder={`在${roomType === 'workspace' ? '工作室' : '团队'}群聊发言... (按Enter发送，Shift+Enter换行)`}
              className="w-full min-h-[80px] max-h-[200px] p-3 border rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          {/* 表情按钮 */}
          <button className="p-2 hover:bg-accent rounded-lg transition-colors">
            <Smile className="w-5 h-5 text-muted-foreground" />
          </button>

          {/* 发送按钮 */}
          <button
            onClick={handleSendMessage}
            disabled={!messageInput.trim()}
            className="px-6 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90 disabled:opacity-50 transition-opacity"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  )
}
