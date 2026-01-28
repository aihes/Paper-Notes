# Clawd.bot 是什么？为什么你需要一个 AI 员工

> **"The UNIX philosophy meets your DMs"** — Clawd.bot 将 UNIX 哲学与即时通讯结合，打造了一个真正能"做事"的个人 AI 助手。

---

## 本质：Clawd.bot 究竟是什么？

抛开所有技术细节，Clawd.bot 的**最本质**可以用一句话概括：

> **Clawd.bot = 消息平台 ↔️ AI Agent 的通用翻译网关**

### 它解决的问题

想象这样一个场景：
- 你在 WhatsApp 上给 AI 发一条消息："帮我查一下明天的天气"
- AI 收到消息，调用天气 API 获取数据
- AI 把结果发回给你

这看起来很简单，但背后有一个巨大的问题：**WhatsApp 不懂 AI，AI 也不懂 WhatsApp**。

Clawd.bot 就是这个"翻译官"——它：
1. **接收**来自任何消息平台的输入
2. **翻译**成 AI 能理解的格式
3. **路由**给合适的 AI Agent 处理
4. **返回**结果到原平台

### 为什么是"网关"而不是"应用"？

这很重要。Clawd.bot 不是让你用它来聊天的应用，而是：

| 传统 AI 助手 | Clawd.bot |
|:---|:---|
| ❌ 必须打开特定 App | ✅ 在你习惯的工具里用 |
| ❌ 数据在云端 | ✅ 完全本地运行 |
| ❌ 功能固定 | ✅ 可编程、可扩展 |
| ❌ 对话为主 | ✅ **行动为主** |

### 用一句话记住它

> **Clawd.bot 让 AI 渗透到你现有的数字生活中，而不是要求你迁移到一个新平台。**

这是它的本质，也是它区别于 ChatGPT、Claude 等所有云端 AI 助手的根本所在。

---

## 什么是 Clawd.bot？

Clawd.bot 是一个运行在你本地计算机上的**个人 AI 助手**，与传统的聊天机器人不同，它的核心理念是 **"The AI that actually does things"** —— 不仅能够对话，更能**执行实际操作**。

