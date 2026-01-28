# OpenSpec v1.0 深度解析：规范驱动开发的范式转移

> 2026年1月，OpenSpec 发布 v1.0 稳定版——这不是一次普通的版本更新，而是一场 **AI 编程助手协作方式** 的范式革命。

![OpenSpec 工作流演进](http://aisdapp.aihe.space/typora/c3ad2e1d-0bfc-4f85-bddc-d3828c676fa9.png)
*从僵硬的三步工作流到灵活的行动系统：OpenSpec v1.0 的范式转移*

---

## 核心洞察

OpenSpec v1.0 的发布标志着 **规范驱动开发 (Spec-Driven Development, SDD)** 从实验性玩具，进化为可应用于生产环境的成熟方法论。其核心变革在于：

- **从流程到行动**：抛弃僵硬的三步工作流，转向灵活的基于行动的系统
- **从静态到动态**：AI 不再依赖预配置的提示词，而是实时查询项目状态
- **从单一到通用**：一次配置，兼容 21 种 AI 编程工具

---

## 个人使用体验：OpenSpec vs SpecKit

![OpenSpec 使用记录](http://aisdapp.aihe.space/typora/cb172a6d-2849-49c2-bb6c-5a153d427c7e.png)
*笔者使用 OpenSpec 一个多月的工作记录 — 从 12 月中旬开始持续使用至今*

作为一个持续使用 OpenSpec 一个多月的开发者，我也曾深度体验过 GitHub 的 SpecKit。以下是我的真实对比感受：

### 为什么最终选择了 OpenSpec？

| 维度 | SpecKit | OpenSpec |
|------|---------|----------|
| **工作流灵活性** | 僵化的 `/specify → /plan → /tasks → /implement` 序列 | 灵活的行动系统，随时编辑任何工件 |
| **状态感知** | AI 需要猜测当前进度 | CLI 实时返回项目状态，AI 精确知道下一步 |
| **工具切换成本** | 每个工具独立模板，切换困难 | Agent Skills 通用格式，一次配置到处运行 |
| **迭代速度** | 较慢（GitHub 流程） | 快速（社区驱动，频繁更新） |

### 使用中的真实感受

**1. 状态透明性是杀手级特性**

使用 SpecKit 时，我经常遇到 AI "忘记"之前讨论过的内容。而 OpenSpec 的Spec描述系统现状，以及一些物件，让 AI 始终知道：
- 哪些工件已创建
- 当前处于哪个阶段
- 下一步该做什么

**2. 灵活性优于完美流程**

SpecKit 的四段式流程理论上很完美，但实际开发中经常需要：
- 回去修改 PRD
- 跳过某些工件
- 重新审视技术方案

OpenSpec 的行动系统让我随时可以做这些事，而不被流程绑架。主要还是觉得Speckit的流程有点重，后期应该是全自动化的。 当然如果非常复杂的大需求，用Speckit应该也可以，但是日常大部分还是增量迭代，小步快跑为主。


---

## 核心问题与解决方案详解

OpenSpec 的每一次版本迭代都不是随意的功能堆砌，而是针对 **AI 协作开发中的真实痛点** 进行精准打击。以下是各版本解决的核心问题及其背后的设计思路。

---

### 问题一：AI 无法理解项目动态状态 (v1.0.0)

#### 痛点描述

在使用 AI 编程助手时，开发者经常遇到这样的场景：

> **开发者**："帮我实现用户登录功能"
> **AI**：开始编写代码...
> **开发者**："等等，我们之前不是已经讨论过要先用 JWT 吗？而且 PRD 里写了要支持第三方登录！"
> **AI**：抱歉，我没有上下文...

传统方案的致命缺陷：
- **静态提示词**：AI 只能读取预配置的文件，无法知道当前项目有哪些工件已经存在
- **盲目执行**：AI 不知道哪些工件已创建、哪些待创建，常常重复工作或遗漏关键步骤
- **状态不透明**：没有机制让 AI 查询"我现在可以做什么"

#### OpenSpec v1.0 的解决方案

**1. 工件图 (Artifact Graph) 状态追踪**

OpenSpec 引入了工件图的概念，实时追踪每个变更的状态：

```
change-123 (新增购物车)
├── spec/prd.md          [✓ 已创建]
├── spec/tech-design.md  [✓ 已创建]
├── spec/tasks.md        [✓ 已创建]
├── impl/implementation.md [ ] 待创建
└── verification.md      [ ] 待创建
```

AI 在执行任何操作前，会先调用 CLI 查询当前状态：
```bash
openspec list --format json
```

返回的结构化数据让 AI 精确知道：
- 当前有哪些活跃变更
- 每个变更有哪些工件已创建/待创建
- 下一步应该做什么

**2. 行动系统 (Action-Based System)**

取代僵化的 `proposal → apply → archive` 三段式，v1.0 引入了 9 个独立行动：

| 行动 | 何时使用 | AI 如何理解 |
|------|---------|------------|
| `/opsx:explore` | 思考阶段，不写代码 | "只思考，不实现" |
| `/opsx:new` | 开始新功能 | "创建新目录，准备工件" |
| `/opsx:continue` | 逐步创建工件 | "检查已有工件，创建下一个" |
| `/opsx:ff` | 快速跳过规划 | "一次性创建所有规划工件" |
| `/opsx:apply` | 实现代码 | "读取 tasks.md，逐项实现" |
| `/opsx:verify` | 验证实现 | "对比规范与代码，标记差异" |
| `/opsx:sync` | 同步规范 | "解析 ## ADDED/MODIFIED，合并到主规范" |
| `/opsx:archive` | 归档完成 | "验证完整性，移动到 archive" |
| `/opsx:onboard` | 新人入职 | "11 个阶段的交互式教程" |

**3. 动态指令组装 (Dynamic Instruction Assembly)**

旧方案：AI 读取一个巨大的 `CLAUDE.md` 文件
```markdown
# 项目规范
[2000 行配置...]
```

新方案：三层动态组装

```javascript
// AI 执行 /opsx:apply 时，CLI 返回：
{
  "context": {
    "techStack": ["Next.js", "TypeScript", "Prisma"],
    "projectStructure": "..."
  },
  "rules": {
    "tasks.md": "每个任务必须包含 [ ] checkbox 格式的验证标准"
  },
  "template": `
# 实施计划

## 任务分解
- [ ] {{task}} | 验证：{{verification}}
  `
}
```

AI 不再"猜测"如何工作，而是获得精确的上下文 + 约束 + 输出模板。

---

### 问题二：设计-实现漂移 (v0.20.0)

#### 痛点描述

典型的开发场景：

```
Day 1: PRD 定义"用户可以导出 CSV 和 PDF"
Day 5: 开发者实现时发现 PDF 库有问题，只实现了 CSV
Day 10: 产品经理问"PDF 功能呢？"
Day 11: 开发者"哦...我忘了"
```

**问题本质**：实现代码与原始规范之间缺乏一致性验证机制。

#### OpenSpec v0.20.0 的解决方案

**`/opsx:verify` 命令**

执行 `/opsx:verify` 时，OpenSpec 会：

1. **解析规范**：读取 `spec/prd.md`、`spec/tech-design.md`、`spec/tasks.md`
2. **扫描代码**：分析实现文件的函数、类、API 端点
3. **对比差异**：检查每个需求是否被实现
4. **生成报告**：

```markdown
# 验证报告

## ✅ 已实现
- [x] 用户可以导出 CSV (found: exportCSV() in utils/export.ts)

## ❌ 未实现
- [ ] 用户可以导出 PDF (规范中要求，代码中未找到)

## ⚠️ 超出范围
- [ ] exportExcel() (规范中未提及，但代码中存在)
```

这个机制确保了 **"承诺的是什么，交付的就是什么"**。

---

### 问题三：工具锁定 (v0.17.0 - v1.0.0)

#### 痛点描述

开发者在不同 AI 工具间切换时面临巨大成本：

```
使用 Cursor:
→ 配置 .cursorrules

切换到 Claude Code:
→ 重写提示词到 CLAUDE.md

团队新成员用 Windsurf:
→ 又要写一套配置...
```

每个工具都有自己的"提示词方言"，规范资产无法复用。

#### OpenSpec 的解决方案

**1. Agent Skills 通用格式**

OpenSpec 定义了一个 YAML-frontmatter 的 Markdown 格式：

```yaml
---
name: opsx:new
description: 创建一个新的 OpenSpec 变更
---

# 使用指南

运行 /opsx:new 开始...
```

这个格式被 **21 种 AI 工具** 同时支持：
- Claude Code, Cursor, Windsurf, Continue（主流编辑器）
- Aider, Cline, RooCode, Kilo Code（CLI 工具）
- GitHub Copilot, Amazon Q, Gemini CLI（云服务）
- 以及更多...

**2. 一次配置，到处运行**

```bash
openspec init
# → 选择你使用的工具（可多选）

# 生成的 .claude/skills/ 目录：
# ├── opsx-new.md
# ├── opsx-apply.md
# ├── opsx-verify.md
# └── ...
```

这些 skill 文件在所有工具中都能直接使用，无需任何转换。

---

### 问题四：批量变更管理混乱 (v0.23.0)

#### 痛点描述

一次开发迭代完成 5 个功能后：

```
openspec/changes/
├── 2026-01-10-feature-a/  [已完成]
├── 2026-01-12-feature-b/  [已完成]
├── 2026-01-15-feature-c/  [已完成]
├── 2026-01-18-feature-d/  [已完成]
└── 2026-01-20-feature-e/  [已完成]
```

传统方案需要：
1. 逐个进入目录
2. 手动运行 `/opsx:archive`
3. 检查是否有冲突
4. 重复 5 次

#### OpenSpec v0.23.0 的解决方案

**`/opsx:bulk-archive` 命令**

```bash
/opsx:bulk-archive
```

一步完成：

1. **扫描所有变更**：自动识别已完成的变更
2. **批量验证**：检查每个变更的规范完整性
3. **冲突检测**：发现多个变更修改同一主规范段落
4. **确认归档**：显示摘要，一键归档

输出示例：
```
Found 5 completed changes:

✓ feature-a (3 artifacts, ready to archive)
✓ feature-b (4 artifacts, ready to archive)
✓ feature-c (2 artifacts, ready to archive)
✓ feature-d (5 artifacts, ready to archive)
✓ feature-e (3 artifacts, ready to archive)

⚠️  Conflict detected: feature-b and feature-e both modify spec/api.md
   → Will be resolved during sync

Archive all 5 changes? (y/n)
```

---

### 问题五：项目配置僵化 (v0.22.0)

#### 痛点描述

不同项目有不同的工作流需求：

- **前端项目**：需要组件设计规范、Storybook 集成
- **后端项目**：需要 API 规范、数据库迁移脚本
- **全栈项目**：两套都需要

全局配置无法满足这种多样性。

#### OpenSpec v0.22.0 的解决方案

**项目级配置 `openspec/config.yaml`**

```yaml
# openspec/config.yaml
rules:
  - "前端组件必须包含 TypeScript 接口定义"
  - "API 变更必须包含 OpenAPI spec 更新"

context_files:
  - "package.json"
  - "tsconfig.json"
  - "docs/api-conventions.md"

schemas:
  - path: schemas/component-design.yaml
    artifact: component-spec
  - path: schemas/api-endpoint.yaml
    artifact: api-spec
```

**项目自定义工件模式**

```
openspec/schemas/
├── component-design.yaml
│   └── template.md
└── api-endpoint.yaml
    └── template.md
```

项目可以定义自己的工件类型和模板，OpenSpec 会自动识别。

---

### 问题六：新手入门门槛高 (v0.21.0 - v1.0.0)

#### 痛点描述

新团队成员加入时：

```
资深开发者: "用 OpenSpec 创建一个新变更"
新人: "怎么用？"
资深开发者: "运行 /opsx:new"
新人: "然后呢？"
资深开发者: "创建 PRD、技术方案..."
新人: "具体怎么写？有例子吗？"
```

缺乏系统的引导，新手学习曲线陡峭。

#### OpenSpec v1.0 的解决方案

**`/opsx:onboard` 交互式入职**

一个 **15 分钟** 的完整教程，包含 **11 个阶段**：

| 阶段 | 学习内容 |
|------|---------|
| 1 | 理解 Spec-Driven Development 的概念 |
| 2 | 探索当前项目结构 |
| 3 | 创建第一个变更 |
| 4 | 编写 PRD（带模板和示例） |
| 5 | 编写技术方案（带模板和示例） |
| 6 | 分解任务清单 |
| 7 | 实现代码（AI 辅助） |
| 8 | 验证实现与规范一致性 |
| 9 | 同步增量规范到主规范 |
| 10 | 归档完成的变更 |
| 11 | 开始自己的真实任务 |

每个阶段都是：
- **可执行的**：AI 给出具体命令
- **可验证的**：有明确的完成标准
- **代码库感知的**：基于真实项目上下文给出建议

---

### 问题七：规范同步脆弱 (v0.18.0 - v1.0.0)

#### 痛点描述

增量规范同步到主规范时，传统方案使用**头部匹配**：

```
## API Endpoints
### POST /api/users
[从 delta spec 复制内容...]
```

问题：
- 如果主规范标题改为 "## REST API Endpoints"，同步会失败
- 无法识别新增/修改/删除的细微差别
- 冲突解决需要人工介入

#### OpenSpec v1.0 的解决方案

**语义化标记**

增量规范使用明确的语义标记：

```markdown
## ADDED API Endpoints

### POST /api/users
创建新用户

## MODIFIED Authentication

从 JWT v1 升级到 JWT v2：
- 添加 refresh token 机制
- 延长 access token 有效期

## REMOVED LegacyAuth
不再支持基本认证
```

归档时，OpenSpec 解析这些标记：
- `ADDED` → 追加到主规范
- `MODIFIED` → 智能合并（保留主规范的补充说明）
- `REMOVED` → 从主规范删除

这种**需求级别的同步**比**文本级别的匹配**更可靠。

---

## 问题-解决方案矩阵总结

| 版本 | 核心问题 | 解决方案 | 影响 |
|------|---------|---------|------|
| **v1.0.0** | AI 无法理解项目状态 | 工件图 + 行动系统 + 动态指令 | AI 协作从"盲目执行"到"精确理解" |
| **v0.23.0** | 批量归档低效 | `/opsx:bulk-archive` | 5 个变更加 10 秒归档 |
| **v0.22.0** | 配置僵化 | 项目级 config.yaml + 自定义 schema | 不同项目可定制工作流 |
| **v0.21.0** | 反馈门槛高 | CLI 直接提交 GitHub Issue | 3 秒提交反馈 |
| **v0.20.0** | 设计-实现漂移 | `/opsx:verify` | 自动检测规范偏离 |
| **v0.19.0** | 编辑器碎片化 | 21 种工具通用 Agent Skills | 一次配置，到处运行 |
| **v0.18.0** | 规范同步脆弱 | 语义化标记 (ADDED/MODIFIED/REMOVED) | 需求级别精确同步 |

---

## 版本 Release 详解

以下是每个版本的详细 Release 内容，包含所有新增功能、改进和修复。

---

### v1.0.1 — Patch Release (2026年1月)

**类型：** 补丁版本

**变更：**
- 修复了入职指南中归档路径的错误
  - 模板现在显示正确的路径 `openspec/changes/archive/YYYY-MM-DD-<name>/`
  - 之前错误地显示为 `openspec/archive/YYYY-MM-DD--<name>/`

**影响：** 文档修正，不影响功能

---

### v1.0.0 — "The OPSX Release" (2026年1月)

**类型：** 里程碑版本 — 从实验性到稳定版

#### 新增 (New)

**1. 基于行动的工作流 (Action-Based Workflow)**

取代了僵硬的 `proposal → apply → archive` 固定序列，转向灵活的行动系统。现在可以随时编辑任何工件，工件图会自动追踪状态。

| 命令 | 功能描述 |
|------|---------|
| `/opsx:explore` | 思考模式 — 在承诺变更前探索想法和调查问题 |
| `/opsx:new` | 创建新变更 — 开始一个新的规范驱动变更 |
| `/opsx:continue` | 逐步创建 — 一次创建一个工件，逐步完成 |
| `/opsx:ff` | 快速生成 — 一次性生成所有规划工件 |
| `/opsx:apply` | 实现任务 — 根据任务清单实现代码 |
| `/opsx:verify` | 验证实现 — 验证实现是否与规范匹配 |
| `/opsx:sync` | 同步规范 — 将增量规范同步到主规范 |
| `/opsx:archive` | 归档变更 — 将完成的变更归档 |
| `/opsx:bulk-archive` | 批量归档 — 一次性归档多个完成的变更 |
| `/opsx:onboard` | 交互式入职 — 15分钟完整工作流教程 |

**2. 动态指令系统 (Dynamic Instructions)**

AI 指令现在由三层动态组装：

```yaml
context:    # 项目上下文
  - 技术栈
  - 项目结构

rules:      # 工件特定约束
  - PRD 必须包含成功标准
  - 任务必须包含验证标准

template:   # 输出结构模板
  - Markdown 标题层级
```

AI 不再接收静态提示词，而是实时查询 CLI 获取项目状态。

**3. 语义化规范同步 (Semantic Spec Syncing)**

增量规范使用语义标记：
- `## ADDED` — 新增内容
- `## MODIFIED` — 修改内容
- `## REMOVED` — 删除内容

归档时在**需求级别**解析这些标记，而非脆弱的头部匹配。

**4. Agent Skills 系统**

单个 `.claude/skills/` 目录替代了 8+ 个分散的配置文件：
- `CLAUDE.md`
- `.cursorrules`
- `AGENTS.md`
- `project.md`
- 以及其他工具特定文件...

Skills 是 YAML-frontmatter 的 Markdown 文件，跨 Claude Code、Cursor、Windsurf 等工具工作。

**5. 交互式入职教程 (Interactive Onboarding)**

`/opsx:onboard` 提供：
- **11 个阶段**的完整工作流教程
- 代码库感知的任务建议
- 约 **15 分钟**完成
- 引导新人完成首次完整的规范驱动变更

**6. 交互式设置 (Interactive Setup)**

`openspec init` 现在提供：
- 动画欢迎屏幕
- 可搜索的多选工具列表
- 自动预选已配置的工具，便于刷新配置

**7. 21 种 AI 工具支持**

完整支持：Claude Code, Cursor, Windsurf, Continue, Gemini CLI, GitHub Copilot, Amazon Q, Cline, RooCode, Kilo Code, Auggie, CodeBuddy, Qoder, Qwen, CoStrict, Crush, Factory, OpenCode, Antigravity, iFlow, Codex

**8. 自定义模式 (Custom Schemas)**

在 `openspec/schemas/` 中定义自定义工件工作流，无需修改包代码。

#### 破坏性变更 (Breaking Changes)

**移除的命令：**
- ❌ `/openspec:proposal`
- ❌ `/openspec:apply`
- ❌ `/openspec:archive`

**移除的配置文件生成：**
- ❌ `CLAUDE.md`
- ❌ `.cursorrules`
- ❌ `AGENTS.md`
- ❌ `project.md`

#### 迁移方式

运行 `openspec init` — 现有工作全保留（活跃变更、已归档变更、主规范），仅清理过时配置文件（需确认）。

#### 修复 (Fixed)

- Claude Code YAML 解析失败（当命令名称包含冒号时）
- 任务文件解析（处理复选框行尾的空白字符）
- JSON 指令输出现在分离 context/rules 与 template（AI 曾将约束块复制到工件文件中）

#### 文档新增

- 入门指南 (Getting Started)
- CLI 参考 (CLI Reference)
- 命令参考 (Commands)
- 概念指南 (Concepts)
- 自定义指南 (Customization)

---

### v0.23.0 — Bulk Archive, Simplified Setup (2025年末)

**类型：** 功能版本

#### 新增 (New)

**批量归档 (Bulk Archive)**

- `/opsx:bulk-archive` — 一次性归档多个完成的变更
- 自动验证规范
- 检测冲突
- 显示单个确认提示后归档

#### 改进 (Improved)

**配置设置**

- 创建新 OpenSpec 配置现在使用带有有用注释的合理默认值
- 不再通过问答式交互

---

### v0.22.0 — Project Configuration (2025年末)

**类型：** 功能版本（实验性）

#### 新增 (New)

**项目级配置 (Project Configuration)**

- `openspec/config.yaml` — 每个项目配置 OpenSpec
- 可注入自定义规则
- 指定上下文文件
- 控制模式解析

**项目本地模式 (Project-Local Schemas)**

- `openspec/schemas/` — 定义项目特定工作流的自定义工件模式

**模式管理 (Schema Management)**

- `openspec schema list` — 列出所有可用模式
- `openspec schema show` — 显示模式详情
- `openspec schema export` — 导出模式定义
- `openspec schema validate` — 验证工件是否符合模式

#### 修复 (Fixed)

- 配置加载现在处理空的 `rules` 字段而不报错

---

### v0.21.0 — Feedback Command, Nix Support (2025年末)

**类型：** 功能版本

#### 新增 (New)

**反馈命令 (Feedback Command)**

- `openspec feedback` — 直接从 CLI 提交反馈
- 自动创建带有元数据的 GitHub Issue
- 如果失败，提供手动提交链接

**Nix 支持**

- Nix flake 支持 — 使用 `flake.nix` 安装和开发
- 自动化维护和 CI 验证

#### 改进 (Improved)

**变更推断**

- `opsx apply` 自动从对话上下文检测要应用的变更
- 有歧义时提示用户

**归档同步评估**

- 同步操作期间更清晰的增量规范位置指导

#### 修复 (Fixed)

**探索模式护栏**

- 探索模式现在明确阻止实现
- 保持聚焦于思考和发现

---

### v0.20.0 — Verify Command (2025年末)

**类型：** 功能版本

#### 新增 (New)

**验证命令 (Verify Command)**

- `/opsx:verify` — 验证实现是否与规范匹配
- 捕获计划内容与构建内容之间的"漂移"

#### 修复 (Fixed)

- Vitest 不再产生进程风暴 — worker 并行现在有上限
- Agent workflows 使用非交互模式进行验证命令
- PowerShell 补全生成器现在产生有效语法（移除尾随逗号）

---

### v0.19.0 — Editor Extensions (2025年末)

**类型：** 功能版本

#### 新增 (New Features)

**编辑器支持**

- **Continue IDE 支持** — OpenSpec 现在为 Continue 生成斜杠命令
- 扩展了编辑器集成选项（Cursor, Windsurf, Claude Code 等）

**Shell 补全**

- Bash, Fish, PowerShell 补全
- 运行 `openspec completion install` 在首选 shell 中设置 Tab 补全

**探索命令**

- `/opsx:explore` — 新的思考伙伴模式
- 用于在承诺变更前探索想法和调查问题

#### 修复 (Bug Fixes)

- Shell 补全现在在命令有子命令时正确提供父级标志（如 `--help`）
- 修复了测试中的 Windows 兼容性问题

#### 其他 (Other)

- 添加了可选的匿名使用统计
  - 帮助理解 OpenSpec 如何被使用
  - **默认选择退出** — 设置 `OPENSPEC_TELEMETRY=0` 或 `DO_NOT_TRACK=1` 禁用
  - 仅收集命令名称和版本；不收集参数、文件路径或内容
  - 在 CI 环境中自动禁用

---

## 商业/行业洞察

### 1. SDD 正在成为 AI 开发的新标准

2025-2026 年，AI 编程助手爆发式增长（Copilot, Cursor, Windsurf, Cline, Aider 等），但每个工具都有自己的 "提示词工程" 黑魔法。OpenSpec 的出现，本质上是：

> **将 "AI 提示词" 从艺术，升级为可工程化的 "规范"**

这与 OpenAPI 对 REST API 的标准化作用类似 — 让 AI 协作从 "玄学" 变成可复制的工程实践。

### 2. 工具战争的终结

OpenSpec v1.0 支持 **21 种 AI 工具**，包括：

| 分类 | 工具 |
|------|------|
| 主流编辑器 | Claude Code, Cursor, Windsurf, Continue |
| CLI 工具 | Aider, Cline, RooCode, Kilo Code |
| 云服务 | GitHub Copilot, Amazon Q, Gemini CLI |
| 其他 | Auggie, CodeBuddy, Qoder, Qwen, CoStrict, Crush, Factory, OpenCode, Antigravity, iFlow, Codex |

这意味着：**你的规范资产不再被单一工具锁定**。今天用 Cursor，明天切换到 Windsurf？无需重写提示词。

### 3. 从 "提示词工程师" 到 "规范架构师"

v1.0 的动态指令系统揭示了未来趋势：

> **AI 不再需要你写完美的提示词，它需要的是结构化的项目上下文 + 约束规则 + 输出模板**

三层架构：
- **Context (上下文层)** — 你的技术栈、项目结构
- **Rules (规则层)** — 工件特定的约束（如 "PRD 必须包含成功标准"）
- **Templates (模板层)** — 输出结构（如 Markdown 标题层级）

---

## 个人/职业启发

### 对开发者：从 "写提示词" 到 "写规范"

**实操建议：**

1. **立即行动：** 运行 `/opsx:onboard` — 15分钟交互式教程，完成首次完整的规范驱动变更
2. **建立习惯：** 每次编码前，先用 `/opsx:explore` 思考，再用 `/opsx:new` 正式开始
3. **版本控制你的规范：** 将 `openspec/` 目录提交到 Git — 这是你的 "第二代码库"

### 对团队：AI 协作的可复用性

**痛点解决：**

| 传统问题 | OpenSpec 方案 |
|---------|--------------|
| "为什么 Copilot 在你机器上聪明，在我机器上笨？" | 统一的规范定义，消除 "提示词彩票" |
| "新人不知道如何有效使用 AI 助手" | `/opsx:onboard` 提供标准化入职 |
| "我们的 AI 提示词散落在 8 个不同的文件里" | 单一 `.claude/skills/` 目录 |

### 对产品经理：规范的可追踪性

OpenSpec 的语义化同步 (`## ADDED`, `## MODIFIED`) 意味着：

> **每一次变更的需求追溯，像 Git 一样精确**

不再是 "我记得我们在某个会议讨论过"，而是：
```
openspec/changes/2026-01-15-feature-x/spec/prd.md
## ADDED Requirements
- [x] 用户必须能够一键导出 CSV
```

---

## 可执行工具包

### 快速上手检查清单

```bash
# 1. 安装
npm install -g @openspec/cli

# 2. 初始化（交互式，支持多选工具）
openspec init

# 3. 完成入职教程（强烈推荐）
# 在 AI 助手中输入：/opsx:onboard

# 4. 你的第一个规范驱动变更
/opsx:new
# → AI 会引导你创建 PRD、技术方案、实施计划
```

### AI 协作提示词模板

**场景 1：探索新功能（不写代码）**
```
请帮我使用 /opsx:explore 模式思考以下问题：
[描述问题或想法]

我想理解：
1. 这个需求的核心价值是什么？
2. 有哪些潜在的技术方案？
3. 主要风险和依赖是什么？

注意：不要生成任何代码，只需要思考和分析。
```

**场景 2：开始规范驱动的开发**
```
我想开发一个新功能，使用 OpenSpec 工作流：

功能描述：[简短描述]

请帮我：
1. 运行 /opsx:new 创建新变更
2. 逐步创建所需的工件（PRD、技术方案、任务清单）
3. 在 /opsx:apply 之前，先让我审查所有规划工件
```

**场景 3：验证实现**
```
我已完成代码实现，请帮我运行 /opsx:verify 检查：
1. 实现是否与原始规范一致？
2. 是否有遗漏的需求？
3. 是否有超出范围的变更？
```

---

## 结语

OpenSpec v1.0 的发布，不是终点，而是 **规范驱动开发** 走向主流的起点。

当 AI 编程助手从 "辅助工具" 进化为 "协作伙伴"，我们需要的不只是更聪明的模型，而是：

> **一套让 AI 理解我们意图的通用语言**

OpenSpec 正在构建这套语言。

---

## 扩展阅读

- [OpenSpec GitHub](https://github.com/Fission-AI/OpenSpec)
- [OpenSpec 完整发布说明](https://github.com/Fission-AI/OpenSpec/releases)
- [OpenSpec 使用指南（中文）](https://github.com/Tenas-AI/OpenSpec-Chinese)
- [迁移指南](https://github.com/Fission-AI/OpenSpec/blob/main/docs/migration.md)

---

**极简摘要：** OpenSpec v1.0 将规范驱动开发从实验性玩具升级为生产级工具，通过基于行动的工作流、动态指令系统和21种工具兼容，正在成为 AI 编程协作的新标准。

---

## 全景总结

![OpenSpec v1.0 全景总结](http://aisdapp.aihe.space/typora/9069f4bc-a3ab-42b1-a2eb-77fbf2a12a78.png)
*OpenSpec v1.0 核心变革全景：从实验性到生产级，从单一工具到通用标准*

---

## Sources

- [OpenSpec GitHub Releases](https://github.com/Fission-AI/OpenSpec/releases)
- [OpenSpec CHANGELOG](https://github.com/Fission-AI/OpenSpec/blob/main/CHANGELOG.md)
- [OpenSpec GitHub Repository](https://github.com/Fission-AI/OpenSpec)
- [OpenSpec 中文版](https://github.com/Tenas-AI/OpenSpec-Chinese)
- [OpenSpec 使用指南](https://blog.mapin.net/posts/OpenSpec%20使用指南)
- [规范驱动 AI 协作深度解析](https://blog.csdn.net/yangshangwei/article/details/154361472)
