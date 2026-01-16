# Doubling Down on DeepAgents
Date: Oct 28, 2025
Source: https://www.blog.langchain.com/doubling-down-on-deepagents/

## What are Deep Agents?

**Definition:** Agents able to do complex, open-ended tasks over longer time horizons.

### Four Key Elements

1. **Planning tool** - for task decomposition and strategy
2. **Filesystem access** - for context and state management
3. **Subagents** - for specialized task delegation
4. **Detailed prompts** - for behavior guidance

## DeepAgents 0.2 Release

### Major New Feature: Pluggable Backends

**Previous (0.1):**
- "Virtual filesystem" using LangGraph state

**New (0.2):**
- Backend abstraction allows any filesystem
- Built-in implementations:
  - LangGraph State
  - LangGraph Store (cross-thread persistence)
  - Local filesystem

### Composite Backends

**Concept:** Base backend + mapped backends at subdirectories

**Example Use Case - Long-term Memory:**
```
Base: Local filesystem
Map: /memories/ → S3-backed virtual filesystem
Result: Agent can persist memories beyond local computer
```

**Extensibility:**
- Write custom backends for any database/data store
- Subclass existing backends for:
  - File write guardrails
  - Format checking
  - Access control

### Other 0.2 Improvements

1. **Large Tool Result Eviction**
   - Auto-dump large results to filesystem
   - Triggered when exceeding token limit

2. **Conversation History Summarization**
   - Auto-compress old conversation history
   - Maintains token budget

3. **Dangling Tool Call Repair**
   - Fix message history when tool calls interrupted/cancelled
   - Ensures consistency before execution

## When to Use What?

### Library Positioning

| Library | Role | Best For |
|---------|------|----------|
| **LangGraph** | Agent Runtime | Workflows + agents combinations |
| **LangChain** | Agent Framework | Core loop, build from scratch |
| **DeepAgents** | Agent Harness | Autonomous, long-running agents |

### DeepAgents Specifics

**Use DeepAgents when:**
- Building autonomous agents
- Need long-running capabilities
- Want built-in features:
  - Planning tools
  - Filesystem access
  - Subagent support
  - Context management

**Architecture:**
```
DeepAgents (harness)
    ↓ built on
LangChain (framework)
    ↓ built on
LangGraph (runtime)
```

## Key Concepts

### Virtual Filesystem
- Abstraction over any storage backend
- Enables:
  - Cross-session persistence
  - Multi-location state
  - Custom guardrails
  - Format validation

### Context Management
- Token budget awareness
- Automatic eviction strategies
- History compression
- State delegation to filesystem

### Extensibility Points

1. **Custom Backends**
   - Implement storage interface
   - Connect to your infrastructure
   - Examples: S3, databases, custom APIs

2. **Backend Subclassing**
   - Add validation
   - Implement access control
   - Enforce formats
   - Custom error handling

3. **Composite Strategies**
   - Mix multiple backends
   - Directory-based routing
   - Tiered storage (local + cloud)

## Use Case Examples

### Long-term Memory
```
/workspace/ → Local (working files)
/memories/ → S3 (persistent knowledge)
```

### Multi-environment
```
/dev/ → Local filesystem
/prod/ → Database backend
/cache/ → In-memory LangGraph state
```

### Tiered Storage
```
/recent/ → Fast local storage
/archive/ → Cloud storage (S3, etc.)
```

## Comparison with Alternatives

### vs LangGraph
- **LangGraph:** More control, workflow-agent mix
- **DeepAgents:** Opinionated, batteries-included for autonomy

### vs LangChain
- **LangChain:** Pure framework, maximum flexibility
- **DeepAgents:** Harness with built-ins, less setup

## Getting Started

**Bring:**
- Custom tools for your domain
- Custom prompt for behavior
- Choose/configure backend

**Get:**
- Planning capabilities
- Filesystem access
- Subagent coordination
- Context management
- History handling

## Future Direction

Focus on autonomous, long-running agent use cases with:
- Improved context management
- Better backend abstractions
- Enhanced tooling
- Production-ready defaults
