# 2025 AI 工程师阅读清单：从大模型到智能体的 50 篇必读精选

> **来源说明**：本文整理自 [Latent Space](https://www.latent.space/p/2025-papers) 发布的《The 2025 AI Engineer Reading List》。这份清单由 AI 领域的专家社区策划，旨在为从零开始或希望在实战中进阶的 AI 工程师提供一份详尽的“必读书单”。

## 核心设计理念
- **精简高效**：精选约 50 篇论文/项目，平均每周读一篇。
- **直击痛点**：不仅是罗列名称，更解释了“为什么这重要”。
- **实战导向**：跳过了过时的理论，聚焦于 2025 年 AI 工程师在工作中真正需要的知识。

---

## 目录
1. [前沿大模型 (Frontier LLMs)](#1-前沿大模型)
2. [基准测试与评估 (Benchmarks and Evals)](#2-基准测试与评估)
3. [提示工程与思维链 (Prompting & CoT)](#3-提示工程与思维链)
4. [检索增强生成 (RAG)](#4-检索增强生成)
5. [智能体 (Agents)](#5-智能体)
6. [代码生成 (Code Generation)](#6-代码生成)
7. [视觉 (Vision)](#7-视觉)
8. [语音 (Voice)](#8-语音)
9. [图像/视频扩散模型 (Diffusion)](#9-图像视频扩散模型)
10. [微调 (Finetuning)](#10-微调)

---

## 1. 前沿大模型 (Frontier LLMs)
**核心关注点**：理解领先实验室的技术路径和推理模型的崛起。

- **主流梯队**：GPT 系列（GPT-4 到 o1/o3）、Claude 3/4、Gemini 1/2.5。
- **开源力量**：Llama 1-3 系列及其变体（Mistral, Qwen 3）。
- **DeepSeek 现象**：DeepSeek V1-V3, R1, 尤其是其 **GRPO** 强化学习算法。
- **推理模型 (Reasoning)**：2025 年的焦点是 o1, R1 和 QwQ。必读：[Let’s Verify Step By Step](https://arxiv.org/abs/2305.20050)。

## 2. 基准测试与评估 (Benchmarks and Evals)
**核心关注点**：不要被刷榜误导，学会评估模型的真实能力。

- **综合知识**：MMLU Pro, GPQA Diamond。
- **长文本能力**：**MRCR** (OpenAI 采用) 取代了过时的 Needle in a Haystack。
- **指令遵循**：IFEval 是目前最领先的评估方式。
- **抽象推理**：**ARC AGI** 挑战赛，被视为模型“智商”的真正试金石。

## 3. 提示工程与思维链 (Prompting & CoT)
**核心关注点**：人类是糟糕的零样本提示者，学会让 LLM 优化提示。

- **必读综述**：[The Prompt Report](https://arxiv.org/abs/2406.06608)。
- **核心技术**：Chain-of-Thought (CoT), Tree of Thought (引入回溯机制)。
- **自动化趋势**：**DSPy** 框架，通过算法而非手工调整来优化提示。
- **安全防范**：理解提示注入 (Prompt Injection) 的原理与防御。

## 4. 检索增强生成 (RAG)
**核心关注点**：RAG 本质上是信息检索 (IR) 问题，不仅仅是向量数据库。

- **基础理论**：了解 TF-IDF, BM25 等传统 IR 技术。
- **RAG 2.0**：Contextual AI 提出的新范式；掌握 HyDE, 重新排序 (Rerankers) 和多模态数据处理。
- **知识图谱**：**GraphRAG** (Microsoft) 是 2024-2025 年的热门趋势。
- **评估框架**：RAGAS 和 Nvidia 的 FACTS 框架。

## 5. 智能体 (Agents)
**核心关注点**：从单纯的聊天机器人转向具备规划和工具调用能力的智能系统。

- **核心基准**：**SWE-bench** (解决真实 GitHub Issue 的能力)。
- **架构设计**：**ReAct** (推理+行动)；**MemGPT** (模拟长效记忆)。
- **认知架构**：Voyager (Curriculum, Skill Library, Sandbox)。
- **最佳实践**：Anthropic 发布的 [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)。

## 6. 代码生成 (Code Generation)
**核心关注点**：Frontier 已从研究转向工业实战（如 Devin, Cursor）。

- **开源模型**：Qwen2.5-Coder, DeepSeek-Coder。
- **评估体系**：LiveCodeBench, BigCodeBench。
- **安全与批判**：OpenAI 的 **CriticGPT**，用于识别 AI 生成代码中的安全隐患。

## 7. 视觉 (Vision)
**核心关注点**：从单纯的 OCR 转向原生多模态理解。

- **基础模型**：CLIP (ViT 鼻祖), SAM 2 (视频分割)。
- **多模态路径**：区分 Early Fusion (如 Flamingo, Chameleon) 与 Late Fusion。
- **实战利器**：Pixtral, Gemini 2.0 Flash。

## 8. 语音 (Voice)
**核心关注点**：全双工、低延迟的语音交互正在成为标准。

- **标杆项目**：Whisper (ASR), NaturalSpeech (TTS)。
- **新突破**：**Kyutai Moshi** (开源全双工模型)。
- **多模态融合**：语音与视觉在 2025 年正加速合流（如 Gemini 2.0 原生多模态）。

## 9. 图像/视频扩散模型 (Diffusion)
**核心关注点**：从图片生成进化到物理世界模拟。

- **主流架构**：Stable Diffusion (SDXL, SD3), BFL Flux。
- **视频生成**：**Sora** 及其开源对手 (OpenSora, Wan 2.1)。
- **自回归生成**：Llama 3 和 Gemini 2.0 中出现的原生图像生成。

## 10. 微调 (Finetuning)
**核心关注点**：廉价、高效的定制化，不再是昂贵的特权。

- **必掌握技术**：LoRA / QLoRA (低秩适配)。
- **偏好对齐**：**DPO** (直接偏好优化) 已成为 OpenAI 也支持的标准。
- **强化学习**：推理模型的微调（RL Finetuning for reasoning）。
- **实战工具**：**Unsloth** 笔记本和 HuggingFace 的微调指南。

---

## 结语：如何开始？
AI 领域的变化极快，与其迷失在论文海中，不如**挑选一个领域深挖**。
- 如果你关注 RAG，请阅读 GraphRAG 和 RAGAS。
- 如果你对 Agent 感兴趣，请务必读完 Anthropic 的 Agents 指南。
- 如果你追求模型性能，请关注 Unsloth 的最新动态。

保持好奇，持续实战。