![alt text](http://aisdapp.aihe.space/typora/1372bb30-a2f4-403b-868e-68cc2311b0b1.png)

### 核心特点

- **本地运行**：数据完全掌控在自己手中
- **多平台集成**：连接 WhatsApp、Telegram、Discord、iMessage
- **真正的行动能力**：从聊天到执行，跨越鸿沟
- **24/7 在线**：全职 AI 员工，无需休息

---

## 工作原理

Clawd.bot 的架构设计遵循 **Gateway + Agent + Channels** 的模式，理解这个架构有助于更好地使用它。

### 架构概览

![Clawd.bot 架构全景图](http://aisdapp.aihe.space/typora/e9b2d9c3-c192-4cd5-ae3d-aa54f32a1996.png)

上图展示了 Clawd.bot 的完整数据流：从用户的消息平台开始，经过渠道层适配，通过 Gateway 路由到 AI Agent 处理，最终调用各种工具完成操作并返回结果。

下面是详细的架构说明：



```
┌─────────────────────────────────────────────────────────────────┐
│                         用户使用的通讯工具                        │
│  WhatsApp  │  Telegram  │  Discord  │  iMessage  │  ...         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Channels (渠道层)                         │
│  负责与各平台通信，将消息统一转换为内部格式                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Gateway (网关服务)                         │
│  WebSocket 服务器 │ 消息路由 │ 会话管理 │ 认证授权                │
│         默认端口: 18789 (dev: 19001)                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Agent (AI 代理)                          │
│  消息理解 │ 任务规划 │ 工具调用 │ 结果生成                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Tools (工具集)                           │
│  Shell │ Browser │ Email │ Calendar │ Memory │ Webhooks │ ...   │
└─────────────────────────────────────────────────────────────────┘
```

### 核心组件说明

#### 1. Gateway（网关服务）

Gateway 是 Clawd.bot 的**核心服务**，扮演以下角色：

- **WebSocket 服务器**：为 Agent 提供实时连接
- **消息路由中心**：将来自各渠道的消息分发到对应的 Agent
- **会话管理器**：维护对话上下文和状态
- **认证授权**：管理配对设备和访问权限

运行方式：
```bash
# 前台运行（调试用）
clawdbot gateway --foreground

# 后台运行（推荐）
clawdbot gateway start
```

#### 2. Channels（渠道层）

Channels 是 Clawd.bot 与外部通讯平台的**适配器**：

- **WhatsApp Web**：通过浏览器自动化连接
- **Telegram Bot API**：使用 Bot Token 访问
- **Discord Bot**：通过 Discord Bot API
- **iMessage**：使用 AppleScript (仅 macOS)

每个 Channel 负责将平台特定的消息格式转换为统一的内部格式。

#### 3. Agent（AI 代理）

Agent 是**智能处理单元**，负责：

- **理解用户意图**：解析自然语言消息
- **任务规划**：将复杂任务拆解为可执行步骤
- **工具调用**：调用合适的工具完成操作
- **结果生成**：将执行结果转换为自然语言回复

#### 4. Tools（工具集）

Tools 是 Agent 的**手脚**，提供实际的执行能力：

| 工具类别 | 示例 |
|:---|:---|
| **系统操作** | Shell 命令执行、文件操作 |
| **网络操作** | HTTP 请求、Web 抓取 |
| **浏览器** | Chrome/Chromium 自动化 |
| **邮件** | 发送邮件、读取收件箱 |
| **日历** | 创建事件、查询日程 |
| **记忆** | 存储和检索长期信息 |

### 消息流转过程

```
用户发送消息
    │
    ▼
渠道层接收 (如 Telegram)
    │
    ▼
Gateway 路由到 Agent
    │
    ▼
Agent 理解意图
    │
    ▼
调用工具执行操作 (如运行 Shell 命令)
    │
    ▼
获取执行结果
    │
    ▼
Agent 生成回复
    │
    ▼
Gateway 路由回渠道
    │
    ▼
用户收到回复
```

### 配置文件结构

```bash
~/.clawdbot/
├── clawdbot.json          # 主配置文件
├── credentials/           # 敏感凭据（Bot Token 等）
├── devices/               # 已配对设备
├── agents/                # Agent 工作空间
│   └── main/
│       ├── sessions/      # 会话记录
│       └── memory/        # 长期记忆
└── state/                 # 运行时状态
```

### 关键配置参数

```json
{
  "gateway": {
    "port": 18789,           // Gateway 端口
    "hostname": "127.0.0.1"  // 绑定地址
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "xxx",
      "dmPolicy": "open",     // DM 策略: open/pairing
      "allowFrom": ["*"]      // 允许的用户
    }
  },
  "agent": {
    "model": "gpt-4o",       // 使用的 LLM
    "tools": ["shell", "browser", "email"]
  }
}
```


---

## 主要使用场景

| 场景 | 说明 | 示例 |
| :--- | :--- | :--- |
| **邮件管理** | 清理收件箱、自动回复邮件 | "帮我清理今天的垃圾邮件" |
| **日程安排** | 管理日历、安排会议 | "下周三下午和 Alex 约个会议" |
| **旅行助手** | 航班值机、旅行预订管理 | "帮我办理明天的航班值机" |
| **设计辅助** | 研究最新设计趋势、支持创意工作 | "总结一下 2026 年 UI 设计趋势" |
| **信息检索** | 通过聊天快速获取信息 | "这篇论文的核心观点是什么？" |
| **任务自动化** | 通过自然语言执行系统命令 | "运行测试并把结果发给我" |

---

## 安装与快速开始

### 已安装版本检查

```bash
clawdbot --version
# 🦞 Clawdbot 2026.1.24-3 (885167d)
```

### 首次使用流程

```bash
# 1. 运行设置向导
clawdbot onboard

# 2. 登录你想要使用的渠道（如 WhatsApp）
clawdbot channels login --verbose

# 3. 启动 Gateway 服务
clawdbot gateway

# 4. 发送第一条消息测试
clawdbot message send --target "联系人" --message "Hello"
```


![clawdbot onboard会引导你一步步的进行操作，每步都有详细的说明](http://aisdapp.aihe.space/typora/a5b559a8-817a-429a-ad2b-d75d345b6804.png)

---

## 常用命令速查

### 初始化与配置

```bash
clawdbot setup              # 初始化配置文件
clawdbot onboard            # 交互式设置向导
clawdbot configure          # 配置凭据、设备、代理默认值
clawdbot config             # 配置助手（get/set/unset）
```

### 渠道管理

```bash
clawdbot channels login --verbose     # 登录渠道（显示二维码）
clawdbot message send --target +15555550123 --message "Hi" --json
clawdbot message send --channel telegram --target @mychat --message "Hi"
```

### Gateway 与 Agent

```bash
clawdbot gateway --port 18789         # 启动 Gateway
clawdbot --dev gateway                # 开发者模式（隔离状态）
clawdbot agent --to +15555550123 --message "Run summary" --deliver
```

### 状态与诊断

```bash
clawdbot status              # 查看渠道健康状态
clawdbot health              # 获取运行中的 Gateway 健康状态
clawdbot dashboard           # 打开控制面板
clawdbot logs                # 查看 Gateway 日志
```

---

## 高级功能

### Agent 管理

```bash
clawdbot agents              # 管理隔离的代理（工作空间 + 认证 + 路由）
clawdbot skills              # 技能管理
clawdbot memory              # 内存搜索工具
clawdbot browser             # 管理专用浏览器
```

### 开发者工具

```bash
clawdbot --dev               # 开发配置文件
clawdbot tui                 # 终端 UI
clawdbot cron                # Cron 调度器
clawdbot webhooks            # Webhook 管理
```

---

## 故障排查与调试

### Telegram 消息无回应？

这是最常见的问题，通常有以下几种原因：

#### 原因 1：DM 配对模式（最常见）

默认情况下，Telegram bot 使用 `dmPolicy: "pairing"` 模式，需要先完成配对才能接收私信。

**症状**：
```bash
# 日志显示类似错误
error [tools] message failed: Unknown target "me" for Telegram
error [tools] message failed: Telegram send failed: chat not found
```

![alt text](http://aisdapp.aihe.space/typora/e5fd5aa0-ba26-4847-959b-635822c8a80e.png)

**解决方案 A - 完成配对**：

1. 查看待处理的配对请求：
```bash
cat ~/.clawdbot/credentials/telegram-pairing.json
```

2. 记下配对码（如 `XBA7XXXX`）

3. 在 Telegram 中给 bot 发送配对码完成配对

**解决方案 B - 改为开放模式（更简单）**：

编辑配置文件 `~/.clawdbot/clawdbot.json`：

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "你的token",
      "dmPolicy": "open",
      "allowFrom": ["*"],
      "groupPolicy": "allowlist"
    }
  }
}
```

然后重启 Gateway：
```bash
clawdbot pairing approve telegram XXX
clawdbot gateway restart
```

![alt text](http://aisdapp.aihe.space/typora/5e5d7628-529f-485b-bd2e-8d63b937a588.png)

#### 原因 2：Bot 未启动

在 Telegram 中必须先点击 **"Start"** 按钮或发送 `/start` 命令。

### 查看日志调试

#### 实时查看日志

```bash
# 实时跟踪日志
clawdbot logs --follow

# 查看最近日志
clawdbot logs
```
![alt text](http://aisdapp.aihe.space/typora/73f9f442-6de6-47c6-ad89-92c79889b8b2.png)

#### 日志文件位置

```bash
# 日志文件
/tmp/clawdbot/clawdbot-YYYY-MM-DD.log

# Telegram 配对状态
~/.clawdbot/credentials/telegram-pairing.json

# 配对设备列表
~/.clawdbot/devices/paired.json
```

### 运行方式说明

Clawd.bot 通过 **Gateway 服务** 运行，有两种模式：

#### 模式 1：LaunchAgent（推荐，后台运行）

```bash
# 安装为系统服务（开机自启动）
clawdbot gateway install

# 启动服务
clawdbot gateway start

# 重启服务
clawdbot gateway restart

# 停止服务
clawdbot gateway stop
```

#### 模式 2：前台运行（调试用）

```bash
# 前台运行，日志直接输出
clawdbot gateway --foreground
```

### 常用诊断命令

```bash
# 查看完整状态（包括安全审计）
clawdbot status

# 深度检查（测试各渠道连接）
clawdbot status --deep

# 检查健康状态
clawdbot health

# 查看渠道状态
clawdbot channels status

# 查看 Telegram 相关日志
clawdbot channels logs --channel telegram
```

### Dashboard 调试

Web 控制面板是最直观的调试工具：

```bash
# 打开 Dashboard
clawdbot dashboard

# 或直接访问
open http://127.0.0.1:18789
```

在 Dashboard 中可以：
- 查看实时日志
- 发送测试消息
- 查看会话状态
- 管理配置
- 查看 Agent 运行状态

### 配置文件快速参考

| 文件路径 | 用途 |
|:---|:---|
| `~/.clawdbot/clawdbot.json` | 主配置文件 |
| `~/.clawdbot/credentials/telegram-pairing.json` | Telegram 配对请求 |
| `~/.clawdbot/devices/paired.json` | 已配对设备 |
| `~/.clawdbot/agents/main/sessions/sessions.json` | Agent 会话 |

---

## 深度思考：Clawd.bot 代表了什么？

### 范式转移：从"对话"到"行动"

过去五年的 AI 产品，无论是 ChatGPT、Claude 还是各类智能助手，本质上都是**对话系统**——你问，它答。信息流动是单向的，认知负载在你身上：你需要记住问题、构思提问、理解答案、再转化为行动。

Clawd.bot 代表了一个根本性的转移：**AI 从信息工具变成了行动代理**。

这不是量的改进，是质的飞跃。当 AI 可以直接发邮件、定会议、跑测试、办值机时，它不再是一个"更聪明的搜索引擎"，而是一个**可以委托任务的数字劳动力**。

### 为什么是"本地 + 开源"？

2023-2024 年，所有人都以为 AI 的未来是 ChatGPT 这样的云端超级服务。但 Clawd.bot 的爆火揭示了一个被忽视的方向：**本地化、可控制的个人 AI**。

这背后有两个深层原因：

**1. 隐私不是技术问题，是控制权问题**

云端 AI 再安全，你的数据终究在别人的服务器上。当 AI 开始处理你的邮件、日程、聊天记录时，"隐私"就不再是抽象概念，而是实实在在的**控制权**。Clawd.bot 把这个控制权还给了你——代码在你的机器上，数据在你的硬盘里，修改权在你手中。

**2. 个人数字孪生需要个性化**

云端 AI 服务是"万人一面"的通用模型。但真正的个人助手需要了解你的习惯、偏好、人际关系、工作方式。这些深度的个性化，只有长期运行、数据本地的系统才能做到。Clawd.bot 不是在用你的 prompt 调用通用 API，而是在构建一个**属于你一个人的数字延伸**。

### Unix 哲学的回归

Clawd.bot 的核心理念是"The UNIX philosophy meets your DMs"。这不是一句口号，而是对过去十年"大而全"产品的反思。

- Slack、Discord、Notion 这些平台都想成为你的"一切"
- Clawd.bot 说：不，你继续用你喜欢的工具，我只是在背后帮你连接它们

这是 Unix 哲学的核心：**做好一件事，提供清晰的接口，允许组合**。在这个意义上，Clawd.bot 不是在和 ChatGPT 竞争，它是在重新定义竞争的维度——不是"谁的模型更强"，而是"谁能更好地融入你现有的工作流"。

### 对个人：认知外包与可编程生活

Clawd.bot 的真正价值，是让你可以**外包常规认知任务**，把注意力集中在真正重要的事情上。

这不是"自动化"，自动化是预定义流程的机械执行。这是**可编程的生活**——你可以用自然语言描述意图，AI 理解上下文、拆解任务、执行操作、反馈结果。当"回复这封邮件"、"安排下周会议"、"总结这篇论文"这些任务可以委托时，你的时间就被释放了。

更重要的是，这是一种**新的思维方式**：你不再需要记住如何操作每个软件，只需要记住"我想做什么"。操作知识的负担被转移到了 AI 身上。

### 对行业：去平台化的信号

Clawd.bot 的流行是一个信号：**用户开始厌倦平台锁定**。

过去十年，每个服务都想成为你的"入口"——微信要做操作系统，抖音要做生活方式，Slack 要做数字 HQ。但 Clawd.bot 说：不需要。

通过桥接你已经使用的工具，而不是要求你迁移到新平台，Clawd.bot 代表了一种**去平台化的可能性**。未来的 AI 不应该是一个你必须访问的网站或 app，而是一个渗透在你所有数字生活中的层。

这可能才是 AI 的终极形态：**不可见**。

### 风险与反思

当然，这种"把生活交给 AI"的模式也带来风险：

- **过度依赖**：当 AI 帮你处理邮件、安排日程、做决策时，你自己的这些能力会退化吗？
- **黑盒化**：当"如何做"的知识被封装在 AI 里，调试和理解变得困难
- **安全边界**：本地运行的 AI 如果被攻击，影响比云端更直接

Clawd.bot 选择开源，部分缓解了这些问题。但这提醒我们：**技术赋权的同时，也在创造新的脆弱性**。

### 结语：24/7 AI 员工的意义

Clawd.bot 被称为"24/7 全职 AI 员工"，这个定位比"助手"更准确。

"助手"意味着辅助，你还是主导者。"员工"意味着你可以**分配责任、设定目标、评估结果**。这是一种新的人机关系——不是工具使用者，而是**管理者与协作伙伴**。

当每个人都可以拥有一个（或多个）这样的"数字员工"时，工作的本质会改变。组织的边界会变得模糊，个人的生产力会被放大，"一个人 + 一群 AI"可能成为新的基本单位。

这不是科幻，是 2026 年正在发生的现实。

---

## 官方资源

- [官方文档](https://docs.clawd.bot/)
- [CLI 命令参考](https://docs.clawd.bot/cli)
- [入门指南](https://docs.clawd.bot/start/getting-started)
- [配置指南](https://docs.clawd.bot/gateway/configuration)
- [GitHub 仓库](https://github.com/clawdbot/clawdbot)

---

## 参考阅读

- [Clawd Bot Review: Features, Pricing & Alternatives](https://www.banani.co/blog/clawd.bot-review-features-pricing-and-alternatives)
- [Clawdbot Showed Me What the Future of Personal AI Assistants Looks Like](https://www.macstories.net/stories/clawdbot-showed-me-what-the-future-of-personal-ai-assistants-looks-like/)
- [I Tested Clawdbot: The Most Powerful AI Assistant You Have Ever Seen](https://medium.com/ai-software-engineer/i-tested-clawdbot-the-most-powerful-ai-assistant-you-have-ever-seen-and-its-free-b5b803771637)
- [知乎：7×24h「全职AI员工」爆火硅谷](https://zhuanlan.zhihu.com/p/1998816724661846482)

