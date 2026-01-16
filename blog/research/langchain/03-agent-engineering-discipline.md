# Agent Engineering: A New Discipline
Date: Dec 9, 2025
Source: https://www.blog.langchain.com/agent-engineering-a-new-discipline/

## The Core Problem

**Gap:** "it works on my machine" → "it works in production"

**Challenge:**
- Traditional software: known inputs, defined outputs
- Agents: users can say anything, behavior space wide open
- Power = unpredictability

## What is Agent Engineering?

**Definition:** Iterative process of refining non-deterministic LLM systems into reliable production experiences.

**Process:** Build → Test → Ship → Observe → Refine → Repeat

**Key Principle:** Shipping isn't the end goal, it's how you learn and improve.

## Three Core Skillsets

### 1. Product Thinking
- Write prompts (hundreds/thousands of lines)
- Understand "job to be done"
- Define evaluations for intended behavior
- Requires: Communication skills, writing ability

### 2. Engineering
- Build tools for agents
- Develop UI/UX (streaming, interrupts)
- Create robust runtimes:
  - Durable execution
  - Human-in-the-loop pauses
  - Memory management

### 3. Data Science
- Build measurement systems:
  - Evaluations
  - A/B testing
  - Monitoring
- Analyze usage patterns
- Error analysis (broader scope than traditional software)

## Where Agent Engineering Appears

**Not a new job title** - extends existing roles:

- **Software/ML Engineers:**
  - Write prompts
  - Build agent tools
  - Trace tool calls
  - Refine underlying models

- **Platform Engineers:**
  - Build agent infrastructure
  - Handle durable execution
  - Implement human-in-the-loop workflows

- **Product Managers:**
  - Write prompts
  - Define agent scope
  - Ensure problem-solution fit

- **Data Scientists:**
  - Measure reliability
  - Identify improvement opportunities

**Collaboration Pattern:** Rapid iteration across roles
- Engineers trace errors → PMs tweak prompts
- PMs identify scope issues → Engineers build new tools

## Why Now?

### Two Fundamental Shifts

1. **LLMs Handle Complex Workflows**
   - Whole jobs, not just tasks
   - Examples:
     - Clay: prospect research → outreach → CRM updates
     - LinkedIn: talent pool scanning → ranking → surfacing matches
   - Meaningful business value in production

2. **Power Comes with Unpredictability**
   - Multi-step reasoning
   - Tool calling
   - Context adaptation
   - Different from traditional software

### Key Differences from Traditional Software

| Aspect | Traditional Software | Agents |
|--------|---------------------|--------|
| **Inputs** | Predictable, defined | Every input is edge case |
| **Debugging** | Standard methods | Inspect each decision/tool call |
| **"Working"** | Binary (up/down) | Not binary (can be "off the rails") |
| **Validation** | Unit tests, integration tests | Different interpretation possible |

**Critical Challenges:**

1. **No "normal" input**
   - Natural language = infinite variation
   - "make it pop" or "do what you did last time but differently"
   - Human-like interpretation variability

2. **New debugging paradigm**
   - Logic lives inside model
   - Must inspect each decision
   - Small prompt changes = huge behavior shifts

3. **"Working" isn't binary**
   - 99.99% uptime ≠ reliable
   - Questions matter:
     - Right calls?
     - Correct tool usage?
     - Following intent?

## Agent Engineering in Practice

### Development Cadence

1. **Build Foundation**
   - Simple LLM call with tools → complex multi-agent system
   - Architecture depends on workflow vs agency balance

2. **Test Imaginable Scenarios**
   - Catch obvious issues
   - BUT: Can't anticipate all natural language inputs
   - Mindset shift: "test reasonably, ship to learn"
   - NOT: "test exhaustively, then ship"

3. **Ship to See Reality**
   - Immediate exposure to unconsidered inputs
   - Every production trace shows actual needs

4. **Observe**
   - Trace every interaction:
     - Full conversation
     - Every tool called
     - Exact context per decision
   - Run evals on production data
   - Measure: accuracy, latency, satisfaction, etc.

5. **Refine**
   - Identify failure patterns
   - Edit prompts
   - Modify tool definitions
   - Add problematic cases to regression tests
   - Continuous process

6. **Repeat**
   - Ship improvements
   - Watch production changes
   - Each cycle teaches something new
   - Learn: user interactions, reliability definition

## Success Pattern

**Common trait of successful teams:**
- Stopped trying to perfect before launch
- Treat production as primary teacher
- Trace every decision
- Evaluate at scale
- Ship improvements in days (not quarters)

## The Opportunity

**Requirements for reliable agents:**
- Systematic iteration work
- No shortcuts
- Production-first learning

**The Question:** Not whether agent engineering becomes standard, but how quickly teams can adopt it.

## Key Insights

1. **Shipping = Learning**: Production is where you discover what matters
2. **Systematic Iteration**: Faster cycles = more reliable agents
3. **Cross-functional**: Product + Engineering + Data Science together
4. **New Standards**: Different from traditional software development
5. **Empirical Foundation**: Data-driven refinement essential
