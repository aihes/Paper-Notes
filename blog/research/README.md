# AI 技术博客研究资料库

📅 更新日期: 2026-01-15

## 📁 目录结构

```
blog/research/
├── README.md                          # 本文件
├── ARTICLE_TOPICS_ANALYSIS.md         # 文章选题分析报告 ⭐
├── anthropic/                         # Anthropic 博客内容
│   ├── 01-engineering-blog-overview.md
│   ├── 02-newsroom-highlights.md
│   └── 03-economic-index-primitives.md
└── langchain/                         # LangChain 博客内容
    ├── 01-blog-overview.md
    ├── 02-multi-agent-architecture.md
    ├── 03-agent-engineering-discipline.md
    └── 04-deepagents-overview.md
```

## 🎯 快速导航

### 📊 文章选题分析
**[ARTICLE_TOPICS_ANALYSIS.md](./ARTICLE_TOPICS_ANALYSIS.md)** - 完整的技术文章选题分析报告

**核心推荐:**
1. **Agent Engineering 实践指南** (最高优先级 ⭐⭐⭐⭐⭐)
2. **多 Agent 架构设计完全指南** (⭐⭐⭐⭐⭐)
3. **AI 经济影响量化研究** (⭐⭐⭐⭐⭐)

### 📚 Anthropic 内容

#### 1. 工程博客总览
**文件:** [anthropic/01-engineering-blog-overview.md](./anthropic/01-engineering-blog-overview.md)

**核心主题:**
- Agent 评估与测试
- 长时程 Agent 架构
- 高级工具使用模式
- MCP (Model Context Protocol)
- 多 Agent 系统

**最新文章 (2025):**
- Demystifying evals for AI agents
- Effective harnesses for long-running agents
- Advanced tool use on Claude Platform
- Code execution with MCP

#### 2. 新闻发布重点
**文件:** [anthropic/02-newsroom-highlights.md](./anthropic/02-newsroom-highlights.md)

**产品发布:**
- Claude Opus 4.5 (Nov 24, 2025) - 编程/Agent/Computer Use 最佳
- Claude Sonnet 4.5 (Sep 29, 2025) - 基准记录 + 最对齐
- Claude Haiku 4.5 (Oct 15, 2025) - 速度与成本效率

**公司里程碑:**
- Series F: $13B @ $183B 估值
- 收入增长: $1B → $5B (8 个月)

**重要合作:**
- Accenture, Snowflake, DOE
- MCP 捐赠给 Agentic AI Foundation

#### 3. 经济指数研究
**文件:** [anthropic/03-economic-index-primitives.md](./anthropic/03-economic-index-primitives.md)

**五大经济原语:**
1. Task Complexity - 任务复杂度
2. Skill Level - 技能水平
3. Purpose - 使用目的
4. AI Autonomy - AI 自主性
5. Success Rate - 成功率

**关键数据:**
- 大学学历任务: 12x 加速
- 职业覆盖率: 49% (25%+ 任务)
- 生产力增长: 1.0-1.8 pp/年

### 📚 LangChain 内容

#### 1. 博客总览
**文件:** [langchain/01-blog-overview.md](./langchain/01-blog-overview.md)

**核心产品:**
- LangSmith Agent Builder (GA)
- Deep Agents Framework
- LangGraph v1.0

**主要主题:**
- Agent Engineering 新学科
- Multi-Agent 架构
- Debugging 工具 (Fetch, Polly)
- Deep Agents 评估

#### 2. 多 Agent 架构
**文件:** [langchain/02-multi-agent-architecture.md](./langchain/02-multi-agent-architecture.md)

**四大模式:**
1. **Subagents** - 中心化编排
2. **Skills** - 渐进式披露
3. **Handoffs** - 状态驱动
4. **Router** - 并行分发

**性能数据:**
- Anthropic 案例: 90.2% 提升
- 重复请求: 40-50% 效率提升
- 多领域查询: 67% token 优化

