5 AI Prompts to Help You Design Prompts Like a Pro
Stop guessing and start engineering. A step-by-step method for designing prompts that are reliable, reusable, and measurable, plus 5 tested prompts and research-backed tips.
Excellent AI Prompts
Nov 17, 2025

You’re on your seventh iteration with ChatGPT, watching it drift further from what you actually need. The problem isn’t the model, it’s that you asked for an outcome without designing the task. The AI had to guess your success criteria, invent its own method, and hope it landed somewhere near useful. Most times it just wastes an hour you’ll never get back.

When you treat prompts like specifications instead of questions, you define the method before asking for results. You set explicit success criteria. You structure the output format. You create the environment for the model to stop guessing and start executing.

This is less about writing longer prompts or using magic words and all about designing the task the way you’d brief a junior analyst who’s competent but needs clear direction. Most people never make this shift, which is why they’re stuck in iteration loops while others are shipping finished work in the first chat round.

Today’s prompts will show you exactly how to do this.

If you are getting value from this, subscribe now, and consider the paid edition as a tiny part of your monthly R&D budget that can return thousands over your career.

Type your email...
Subscribe
Why structured prompts outperform clever ones
Modern models reward specifications over questions
OpenAI and Anthropic both teach the same thing in their engineering guides, clear roles, explicit success criteria, and defined constraints improve output quality more than any other factor. The labs know what works because they’ve tested it at scale across millions of prompts. When you tell the model what to do and how to do it, performance jumps and iteration drops.

Supplying method beats hoping the model invents one
When researchers tested different prompting approaches, they found that giving the model a structured method consistently outperformed leaving it to figure out its own approach. Self-Discover had models compose their own reasoning structures before executing, improving accuracy on reasoning benchmarks. Skeleton-of-Thought had models plan an outline before writing, improving both speed and coherence. The pattern holds across different tasks—defined process produces better results than undefined requests.

The modular approach changes everything
Instead of writing one massive prompt and hoping it works, break your task into discrete steps. One prompt extracts facts. Another structures them. A third writes from the structure. Each step has clear inputs, a defined method, and explicit success criteria. You can test each piece, optimize what matters, and reuse what works. This is how you go from “try again” loops to repeatable systems.

Here are five patterns that apply this thinking to the tasks you’re probably running right now.

Resources: OpenAI Prompt Engineering, Anthropic Prompting Guide, Self-Discover, Skeleton-of-Thought, Chain-of-Verification, DSPy

5 AI prompts for designing prompts that work
Prompt 1: Task decomposer - Force the model to propose and compare solution methods before executing

Prompt 2: Skeleton writer - Outline first, expand second, eliminate structural drift

Prompt 3: Source-grounded writer - Extract claims, verify sources, write only from validated information

Prompt 4: Spec-as-code - Convert messy requests into precise specifications before generating anything

Prompt 5: Evaluator-in-the-loop - Make the model critique and revise its own work against your criteria

Each pattern solves a specific failure mode. Use them when the structure matters more than speed.

Prompt 1: Task decomposer - force method selection before execution
THE PURPOSE: Most bad outputs come from the model choosing a weak approach and executing it confidently. This pattern forces the model to propose multiple solution methods, compare them explicitly, and justify its choice before generating anything. You get intentional workflow design instead of whatever path the model happened to take first.

Copy and customize this prompt:

You are a systems designer solving complex tasks.

**Goal**: [Describe the outcome you need in one sentence]

**Constraints**: 
- Timeline: [How fast do you need this]
- Audience: [Who will use this]
- Tone: [How should this sound]
- Format: [What form should the output take]

**Task**: Propose two different solution methods.

For each method:
1. Name it clearly
2. List 5 specific steps
3. Estimate time required
4. Identify the biggest risk

Create a comparison table:
| Method | Strength | Risk | Speed | Quality |
|--------|----------|------|-------|---------|

**Choose one method** with a two-sentence rationale explaining why this approach beats the alternative for this specific use case.

**Execute the chosen method**. Show your work at each step. Number the steps as you complete them.

**Final output**: Deliver the result plus a 5-item risk register with specific mitigations for each risk.
Before/after example:

Bad prompt: “Write a project plan for launching our new API documentation.”

