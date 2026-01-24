# Antigravity 会话归档工作流

此工作流用于将 Google Antigravity 的会话内容（包括 Plan、Task、Walkthrough 及核心背景）整理并归档为 OpenSpec 变更。

<!-- OPENSPEC:START -->
**Guardrails**
- **完整性优先**：优先保留会话的完整上下文，特别是“为什么要做”以及“最终达成了什么”。
- **规范化结构**：所有的归档内容必须严格遵循 OpenSpec 的目录结构规范 (`openspec/changes/<change-id>/`)。
- **信息分层**：将高层意图放入 `proposal.md`，执行细节放入 `tasks.md`，复杂推理和过程放入 `design.md`。

**Steps**
1. **初始化变更 (Initialize Change)**
   - 回顾会话核心主题，确定一个简洁明确的 `change-id`（建议格式：`archive-session-<topic>`，例如 `archive-session-auth-refactor`）。
   - 在终端执行命令创建目录：`mkdir -p openspec/changes/<change-id>`。

2. **提取背景与期望 (Extract Context)**
   - 分析对话历史，定位用户的初始 Prompt 和核心诉求。
   - 创建 `openspec/changes/<change-id>/proposal.md` 文件。
   - 在 `## Why` 章节中：详细描述本次会话的背景、目的以及期望解决的问题。
   - 在 `## What Changes` 章节中：概括本次会话产生的关键产出（Artifacts）或结论。

3. **整理计划与任务 (Organize Plan & Tasks)**
   - 提取 Antigravity Agent 生成的 Plan 和具体的 Task 列表。
   - 创建 `openspec/changes/<change-id>/tasks.md` 文件。
   - 将 Task 列表转换为标准的 Markdown 任务清单格式：
     ```markdown
     ## 1. Execution Plan
     - [x] 1.1 <Task Description>
     - [ ] 1.2 <Task Description>
     ```
   - 标记已完成 (`[x]`) 和未完成 (`[ ]`) 的任务。

4. **记录执行过程 (Record Walkthrough)**
   - 梳理对话中的关键执行步骤 (Walkthrough)、重要决策点以及生成的关键 Artifacts。
   - 创建 `openspec/changes/<change-id>/design.md` 文件（如果内容主要是技术决策）或 `openspec/changes/<change-id>/walkthrough.md`（如果侧重过程记录）。
   - 将 Agent 的思考过程 (CoT)、遇到的问题及解决方案记录在此文件中。

5. **更新系统现状 (Update System Specs)**
   - 这一步至关重要：不仅仅是归档“发生了什么”，还要更新“系统现在是什么样”。
   - 思考本次会话是否增加、修改或移除了系统的能力 (Capabilities)。
   - 在 `openspec/changes/<change-id>/specs/<capability>/spec.md` 中编写变更增量 (Deltas)：
     - **新增功能**：使用 `## ADDED Requirements`。
     - **修改行为**：使用 `## MODIFIED Requirements`（需包含完整的新版需求描述）。
     - **移除功能**：使用 `## REMOVED Requirements`。
   - 这样在执行 `openspec archive` 时，工具会自动将这些变更应用到 `openspec/specs/` 目录，保持系统文档的实时性。

6. **验证归档 (Validate)**
   - 运行 `openspec validate <change-id> --strict` 检查目录结构和文件格式。
   - 确认 `proposal.md` 清晰传达了意图，`tasks.md` 反映了真实进度，且 `specs/` 目录下的变更准确反映了系统现状的改变。

**Reference**
- **Proposal (`proposal.md`)**: 这里的 "Why" 是灵魂，必须讲清楚“为什么”进行这次会话。
- **Tasks (`tasks.md`)**: 直接复用 Agent 的 Plan，它是进度的快照。
- **Design/Walkthrough (`design.md`)**: 用于“防失忆”，记录那些没写在代码里但很重要的思考和尝试。
- **Specs (`specs/.../spec.md`)**: 用于“更新现状”，确保 OpenSpec 能够反映系统的最新状态。
<!-- OPENSPEC:END -->