**决策框架:**
- 何时使用哪种模式
- 性能对比矩阵
- 实现建议

#### 3. Agent Engineering 学科
**文件:** [langchain/03-agent-engineering-discipline.md](./langchain/03-agent-engineering-discipline.md)

**核心概念:**
- 定义: 非确定性系统的生产化
- 循环: Build → Test → Ship → Observe → Refine
- 三大技能: 产品 + 工程 + 数据

**关键洞察:**
- 生产即学习
- 每个输入都是边缘情况
- "工作"不是二元的

**成功案例:**
- Clay, LinkedIn, Vanta, Cloudflare
- Vodafone 客服转型

#### 4. Deep Agents 框架
**文件:** [langchain/04-deepagents-overview.md](./langchain/04-deepagents-overview.md)

**四大要素:**
1. Planning tool
2. Filesystem access
3. Subagents
4. Detailed prompts

**0.2 版本新特性:**
- Pluggable Backends
- Composite Backend 策略
- Large Tool Result Eviction
- History Summarization
- Tool Call Repair

**使用场景:**
- 自主 Agent
- 长时程任务
- 复杂工作流

## 🔥 技术趋势总结

### 1. Agent Engineering 成为新学科
**影响:** 改变 AI 应用开发范式
**关键词:** 非确定性、生产化、迭代循环

### 2. Multi-Agent 架构成熟
**影响:** 提供清晰的模式和决策框架
**关键词:** Subagents, Skills, Handoffs, Router

### 3. 经济影响可量化
**影响:** 为政策和战略提供数据支撑
**关键词:** 经济原语、生产力增长、职业影响

### 4. MCP 成为标准
**影响:** Agent 生态互操作性
**关键词:** 协议标准化、生态系统

### 5. Claude 4.5 系列强势
**影响:** 提升 Agent 能力边界
**关键词:** 编程、推理、Computer Use

## 📖 使用建议

### 写技术文章
1. 查看 **ARTICLE_TOPICS_ANALYSIS.md** 获取选题建议
2. 参考对应的源文件获取详细内容
3. 结合多个主题形成独特视角

### 技术调研
1. 按主题浏览对应文件夹
2. 关注时间线和演进趋势
3. 比较 Anthropic 和 LangChain 的不同视角

### 学习路径
**初学者:**
1. Agent Engineering 学科概念
2. 单 Agent 最佳实践
3. 评估和调试方法

**进阶:**
1. Multi-Agent 架构设计
2. Deep Agents 框架
3. MCP 生态系统

**专家:**
1. 经济影响分析
2. 安全性和对齐
3. 生产部署实践

## 🔗 相关资源

### 官方文档
- [Anthropic Engineering Blog](https://www.anthropic.com/engineering)
- [LangChain Blog](https://blog.langchain.com/)
- [LangGraph Docs](https://docs.langchain.com/oss/python/langgraph/)
- [DeepAgents Docs](https://docs.langchain.com/oss/python/deepagents/)

### 工具平台
- [Claude Platform](https://platform.claude.com/)
- [LangSmith](https://smith.langchain.com/)
- [LangGraph Cloud](https://docs.langchain.com/cloud/)

## 📝 更新记录

- **2026-01-15**: 初始创建，收集 Anthropic 和 LangChain 最新博客内容
  - Anthropic: 3 篇核心内容
  - LangChain: 4 篇核心内容
  - 分析报告: 8 个高价值选题 + 4 个组合方案

## 🎯 下一步

1. ✅ 收集和整理博客内容
2. ✅ 分析技术趋势
3. ✅ 提出文章选题
4. ⏭️ 选择优先级最高的选题
5. ⏭️ 开始撰写第一篇文章

---

**维护者:** 基于 2026-01-15 的 Anthropic 和 LangChain 官方博客内容
**目的:** 为技术文章写作提供最新、权威的研究资料
