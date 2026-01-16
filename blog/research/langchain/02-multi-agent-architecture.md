# Choosing the Right Multi-Agent Architecture
Author: Sydney Runkle
Date: Jan 14, 2026
Source: https://www.blog.langchain.com/choosing-the-right-multi-agent-architecture/

## When to Use Multi-Agent Architectures

**Start with single agents** - they're simpler to build, reason about, and debug.

Two main constraints drive multi-agent adoption:

1. **Context Management**
   - Specialized knowledge doesn't fit in single prompt
   - Need strategies to selectively surface information
   - Context windows and latency are practical limits

2. **Distributed Development**
   - Different teams maintain capabilities independently
   - Clear boundaries and ownership needed
   - Monolithic prompts become difficult to manage

## Performance Evidence

Anthropic's multi-agent research system:
- Architecture: Claude Opus 4 (lead) + Claude Sonnet 4 (subagents)
- Performance: 90.2% improvement over single-agent Opus 4
- Key: Parallel reasoning across separate context windows

## Four Multi-Agent Patterns

### 1. Subagents: Centralized Orchestration

**How it works:**
- Supervisor coordinates specialized stateless subagents
- Main agent maintains conversation context
- Centralized routing through main agent
- Can invoke multiple subagents in parallel

**Best for:**
- Multiple distinct domains (calendar, email, CRM)
- Centralized workflow control needed
- Subagents don't converse directly with users
- Examples: Personal assistants, research systems

**Tradeoff:**
- Extra model call per interaction (latency + tokens)
- Provides centralized control and context isolation

**Implementation:**
- Deep Agents provides out-of-the-box implementation

### 2. Skills: Progressive Disclosure

**How it works:**
- Agent loads specialized prompts on-demand
- Skills = directories with instructions, scripts, resources
- Three-level detail: skill names → full context → additional files
- Dynamic persona adoption

**Best for:**
- Single agent with many specializations
- No constraint enforcement between capabilities needed
- Team distribution with skill ownership
- Examples: Coding agents, creative assistants

**Tradeoff:**
- Context accumulates in conversation history (token bloat)
- Simplicity and direct user interaction throughout

**Note:** Quasi-multi-agent - single agent with dynamic specializations

### 3. Handoffs: State-Driven Transitions

**How it works:**
- Active agent changes based on conversation context
- Agents transfer via tool calling
- State updates determine next agent
- Can change agent or modify current agent's prompt/tools
- State persists across turns

**Best for:**
- Customer support with information collection stages
- Multi-stage conversational experiences
- Sequential constraints and precondition unlocking

**Tradeoff:**
- More stateful (careful state management needed)
- Enables fluid multi-turn conversations

### 4. Router: Parallel Dispatch and Synthesis

**How it works:**
- Routing step classifies and directs input
- Invokes 0+ specialized agents in parallel
- Synthesizes results into coherent response
- Typically stateless per request

**Best for:**
- Distinct verticals (separate knowledge domains)
- Parallel queries across multiple sources
- Result synthesis from multiple agents
- Examples: Enterprise knowledge bases, multi-vertical support

**Tradeoff:**
- Stateless = consistent performance but repeated routing overhead
- Can wrap as tool in stateful agent to mitigate

## Pattern Selection Framework

| Requirements | Pattern |
|-------------|---------|
| Multiple domains + parallel execution | **Subagents** |
| Many specializations + lightweight | **Skills** |
| Sequential workflow + user interaction | **Handoffs** |
| Distinct verticals + parallel synthesis | **Router** |

## Capability Matrix

| Pattern | Distributed Dev | Parallelization | Multi-hop | Direct User Interaction |
|---------|----------------|-----------------|-----------|------------------------|
| Subagents | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| Skills | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Handoffs | — | — | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Router | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | — | ⭐⭐⭐ |

## Performance Analysis

### Scenario 1: One-Shot Request ("buy coffee")

| Pattern | Model Calls |
|---------|------------|
| Handoffs, Skills, Router | 3 |
| Subagents | 4 |

**Insight:** Subagents adds overhead for centralized control

### Scenario 2: Repeat Request

| Pattern | Turn 2 Calls | Total | Efficiency Gain |
|---------|-------------|-------|----------------|
| Handoffs, Skills | 2 | 5 | 40% |
| Router | 3 | 6 | 25% |
| Subagents | 4 | 8 | — |

**Insight:** Stateful patterns save 40-50% on repeats

### Scenario 3: Multi-Domain Query (3 languages, ~2K tokens each)

| Pattern | Calls | Tokens | Notes |
|---------|-------|--------|-------|
| Subagents, Router | 5 | ~9K | Parallel execution |
| Skills | 3 | ~15K | Context accumulation |
| Handoffs | 7+ | ~14K+ | Sequential only |

**Insight:**
- Parallel patterns (Subagents, Router) most efficient
- Subagents: 67% fewer tokens than Skills (context isolation)
- Skills has fewer calls but high token usage
- Handoffs can't leverage parallel tool calling

## Performance Summary

| Pattern | Single Requests | Repeat Requests | Parallel Execution | Large Context |
|---------|----------------|-----------------|-------------------|---------------|
| Subagents | — | — | ✅ | ✅ |
| Skills | ✅ | ✅ | — | — |
| Handoffs | ✅ | ✅ | — | — |
| Router | ✅ | — | ✅ | ✅ |

## Getting Started Recommendations

1. **Start simple**: Single agent + good prompt engineering
2. **Add tools before agents**: Extend capabilities first
3. **Graduate to multi-agent**: Only when hitting clear limits
4. **Quick start**: Deep Agents combines subagents + skills
