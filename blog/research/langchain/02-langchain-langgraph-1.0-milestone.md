# LangChain 和 LangGraph 智能体框架达到 v1.0 里程碑

> 原文链接：[LangChain and LangGraph Agent Frameworks Reach v1.0 Milestones](https://www.blog.langchain.com/langchain-langgraph-1dot0/)  
> 发布时间：2025年10月22日  
> 作者：Sydney Runkle 和 LangChain OSS 团队

---

## 引言：首个主要版本发布

我们正在发布 **LangChain 1.0** 和 **LangGraph 1.0**——我们开源框架的首次主要版本！经过多年的反馈，我们更新了 `langchain` 以专注于核心智能体循环，通过新的中间件概念提供灵活性，并使用最新的内容类型升级模型集成。

这两个框架服务于不同的目的：

- **LangChain** 是构建 AI 智能体的最快方式——具有标准工具调用架构、提供商无关的设计和用于定制的中间件
- **LangGraph** 是一个低级框架和运行时，适用于高度定制和可控的智能体，设计用于支持生产级、长时间运行的智能体

这些 1.0 版本标志着我们对开源库稳定性的承诺，在 2.0 之前不会有破坏性更改。随着这些版本的发布，我们还推出了完全重新设计的[文档网站](https://docs.langchain.com/oss/python/langchain/overview?ref=blog.langchain.com)。

---

## LangChain 1.0

LangChain 始终提供用于与 LLM 交互和构建智能体的高级接口。通过标准化的模型抽象和预构建的智能体模式，它帮助开发者快速部署 AI 功能并构建复杂的应用程序，而无需供应商锁定。在一个任何给定任务的最佳模型经常变化的空间中，这至关重要。

### 我们一直在倾听

在过去三年中，我们听到了一致的反馈：LangChain 的抽象有时过于繁重，包表面积变得庞大，开发者希望在不降级到原始 LLM 调用的情况下对智能体循环有更多控制权。当他们的用例偏离我们的预构建模式时，有些人在定制方面遇到了困难。我们认真对待这些反馈。**LangChain 1.0 是我们的回应**——一个深思熟虑的改进，保留了有效的东西，同时修复了无效的东西。

> "我们严重依赖 LangGraph 在底层提供的持久运行时来支持我们的智能体开发，而 LangChain 1.0 中新的智能体预构建和中间件使其比以前灵活得多。我们对 1.0 感到兴奋，并已经在 Rippling 使用新功能进行构建。" —— **Ankur Bhatt，Rippling AI 负责人**

我们在 LangChain 1.0 中专注于三件事：

1. **我们新的 `create_agent` 抽象**：使用任何模型提供商构建智能体的最快方式
   - 基于 LangGraph 运行时构建，帮助支持可靠的智能体
   - 预构建和用户定义的中间件支持逐步控制和定制

2. **标准内容块**：模型输出的提供商无关规范

3. **精简的表面积**：我们正在精简我们的命名空间，专注于开发者用于构建智能体的内容

### 1. `create_agent` 抽象

`create_agent` 抽象围绕核心智能体循环构建，使快速入门变得容易。以下是循环的工作方式：

**设置**：选择一个模型并给它一些工具和提示词。

**执行**：

1. 向模型发送请求
2. 模型响应：
   - 工具调用 → 执行工具并将结果添加到对话中
   - 最终答案 → 返回结果
3. 从步骤 1 重复

![Agent Loop](https://www.blog.langchain.com/content/images/2025/10/Screenshot-2025-10-08-at-5.15.25---PM--1-.png)

新的 `create_agent` 函数在底层使用 LangGraph 运行此循环。它与 `langgraph.prebuilts` 中的 `create_react_agent` 函数感觉非常相似，该函数已经在生产中使用了一年。

在 `langchain` 中开始使用智能体很容易：

```python
from langchain.agents import create_agent

weather_agent = create_agent(
    model="openai:gpt-5",
    tools=[get_weather],
    system_prompt="Help the user by fetching the weather in their city.",
)

result = agent.invoke({"role": "user", "what's the weather in SF?"})
```

大多数智能体构建器都非常限制，因为它们不允许在这个核心循环之外进行定制。这就是 `create_agent` 通过我们引入的**中间件（Middleware）**脱颖而出的地方。

#### 中间件（Middleware）

中间件定义了一组钩子，允许你在智能体循环中定制行为，在智能体采取的每一步实现细粒度控制。

我们为常见用例包含了一些内置中间件：

- **人工在环（Human-in-the-loop）**：暂停智能体执行，让用户在工具调用执行之前批准、编辑或拒绝它们。这对于与外部系统交互、发送通信或进行敏感交易的智能体至关重要。

- **摘要（Summarization）**：当消息历史接近上下文限制时压缩消息历史，保持最近的消息完整，同时总结较旧的上下文。这可以防止令牌溢出错误，并保持长时间运行的智能体会话性能。

- **PII 编辑（PII redaction）**：使用模式匹配来识别和编辑敏感信息，如电子邮件地址、电话号码和社会安全号码，然后再将内容传递给模型。这有助于维护隐私法规的合规性，并防止用户数据的意外暴露。

LangChain 还支持**自定义中间件**，这些中间件挂接到智能体循环中的各个点。下图展示了这些钩子：

![Middleware Hooks](https://www.blog.langchain.com/content/images/2025/10/middleware_final--2-.png)

#### 结构化输出生成

我们还通过将其合并到主模型 ↔ 工具循环中来改进智能体循环中的结构化输出生成。这通过消除了以前在主循环之外发生的额外 LLM 调用，从而减少了延迟和成本。

开发者现在可以细粒度地控制如何生成结构化输出，无论是通过工具调用还是提供商原生结构化输出。

```python
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from pydantic import BaseModel

class WeatherReport(BaseModel):
    temperature: float    
    condition: str

agent = create_agent(
    "openai:gpt-4o-mini",
    tools=[weather_tool],
    response_format=ToolStrategy(WeatherReport),
    prompt="Help the user by fetching the weather in their city.",
)
```

### 2. 标准内容块

LangChain 的数百个提供商集成（OpenAI、Anthropic 等）在 1.0 中基本保持不变。这些抽象使用的接口位于 `langchain-core` 中，我们正在将其升级到 1.0，并添加一个关键特性：**标准化内容块**。

LangChain 的价值很大程度上来自其提供商无关的接口，允许开发者在单个应用程序中使用跨多个提供商的通用协议。没有标准内容块，切换模型或提供商经常会破坏流、UI 和前端以及内存存储。消息上的新 `.content_blocks` 属性提供：

- 跨提供商的一致内容类型
- 支持推理 trace、引用和工具调用——包括服务器端工具调用
- 复杂响应结构的类型化接口
- 完全向后兼容

这使 LangChain 的抽象与现代 LLM 功能（如推理、引用和服务器端工具执行）保持同步，同时最大限度地减少破坏性更改。

### 3. 精简包

LangChain 1.0 将包范围减少到基本抽象。旧功能移动到 `langchain-classic` 以实现向后兼容。随着框架的成熟，我们了解了哪些模式最重要。这个精简的包切断了多年积累的功能，使 LangChain 既简单又强大。

**主要更改：**

- 在 LangChain 中引入 `create_agent`，在 `langgraph.prebuilt` 中弃用 `create_react_agent`
- 由于 2025 年 10 月 EOL 而放弃 Python 3.9 支持，v1.0 需要 Python 3.10+
  - Python 3.14 支持即将推出！

- 包表面积减少到专注于核心抽象，旧功能移动到 `langchain-classic`

![Package Changes](https://www.blog.langchain.com/content/images/2025/10/Screenshot-2025-10-10-at-11.16.22---PM--1--1-.png)

#### 安装

```bash
# Python
uv pip install --upgrade langchain
uv pip install langchain-classic

# JavaScript
npm install @langchain/langchain@latest
npm install @langchain/langchain-classic
```

#### 迁移

如果你从以前版本的 LangChain 升级，我们创建了详细的资源来指导你完成这些更改。

**版本概述**：[Python](https://docs.langchain.com/oss/python/releases/langchain-v1?ref=blog.langchain.com)，[JavaScript](https://docs.langchain.com/oss/javascript/releases/langchain-v1?ref=blog.langchain.com)

**迁移指南**：[Python](https://docs.langchain.com/oss/python/migrate/langchain-v1?ref=blog.langchain.com)，[JavaScript](https://docs.langchain.com/oss/javascript/migrate/langchain-v1?ref=blog.langchain.com)

---

## LangGraph 1.0

AI 智能体正从原型转向生产，但持久性、可观察性和人工在环控制等核心功能仍然服务不足。

**LangGraph 1.0 通过强大的基于图的执行模型解决了这些差距，并为可靠的智能体系统提供生产就绪的功能：**

- **持久状态** - 你的智能体的执行状态自动持久化，因此如果你的服务器在对话中间重新启动，或者长时间运行的工作流被中断，它会在完全停止的地方继续，而不会丢失上下文或强制用户重新开始。

- **内置持久化** - 在任何点保存和恢复智能体工作流，而无需编写自定义数据库逻辑，实现用例如多天批准流程或跨多个会话运行的后台作业。

- **人工在环模式** - 使用一流的 API 支持暂停智能体执行以供人工审查、修改或批准，使构建人类保持对高风险决策控制的系统变得微不足道。

要深入了解我们的设计理念，请查看我们关于[从第一原则构建 LangGraph](https://www.blog.langchain.com/building-langgraph/)的博客文章。

这是持久智能体框架空间中第一个稳定的主要版本——这是生产就绪 AI 系统的主要里程碑。经过一年多的迭代和 Uber、LinkedIn 和 Klarna 等公司的广泛采用，LangGraph 正式达到 v1。

### 破坏性更改和迁移

唯一值得注意的更改是弃用 `langgraph.prebuilt` 模块，增强功能移动到 `langchain.agents`。

LangGraph 1.0 保持完全向后兼容。

#### 安装

```bash
# Python
uv pip install --upgrade langgraph

# JavaScript
npm install @langchain/langgraph@latest
```

---

## 何时使用每个框架

LangChain 让你使用高级抽象快速构建和部署智能体，而 LangGraph 为需要定制化的复杂工作流提供细粒度控制。

最好的部分？LangChain 智能体建立在 LangGraph 之上，所以你不会被锁定。从 LangChain 的高级 API 开始，当你需要更多控制时无缝降级到 LangGraph。由于图是可组合的，你可以混合两种方法——随着你的需求发展，在自定义 LangGraph 工作流中使用通过 `create_agent` 创建的智能体。

### 选择 LangChain 1.0 用于：

- 使用标准智能体模式快速部署
- 适合默认循环（模型 → 工具 → 响应）的智能体
- 基于中间件的定制
- 高级抽象优于低级控制

### 选择 LangGraph 1.0 用于：

- 确定性和智能体组件混合的工作流
- 长时间运行业务流程自动化
- 需要更多监督/人工在环的敏感工作流
- 高度定制或复杂的工作流
- 需要仔细控制延迟和/或成本的应用程序

---

## 文档和资源

我们正在 [docs.langchain.com](https://docs.langchain.com/?ref=blog.langchain.com) 推出一个改进得多的文档网站。第一次，所有 LangChain 和 LangGraph 文档——跨 Python 和 JavaScript——生活在一个统一的网站中，具有并行示例、共享概念指南和合并的 API 参考。

新文档具有更直观的导航、深思熟虑的指南和常见智能体架构的深入教程。

---

## 感谢和反馈

我们希望你喜欢这些 1.0 版本。我们非常感谢在多年中压力测试 LangChain 和 LangGraph 使它们成为今天的样子的社区。每月 9000 万次下载，为 Uber、JP Morgan、Blackrock、Cisco 等公司的生产应用程序提供支持，我们对你所有人有责任继续创新，但也成为构建智能体的最可靠框架。

虽然这是一个主要里程碑，但我们仍处于软件重大变化的开始。我们想听到你的声音：在 [LangChain 论坛](https://forum.langchain.com/t/launch-week-is-here-oss-1-0s-insights-agent-and-no-code-agent-builder/1890?ref=blog.langchain.com)发帖告诉我们你对 1.0 版本的看法以及你正在构建什么。

---

## 总结

LangChain 1.0 和 LangGraph 1.0 的发布标志着智能体开发框架成熟的重要里程碑。这两个框架为不同的使用场景提供了清晰的路径：

- **LangChain 1.0**：专注于快速开发和标准化模式，通过 `create_agent` 抽象和中间件系统提供灵活性和易用性的平衡
- **LangGraph 1.0**：专注于生产级、长时间运行的智能体，提供持久化状态、人工在环控制和高度定制化能力

这两个框架的协同设计（LangChain 建立在 LangGraph 之上）确保了开发者可以从快速原型无缝过渡到生产就绪系统，而无需重写代码或切换框架。

---

**相关资源：**
- [LangChain 1.0 Python 文档](https://docs.langchain.com/oss/python/langchain/overview)
- [LangGraph 1.0 Python 文档](https://docs.langchain.com/oss/python/langgraph/overview)
- [迁移指南：Python](https://docs.langchain.com/oss/python/migrate/langchain-v1)
- [迁移指南：JavaScript](https://docs.langchain.com/oss/javascript/migrate/langchain-v1)
- [LangChain 论坛讨论](https://forum.langchain.com/t/launch-week-is-here-oss-1-0s-insights-agent-and-no-code-agent-builder/1890)