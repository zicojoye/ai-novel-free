# WebSocket和记忆系统 API使用指南

## 📋 目录
- [WebSocket实时通信](#websocket实时通信)
- [聊天API](#聊天api)
- [记忆API](#记忆api)
- [事件流API](#事件流api)
- [Agent增强功能](#agent增强功能)

---

## WebSocket实时通信

### 1. 客户端连接
```javascript
// 连接到WebSocket
const ws = new WebSocket('ws://localhost:8000/ws/client_id_123');

ws.onopen = () => {
  console.log('WebSocket连接成功');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('收到消息:', data);

  // 处理不同类型的消息
  switch(data.type) {
    case 'message':
      // 聊天消息
      handleChatMessage(data);
      break;
    case 'event':
      // 事件流
      handleEvent(data);
      break;
    case 'mention':
      // 艾特通知
      handleMention(data);
      break;
    case 'task_update':
      // 任务更新
      handleTaskUpdate(data);
      break;
  }
};

// 发送消息
ws.send(JSON.stringify({
  type: 'message',
  room_id: 'workspace',
  content: '你好，Agent们！'
}));
```

### 2. Agent连接
```python
# Agent连接到WebSocket
import asyncio
from websockets import connect

async def agent_connect(agent_id: int):
    uri = f"ws://localhost:8000/ws/agent/{agent_id}"
    async with connect(uri) as websocket:
        print(f"Agent {agent_id} connected")

        # 监听消息
        while True:
            data = await websocket.recv()
            message = json.loads(data)

            # 处理艾特
            if message.get('type') == 'mention':
                await handle_mention(websocket, agent_id, message)

            # 处理其他消息
            elif message.get('type') == 'agent_message':
                await handle_agent_message(websocket, agent_id, message)
```

---

## 聊天API

### 1. 创建聊天房间
```bash
POST /api/chat/rooms
Content-Type: application/json

{
  "project_id": 1,
  "name": "核心创作团队",
  "room_type": "team",
  "member_ids": [1, 2, 3, 4],
  "created_by": 1,
  "description": "核心创作团队群聊"
}
```

### 2. 发送消息
```bash
POST /api/chat/messages
Content-Type: application/json

{
  "project_id": 1,
  "room_id": "workspace",
  "sender_id": 1,
  "sender_type": "agent",
  "content": "大家好，我开始创作新章节了",
  "mentions": [2, 3],
  "message_type": "text"
}
```

### 3. 获取房间消息
```bash
GET /api/chat/messages?room_id=workspace&limit=50
```

### 4. 创建工作室群聊
```bash
POST /api/chat/rooms/workspace?project_id=1
```

### 5. 创建团队群聊
```bash
POST /api/chat/rooms/team/核心创作?project_id=1
Content-Type: application/json

{
  "member_ids": [1, 2, 3, 4]
}
```

---

## 记忆API

### 1. Text2Mem 12个原子操作

#### 创建记忆
```bash
POST /api/memory
Content-Type: application/json

{
  "agent_id": 1,
  "project_id": 1,
  "content": "主角林风设定：25岁程序员，获得摸鱼变强系统",
  "memory_type": "ltm",
  "priority": "high",
  "summary": "主角设定",
  "tags": ["主角", "设定"]
}
```

#### 搜索记忆
```bash
POST /api/memory/operations/search?agent_id=1&query=主角&limit=10
```

#### 关联记忆
```bash
POST /api/memory/operations/link?memory_id=1&linked_memory_ids=[2,3,4]
```

#### 设置优先级
```bash
POST /api/memory/operations/prioritize?memory_id=1&priority=high
```

#### 归档记忆
```bash
POST /api/memory/operations/archive?memory_id=1
```

#### 回忆记忆
```bash
POST /api/memory/operations/recall?agent_id=1&context=主角&limit=5
```

#### 合并记忆
```bash
POST /api/memory/operations/merge?source_ids=[1,2,3]&target_id=4
```

#### 分割记忆
```bash
POST /api/memory/operations/split?memory_id=1&split_points=[100,200,300]
```

#### 验证记忆
```bash
POST /api/memory/operations/verify?memory_id=1
```

### 2. Mem0记忆中间件

#### 添加记忆
```bash
POST /api/memory/mem0/add?agent_id=1&project_id=1&content=记忆内容&importance=8.5&memory_type=stm
```

#### 获取相关记忆
```bash
GET /api/memory/mem0/relevant?agent_id=1&query=相关内容&limit=5
```

### 3. Agent独立知识库

#### 查询Agent知识库
```bash
GET /api/memory/agent-knowledge?agent_id=1&knowledge_type=character&limit=50
```

#### 查看记忆操作日志
```bash
GET /api/memory/1/logs?limit=50
```

---

## 事件流API

### 1. 创建事件
```bash
POST /api/events?project_id=1&event_type=task_start&source_id=1&source_type=agent&description=开始创作章节&importance=8
```

### 2. 获取项目事件
```bash
GET /api/events?project_id=1&limit=50
```

### 3. 获取分类事件
```bash
GET /api/events/project/1/categorized
```

返回示例：
```json
{
  "success": true,
  "categories": {
    "tasks": [...],
    "messages": [...],
    "memory": [...],
    "knowledge": [...],
    "system": [...],
    "errors": [...]
  }
}
```

### 4. 获取Agent事件
```bash
GET /api/events/agent/1?limit=50
```

### 5. 获取任务事件
```bash
GET /api/events/task/1?limit=50
```

### 6. 获取章节事件
```bash
GET /api/events/chapter/1?limit=50
```

### 7. 事件统计
```bash
GET /api/events/stats/1
```

返回示例：
```json
{
  "total": 150,
  "by_type": {
    "task_start": 30,
    "task_complete": 25,
    "agent_message": 50,
    ...
  },
  "by_importance": {
    1: 10,
    5: 50,
    8: 40,
    10: 50
  },
  "by_source": {
    "agent_1": 80,
    "agent_2": 40,
    "user_1": 30
  }
}
```

---

## Agent增强功能

### 1. EnhancedBaseAgent使用

```python
from app.agents.enhanced_agent import EnhancedBaseAgent
from app.models.memory import MemoryType, MemoryPriority
from app.models.chat import EventType

class MyAgent(EnhancedBaseAgent):
    def __init__(self, agent_id: int):
        super().__init__(
            agent_id=agent_id,
            name="我的Agent",
            role="author"
        )

    def get_system_prompt(self) -> str:
        return "你是一个专业的小说创作Agent..."

    async def execute(self, task: dict) -> dict:
        # 执行任务
        project_id = task.get("project_id")

        # 记忆到长期记忆
        await self.create_memory(
            project_id=project_id,
            content="开始创作第3章：主角首次激活系统",
            memory_type=MemoryType.LTM,
            priority=MemoryPriority.HIGH,
            tags=["章节", "激活", "系统"]
        )

        # 添加到Mem0
        await self.add_to_mem0(
            project_id=project_id,
            content="主角首次激活系统",
            importance=8.0
        )

        # 发送消息到群聊
        await self.send_message(
            project_id=project_id,
            room_id="workspace",
            content="我开始创作第3章了，主角即将激活系统！"
        )

        # 回忆相关记忆
        memories = await self.recall_memory(
            project_id=project_id,
            context="主角系统激活",
            limit=5
        )

        # 记录事件
        await self.log_event(
            project_id=project_id,
            event_type=EventType.TASK_START,
            description="开始创作第3章"
        )

        return {
            "success": True,
            "memories_used": len(memories)
        }

    async def process_mention(self, project_id: int, room_id: str,
                           sender_id: int, content: str):
        # 处理被艾特
        reply = await super().process_mention(
            project_id, room_id, sender_id, content
        )

        # 存储到工作记忆
        await self.create_memory(
            project_id=project_id,
            content=f"回复了{sender_id}: {content}",
            memory_type=MemoryType.WM,
            priority=MemoryPriority.LOW
        )

        return reply
```

### 2. Agent协作示例

```python
# 主创Agent艾特编辑Agent
await author_agent.send_message(
    project_id=1,
    room_id="workspace",
    content="@EditorAgent 请帮我润色这段文字",
    mentions=[2]
)

# 编辑Agent自动收到艾特并回复
# 1. WebSocket收到mention事件
# 2. 调用process_mention生成回复
# 3. 发送回复到群聊
# 4. 记录到事件流
# 5. 存储到工作记忆
```

---

## 🎯 完整工作流示例

### 场景：多Agent协作创作章节

```python
# 1. 主创Agent开始创作
result = await author_agent.execute({
    "type": "chapter",
    "project_id": 1,
    "chapter_number": 3,
    "outline": "主角首次激活系统"
})

# 2. 主创Agent发送消息到群聊
await author_agent.send_message(
    project_id=1,
    room_id="workspace",
    content="第3章大纲完成，开始创作！"
)

# 3. 编辑Agent收到消息，主动回复
await editor_agent.process_mention(
    project_id=1,
    room_id="workspace",
    sender_id=1,  # 主创Agent ID
    content="第3章大纲完成，开始创作！"
)

# 4. 审核Agent主动关注并记录
await reviewer_agent.create_memory(
    project_id=1,
    content="第3章需要重点检查主角系统激活的描写",
    memory_type=MemoryType.LTM,
    priority=MemoryPriority.HIGH,
    tags=["审核", "第3章", "系统激活"]
)

# 5. 所有Agent通过事件流实时了解进展
await event_service.create_event(
    project_id=1,
    event_type=EventType.TASK_PROGRESS,
    source_id=1,
    source_type="agent",
    description="主创Agent创作进度: 50%",
    data={"progress": 50, "word_count": 1000}
)

# 6. 前端实时显示所有事件
# WebSocket推送所有事件到连接的客户端
```

---

## 🔍 事件类型说明

| 事件类型 | 说明 | 来源 |
|---------|------|------|
| `task_start` | 任务开始 | Agent |
| `task_progress` | 任务进度更新 | Agent |
| `task_complete` | 任务完成 | Agent |
| `task_error` | 任务错误 | Agent |
| `agent_message` | Agent发送消息 | Agent |
| `agent_mention` | Agent被艾特 | Agent/User |
| `agent_response` | Agent回复 | Agent |
| `system_notice` | 系统通知 | System |
| `memory_update` | 记忆更新 | Agent |
| `knowledge_update` | 知识更新 | Agent |

---

## 💡 最佳实践

### 1. 记忆管理
- **短期记忆(STM)**: 临时会话信息，1-24小时
- **长期记忆(LTM)**: 永久知识，世界观、角色设定
- **工作记忆(WM)**: 推理过程，当前会话

### 2. 优先级设置
- **CRITICAL(10)**: 核心设定、主角金手指
- **HIGH(8)**: 重要剧情、关键角色
- **MEDIUM(5)**: 一般内容、配角
- **LOW(3)**: 临时信息、次要内容
- **TRIVIAL(1)**: 聊天、日常

### 3. 事件流使用
- 重要性1-3: 日常操作
- 重要性5: 一般任务
- 重要性8: 重要任务
- 重要性10: 关键事件

### 4. Agent协作
- 使用艾特明确目标
- 回复时提及原文
- 及时记录重要信息到记忆
- 通过事件流广播进展

---

**更新时间**: 2026年4月14日 08:43