Good prompt: Uses the pattern above, forcing the model to compare timeline-focused vs quality-focused vs user-testing-focused approaches, then execute the selected method with visible checkpoints.

Result: Instead of getting a generic project plan, you get a deliberate method comparison, a justified choice, and execution with built-in quality checks. No iteration needed.

If this newsletter helps you think sharper or earn more, hit subscribe, and when you are ready for the full workflows and money moves, upgrade to paid.

Type your email...
Subscribe
Prompt 2: Skeleton writer - outline before expanding
THE PURPOSE: When you ask a model to write directly, it commits to a structure in the first paragraph and locks itself in. This pattern separates structure from content - build the skeleton first, get your approval, then expand each section. You catch structural problems before the model writes 2,000 words in the wrong direction.

Copy and customize this prompt:

You are an outline-first writer.

**Topic**: [What are you writing about]
**Audience**: [Who is this for - be specific about their role and knowledge level]
**Goal**: [What should the reader be able to do after reading this]
**Length target**: [Approximate word count]
**Tone**: [Professional/conversational/technical/etc.]

**Step 1 - Build skeleton**: Create an outline using H2 and H3 headers only. No paragraphs yet. Each header should be specific enough to know exactly what that section will cover.

**Step 2 - Wait for approval**: Show me the skeleton and ask: “Does this structure work, or should I adjust it?”

**Step 3 - Expand sections**: After I approve, expand each section to 2-3 paragraphs, 4-6 sentences each. Keep examples concrete and scoped to [industry/domain].

**Step 4 - Quality check**: 
- Does each section deliver on its header?
- Are transitions clear?
- Is the technical level consistent?
- Would the audience actually use this?

If any check fails, revise that section and explain what changed.
Prompt 3: Source-grounded writer - verify before writing
THE PURPOSE: When accuracy matters more than speed, this pattern forces the model to extract every claim, identify its source, verify it’s actually supported, and write only from validated information. You eliminate hallucination and unsupported assertions before they make it into your final output.

Copy and customize this prompt:

You are a source-grounded analyst who writes only from verified information.

**Task**: Create a [report/brief/analysis] on [topic] for [audience]
**Tone**: [Specify tone]
**Length**: [Target word count]

**Sources**: [Paste your notes, quotes, links, transcripts, or data here. If you don’t have sources yet, tell me what you need before proceeding.]

**Workflow**:

**Step 1 - Extract claims**: Pull 8-15 atomic claims from the sources. For each claim, include:
- The specific claim in one sentence
- Supporting quote or data point
- Exact source (author/publication + date or URL)

**Step 2 - Verification plan**: For any claim without direct citation, write a 1-2 sentence plan: what would you check, where would you look? If it’s unverifiable from available sources, mark it “drop or reframe.”

**Step 3 - Resolve gaps**: Drop unverifiable claims or reframe them as questions/uncertainties. Keep a “dropped or modified” list with brief explanations.

**Step 4 - Write to spec**: Compose the [artifact type] using only the verified claim set. Every significant assertion must trace to a source.

**Step 5 - Inline citations**: After each paragraph containing factual claims, add bracketed citations [Author, Year] or [Source, YYYY-MM-DD].

**Step 6 - Self-check**: Rate these 5 criteria on a 1-5 scale:
- Accuracy (every claim is sourced)
- Coverage (addresses all key aspects)
- Clarity (audience can follow easily)
- Relevance (stays on target)
- Citation quality (sources are clear and accessible)

If any score is below 4, revise once and show only the final version.

**Deliverables**:
- Final [artifact] with inline citations
- “Claims used” table mapping each claim to its source
- “Dropped/modified” list with reasons
Prompt 4: Spec-as-code - convert requests into machine-readable specifications
THE PURPOSE: Messy requests produce messy outputs. This pattern forces the model to convert your initial ask into a structured specification with explicit fields before it generates anything. You catch ambiguity at the requirements level instead of discovering it in round five of revisions.

Copy and customize this prompt:

Convert this request into a JSON specification before proceeding with any work.

**Request**: [Paste your initial ask here, however messy it is]

**Step 1 - Specification design**: Create a JSON spec with these required fields:
{
  “role”: “The perspective the model should take”,
  “inputs”: “What information is provided or needed”,
  “assumptions”: “What we’re assuming is true”,
  “method”: “The specific approach to use”,
  “quality_criteria”: [”List of 5 specific success criteria”],
  “deliverables”: [”What will be produced”],
  “constraints”: [”Timeline, format, audience, or other limits”]
}

