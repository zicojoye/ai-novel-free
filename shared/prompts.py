#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提示词模板库 - 系统提示词和用户提示词模板
"""

from typing import Dict, Any


class PromptTemplates:
    """提示词模板库"""
    
    # 系统提示词
    SYSTEM_PROMPTS = {
        "author": """你是一位专业的小说作者,擅长创作都市脑洞+反套路系统+灵气复苏类型的小说。
请遵循以下规则:
1. 爽点节奏:每章≥2小爽点、每3章1中爽点、每10章1高潮、每1万字1反转、压抑不超2章
2. 用词规范:使用"叮!"、"系统提示:"等节奏词
3. 避坑红线:主角不圣母且受辱即反击、反派有合理动机、不堆背景、战力有逻辑、内容合规
4. 语言风格:口语化、快节奏、面向下沉市场25-35岁职场男性读者
5. 章节长度:每章必须达到1000字以上,完整展开对话、动作、心理、环境细节
""",
        
        "editor": """你是一位专业的小说编辑,负责润色和优化小说内容。
请关注以下方面:
1. 检查语法错误和错别字
2. 优化句子结构,提升流畅度
3. 增强场景描写和人物刻画
4. 确保节奏紧凑,不拖沓
5. 保持作者原有风格
""",
        
        "reviewer": """你是一位专业的小说审稿人,负责质量把控和逻辑检查。
请检查以下方面:
1. 剧情逻辑是否合理
2. 人物行为是否一致
3. 伏笔和钩子是否合理设置
4. 是否存在矛盾或bug
5. 内容是否合规
""",
        
        "world_builder": """你是一位专业的世界观构建专家,负责完善小说的世界观设定。
请确保世界观具备以下特点:
1. 内在逻辑自洽
2. 具有足够的扩展性
3. 能够支撑剧情发展
4. 符合小说类型特征
5. 细节丰富但不冗余
""",
        
        "knowledge_manager": """你是一位专业的知识库管理员,负责从文本中提取和管理知识。
请关注:
1. 识别关键人物、地点、物品、技能
2. 提取重要情节和伏笔
3. 建立知识之间的关联
4. 确保知识的准确性和完整性
"""
    }
    
    # 用户提示词模板
    USER_PROMPTS = {
        "generate_chapter": """根据以下信息生成小说章节:

项目信息:
- 项目名称: {project_name}
- 小说类型: {genre}
- 当前章节: 第{chapter_number}章
- 章节标题: {chapter_title}
- 目标字数: {target_words}字

上下文:
{context}

要求:
1. 按照番茄爆款铁律创作
2. 确保章节字数达到{target_words}字以上
3. 包含至少2个小爽点
4. 完整展开对话、动作、心理、环境细节
5. 语言口语化、快节奏
""",
        
        "polish_chapter": """请润色以下章节内容:

章节标题: {chapter_title}
原内容:
{content}

润色要求:
1. 保持原有情节和风格
2. 修正语法错误和错别字
3. 优化句子结构,提升流畅度
4. 增强场景描写和细节刻画
5. 确保节奏紧凑
""",
        
        "generate_worldbuilding": """请生成世界观设定:

维度: {dimension}
项目背景: {project_context}
相关内容:
{related_content}

要求:
1. 符合都市脑洞+反套路系统+灵气复苏类型
2. 逻辑自洽,细节丰富
3. 能够支撑后续剧情发展
4. 字数500-1000字
""",
        
        "check_plot_consistency": """请检查以下剧情是否存在逻辑矛盾:

当前剧情:
{current_plot}

相关历史剧情:
{history_plots}

检查点:
1. 人物行为是否一致
2. 事件时间线是否合理
3. 设定是否前后冲突
4. 是否存在逻辑bug

请列出发现的问题,并给出修改建议。
""",
        
        "extract_knowledge": """请从以下文本中提取关键知识条目:

文本内容:
{text}

提取要求:
1. 识别关键人物(名字、身份、特征)
2. 识别重要地点
3. 识别特殊物品/技能
4. 识别重要情节和伏笔
5. 建立知识之间的关联

以JSON格式返回。
""",
        
        "generate_outline": """请根据以下信息生成大纲:

项目信息:
- 项目名称: {project_name}
- 小说类型: {genre}
- 总章节目标: {total_chapters}章
- 当前进度: 已写{current_chapters}章

已有内容:
{existing_content}

要求:
1. 确保主线清晰,结构完整
2. 合理安排爽点节奏
3. 设置合理的伏笔和钩子
4. 每章简要描述剧情要点
5. 字数约2000-3000字
""",
        
        "generate_beat_sheet": """请为以下章节生成节拍表:

章节信息:
- 第{chapter_number}章: {chapter_title}
- 大纲要点: {outline}

节拍表要求:
1. 包含8-12个主要节拍
2. 标注每个节拍的字数
3. 明确节拍的情感节奏
4. 确保节奏张弛有度
5. 总字数符合章节目标
"""
    }
    
    @classmethod
    def get_system_prompt(cls, agent_type: str) -> str:
        """获取系统提示词"""
        return cls.SYSTEM_PROMPTS.get(agent_type, "")
    
    @classmethod
    def get_user_prompt(cls, prompt_type: str, **kwargs) -> str:
        """获取用户提示词模板"""
        template = cls.USER_PROMPTS.get(prompt_type, "")
        return template.format(**kwargs)
    
    @classmethod
    def format_prompt(cls, agent_type: str, prompt_type: str, **kwargs) -> Dict[str, str]:
        """格式化完整提示词"""
        return {
            "system": cls.get_system_prompt(agent_type),
            "user": cls.get_user_prompt(prompt_type, **kwargs)
        }


# 预设提示词模板(供用户自定义)
PRESET_TEMPLATES = {
    "黄金三章": {
        "name": "黄金三章模板",
        "description": "番茄爆款黄金三章模板,确保开篇300字内冲突拉仇恨,1章激活金手指,3章兑现爽点",
        "template": """第1章:
- 开篇300字内必须拉仇恨,制造冲突
- 引出主角困境或危机
- 为系统激活做铺垫

第2章:
- 激活金手指(摸鱼变强系统)
- 主角获得初步能力
- 第一次爽点

第3章:
- 兑现爽点,展示系统效果
- 留下悬念和钩子
- 引导读者期待后续
"""
    },
    
    "爽点公式": {
        "name": "爽点公式模板",
        "description": "标准爽点公式:压抑→爆发→装逼打脸→收获",
        "template": """1. 压抑:反派挑衅/主角受辱/危机逼近
2. 爆发:系统激活/主角反击
3. 装逼打脸:展示实力/反派震惊
4. 收获:获得奖励/升级/收获资源
"""
    },
    
    "伏笔设置": {
        "name": "伏笔设置模板",
        "description": "如何有效设置伏笔和钩子",
        "template": """伏笔设置三要素:
1. 提前埋下:在前文自然提及
2. 合理呼应:后文回应前文
3. 逻辑严密:符合世界观设定

钩子类型:
- 悬念钩子:留疑问
- 剧情钩子:引后续
- 情感钩子:引期待
"""
    }
}