**Step 2 - Clarification**: Ask me 3 specific questions about anything ambiguous or missing from my original request.

**Step 3 - Finalize spec**: After I answer, output the complete specification in clean JSON format.

**Step 4 - Execute**: Generate the deliverable strictly according to the finalized spec. If you cannot meet any quality criterion, add it to a “deviations” array and explain why.

**Step 5 - Validation report**: Show which quality criteria were met (Yes/No for each) and list any deviations with explanations.
Why this works: The JSON format forces precision. The clarification questions catch gaps early. The deviation tracking keeps you honest about what actually shipped versus what was specified.

Prompt 5: Evaluator-in-the-loop - critique and revise before delivery
THE PURPOSE: First drafts are rarely final quality. This pattern builds revision into the workflow by forcing the model to evaluate its own output against your criteria, identify weaknesses, and fix them before you ever see the result. You get second-draft quality on the first pass.

Copy and customize this prompt:

You will create [artifact type] and then evaluate it before delivering.

**Task**: [Describe what you need]
**Audience**: [Who this is for]
**Context**: [Any relevant background]

**Step 1 - First draft**: Create the complete [artifact] based on the task description.

**Step 2 - Internal review**: Evaluate your draft against these criteria:

1. [Criterion 1 - be specific, e.g., “Uses data to support every major claim”]
2. [Criterion 2 - e.g., “Stays within 1,000 words”]
3. [Criterion 3 - e.g., “Includes at least 3 concrete examples”]
4. [Criterion 4 - e.g., “Written at [X grade level] reading level”]
5. [Criterion 5 - e.g., “Ends with clear next steps”]

**Scoring**: Rate each criterion 1-5 where:
- 5 = Fully met
- 4 = Mostly met with minor gaps
- 3 = Partially met
- 2 = Significant gaps
- 1 = Not met

For each criterion, write one sentence explaining your score.

**Step 3 - Revision**: If any criterion scored below 4, revise the draft once to address those specific gaps.

**Step 4 - Final delivery**: Show me only:
- The final [artifact] (revised or original if no revision needed)
- Score summary for each criterion
- One paragraph explaining what changed between drafts and why

Do not show me the first draft. I only see the final result and the improvement explanation.
Note: This pattern works best with Claude, which has stronger self-evaluation capabilities than most models.

FAQs
Q: Do I need multi-step prompts for simple tasks?

No. Use a minimal prompt with clear inputs and maybe one example. Save the scaffolding for reasoning tasks or high-stakes work where the cost of iteration actually matters. OpenAI and Anthropic both recommend starting simple, then adding structure only when outputs drift or quality drops. If “write a blog post intro” works fine, don’t engineer it into a six-step process.

Q: Is this “programming not prompting” approach realistic for non-coders?

Yes. You’re thinking in natural language modules, not writing code. One prompt extracts facts. Another structures them. A third writes from the structure. You can run this manually in ChatGPT, or you can adopt frameworks like DSPy later when you want to optimize against metrics and auto-tune your pipeline. The mental model is what matters - breaking tasks into testable pieces instead of hoping one massive prompt works.

Q: When should I actually use these patterns versus just asking normally?

Use these when:

You’re getting inconsistent outputs from the same type of request

The task is high-stakes (client deliverable, published content, strategic analysis)

You’ll run this task repeatedly and want a reusable system

Accuracy matters more than speed (source-grounded writer)

You’re stuck in iteration loops and need to break the cycle

Skip them when:

The task is one-off and low-stakes

A simple prompt already works fine

You’re exploring ideas and want the model to surprise you

Speed matters more than precision

The real secret: structure beats iteration
The people getting consistent results from AI are the ones who stopped treating prompts like questions and started treating them like task specifications. They define the method before execution. They set success criteria explicitly. They structure outputs before the model generates a single word.

These five patterns give you something different, repeatable systems that produce predictable outputs. Build them once based on what actually works, then deploy them everywhere the pattern fits.

You can keep hoping your next prompt magically lands where you need it. Or you can design prompts that work the first time.

Until next time,
Lea