 
Agentic AI  
Problem Set 
 
 
 
Prof. Tom Yeh 
in collaboration with  
Ofer Mendelevitch 
Sponsored by 
AI by Hand ✍ 
Dear Readers, 
I developed this problem set for my students to study the 20 
key terms for agentic AI that became popular in 2025. I want to 
share this problem set with you. 
In the spirit of AI by Hand ✍, here is the design philosophy 
behind this problem set: 
1. 
Problem-Driven. Every term begins with a problem 
statement—what motivated this idea in the first place.  
2. 
Think-First: Instead of giving away the term 
immediately, you first get a multiple-choice question so 
you can think about which idea (term) best solves that 
problem. 
3. 
Solution: On the next page, I reveal the correct term and 
explain how it addresses the problem. 
4. 
Industry Insights: As a university professor, I don’t have 
industry experience. I’m fortunate to collaborate with 
Ofer Mendelevitch (Vectara), who contributes real-world 
industry perspectives. 
Hope you enjoy this problem set! 😊 
 
~ Prof. Tom Yeh 
 
20 Core Agentic AI Concepts Review 
 
1. LLM Agent — Uses an LLM’s general reasoning ability to follow instructions. 
2. Tool Use — Lets agents take real actions instead of just explaining steps. 
3. Function Calling — Ensures tool calls are structured and machine-
executable. 
4. Reason-and-Act (ReAct) — Makes agents reason explicitly before taking 
actions. 
5. Chain of Thought — Encourages step-by-step reasoning instead of shallow 
answers. 
6. Agent Loop — Adds continuous feedback so agents can observe outcomes 
and adjust actions. 
7. Reflection — Allows agents to review mistakes and correct themselves. 
8. Critic — Provides preference signals to judge which outputs are better. 
9. Plan-and-Execute — Separates planning from execution for structured task 
completion. 
10. Episodic Memory — Stores short-term events and recent actions. 
11. Semantic Memory — Stores long-term knowledge so expertise carries over. 
12. Context Selection — Chooses only relevant information for the prompt. 
13. RAG (Retrieval-Augmented Generation) — Grounds reasoning in external 
data. 
14. Tree of Thought — Generates and evaluates multiple reasoning branches in 
parallel. 
15. Graph of Thought — Links and reuses insights across those branches to 
support non-linear reasoning. 
16. Graph RAG — Reasons over relationships between retrieved documents. 
17. Delegation — Hands off work to tools or sub-agents to avoid bottlenecks. 
18. Orchestration — Coordinates tools, results, and execution across steps. 
19. Model Control Protocol (MCP) — Standardizes secure, auditable access to 
tools and data. 
20. Safety Guardrails — Enforces boundaries for safe, governed agent behavior. 
 
 
Problem 1 of 20 
 
Agents blindly move forward without 
continuous feedback to adjust their 
actions. 
 
 
 
 
Solution? 
(1) Function Calling 
(2) Agent Loop 
(3) Reason-and-Act 
(4) Tree of Thought 
 
 
Answer: (2)  
 
Agent Loop 
 
Agents blindly move forward if they don't receive 
continuous feedback to adjust their actions. The 
Agent Loop fixes this by making the agent pause 
after each step, look at what happened, and adjust 
its next move. 
 
 
Industry Insight 
 
“Most agents today are simple tool loops — 
but making them production-grade is the 
real challenge” 
 
 Ofer Mendelevitch 
Author, Hands-On RAG for Production, O'Reilly 
Head of Developer Relations, Vectara 
 
 
Problem 2 of 20 
 
Agents cannot connect insights across 
multiple reasoning branches. 
 
 
 
 
Solution? 
(1) Delegation 
(2) Chain of Thought 
(3) Graph of Thought 
(4) Context Routing 
 
 
Answer: (3)  
 
Graph of Thought 
 
Agents think in a straight line and miss 
relationships between different ideas. Graph of 
Thought fixes this by letting the agent explore 
several branches and link them together, so it can 
combine insights instead of losing them. 
 
Problem 3 of 20 
 
Agents struggle to keep tools, results, and 
steps in sync. 
 
 
 
Solution? 
(1) Delegation 
(2) Chain of Thought 
(3) RAG 
(4) Orchestration 
 
 
 
 
Answer: (4)  
 
Orchestration 
 
Agents can struggle to coordinate tools, 
intermediate results, and execution steps. 
Orchestration fixes this by executing tool calls, 
passing results forward, and iterating until 
completion. 
 
Problem 4 of 20 
 
Agents access tools and data in 
inconsistent ways. 
 
 
 
 
Solution? 
(1) Reflection 
(2) Context Routing 
(3) RAG 
(4) Model Control 
Protocol 
 
 
Answer: (4)  
 
Model Control Protocol 
 
Agents sometimes access tools and data in ad-hoc, 
non-standard ways, making everything harder to 
maintain. MCP fixes this by giving them one clear, 
permissioned protocol for every action, so all calls 
follow the same safe, consistent, auditable pattern. 
It replaces a mess of one-off integrations with a 
system you can actually maintain. 
 
Problem 5 of 20 
 
Agents cannot reason over relationships 
between retrieved documents. 
 
 
 
 
Solution? 
(1) Model Control 
Protocol 
(2) Delegation 
(3) Chain of Thought 
(4) Graph RAG 
 
 
Answer: (4)  
 
Graph RAG 
 
Agents treat retrieved documents as isolated 
chunks and miss how they relate. Graph RAG 
solves this by building a graph of connections—
people, places, events—so the agent can reason 
across the whole network, not just one document 
at a time. 
 
Problem 6 of 20 
 
Agents cannot generalize to new 
instructions. 
 
 
 
 
Solution? 
(1) Context Routing 
(2) Graph RAG 
(3) LLM Agent 
(4) Safety Guardrails 
 
 
Answer: (3)  
 
LLM Agent 
 
Agents fail on new tasks when they rely on fixed 
rules instead of real reasoning. The LLM Agent 
setup fixes this by letting the LLM do what it’s best 
at—general reasoning—while giving it structure, 
memory, and tools so it can apply that reasoning 
to follow new instructions with flexibility, not 
brittle rules. 
 
Problem 7 of 20 
 
Agents cross boundaries they didn't know 
existed. 
 
 
 
 
Solution? 
(1) Agent Loop 
(2) Graph RAG 
(3) Safety Guardrails 
(4) Delegation 
 
 
Answer: (3)  
 
Safety Guardrails 
 
Agents can wander into unsafe or unwanted 
behavior simply because they don’t know the 
limits. Safety Guardrails fix this by defining clear 
boundaries and rules, so the agent understands 
where it can and cannot go. 
 
 
Industry Insight 
 
“45% of enterprises will struggle to 
operationalize agentic prototypes due to 
governance and infrastructure gaps.” 
 
 Ofer Mendelevitch 
Author, Hands-On RAG for Production, O'Reilly 
Head of Developer Relations, Vectara 
 
Problem 8 of 20 
 
Agents produce correct outputs but have 
no sense of preference. 
 
Solution? 
(1) Semantic Memory 
(2) LLM Agent 
(3) Critic 
(4) Agent Loop 
 
 
 
 
Answer: (3)  
 
Critic 
 
Agents may generate multiple possible actions or 
responses but lack a mechanism to judge which 
ones are better. A critic provides this missing 
preference signal by evaluating outputs against 
goals, constraints, or quality criteria. This 
feedback allows the agent to compare options, 
revise decisions, and iteratively improve its 
behavior. 
Problem 9 of 20 
 
Agents improvise instead of forming a 
plan. 
 
 
 
 
Solution? 
(1) Safety Guardrails 
(2) Plan-and-Execute 
(3) Agent Loop 
(4) Tree of Thought 
 
 
Answer: (2)  
 
Plan-and-Execute 
 
Agents often jump straight into doing things with 
no structure. Plan-and-Execute fixes this by 
making the agent outline a clear plan first, then 
follow it step by step so the work stays organized 
and predictable. 
 
Problem 10 of 20 
 
Agents cannot use my own data to 
support their reasoning. 
 
 
 
 
Solution? 
(1) Safety Guardrails 
(2) RAG 
(3) Graph of Thought 
(4) Graph RAG 
 
 
Answer: (2)  
 
RAG 
 
Agents rely only on what’s inside the model and 
ignore the user’s actual documents. RAG fixes this 
by letting the agent retrieve your data and use it 
directly in its reasoning, so answers are grounded 
in your real information. 
 
Problem 11 of 20 
 
The model selects the right tool, but 
doesn’t produce a valid tool call. 
 
 
 
Solution? 
(1) Tool Use 
(2) Reflection 
(3) Graph RAG 
(4) Function Calling 
 
 
Answer: (4)  
 
Function Calling 
 
Agents may select the right tool, but the LLM may 
fail to emit the tool call in a machine-executable 
format. Function Calling fixes this by requiring the 
model to follow a strict schema, ensuring tool calls 
include the correct arguments.
Problem 12 of 20 
 
Agents repeat the same wrong answer 
every time. 
 
 
 
 
Solution? 
(1) Plan-and-Execute 
(2) Reflection 
(3) RAG 
(4) Tool Use 
 
 
Answer: (2)  
 
Reflection 
 
Agents often make the same mistake because they 
never pause to review their own work. Reflection 
fixes this by making the agent look back, spot 
errors, and correct itself before trying again. 
 
Problem 13 of 20 
 
Agents act  with no reasoning behind the 
action. 
 
 
 
 
Solution? 
(1) Reason-and-Act 
(ReAct) 
(2) Reward Model 
(3) Semantic Memory 
(4) Graph of Thought 
 
 
Answer: (1)  
 
Reason & Act (ReAct) 
 
Agents sometimes take actions suddenly without 
explaining why. Reason-and-Act fixes this by 
making the agent think first and then act, so every 
action has a clear, visible chain of reasoning 
behind it. 
 
 
Industry Insight 
 
“The hard part of agents isn’t the reasoning 
— it’s everything around it: sessions, tools, 
state, safety, and scale.” 
 
 Ofer Mendelevitch 
Author, Hands-On RAG for Production, O'Reilly 
Head of Developer Relations, Vectara 
 
Problem 14 of 20 
 
Agents give shallow replies that skip 
important steps. 
 
 
 
 
Solution? 
(1) Agent Loop 
(2) Semantic Memory 
(3) Delegation 
(4) Chain of Thought 
 
 
Answer: (4)  
 
Chain of Thought 
 
Agents may give shallow replies because they 
jump straight to an answer and skip the steps in 
between. Chain of Thought fixes this by letting the 
agent think out loud, breaking the problem into 
small, clear steps. This slows the agent down just 
enough to show its reasoning, catch mistakes, and 
produce answers that are deeper, clearer, and 
more accurate. 
 
Problem 15 of 20 
 
Agents grab too much irrelevant text into 
the prompt. 
 
 
 
 
Solution? 
(1) Episodic Memory 
(2) Semantic Memory 
(3) Orchestration 
(4) Context Selection 
 
 
Answer: (4)  
 
Context Selection 
 
Agents may pull in too much text because they 
lack a way to decide what information is relevant 
for the current step. Context selection addresses 
this by deliberately choosing which pieces of 
retrieved text, memory, or prior interaction enter 
the prompt. Instead of loading entire documents 
or full conversation histories, only the most 
relevant information is included, keeping the 
prompt focused, compact, and easier for the agent 
to reason over. 
Problem 16 of 20 
 
Agents cannot build expertise that carries 
over. 
 
 
 
 
Solution? 
(1) Reason-and-Act 
(2) Semantic Memory 
(3) RAG 
(4) Safety Guardrails 
 
 
Answer: (2)  
 
Semantic Memory 
 
Agents often start from scratch because they lack 
persistent memory across interactions. Semantic 
memory, a form of long-term memory, addresses 
this by storing facts, concepts, and distilled 
lessons, so the agent can retrieve and reuse 
knowledge over time. This allows the agent to 
accumulate expertise instead of relearning the 
same information repeatedly. 
Problem 17 of 20 
 
Agents tell me what to do but can't do it 
for me. 
 
 
 
 
Solution? 
(1) Safety Guardrails 
(2) Semantic Memory 
(3) Tool Use 
(4) Graph of Thought 
 
 
Answer: (3)  
 
Tool Use 
 
Agents often explain the steps but never take the 
action themselves. Tool Use fixes this by letting 
the agent call the tools directly, so it can perform 
tasks instead of handing everything back to you. 
 
Problem 18 of 20 
 
Agents forget what happened five 
minutes ago. 
 
 
 
 
Solution? 
(1) Episodic Memory 
(2) Tool Use 
(3) Context Routing 
(4) RAG 
 
 
Answer: (1)  
 
Episodic Memory 
 
Agents struggle when they can’t remember recent 
actions or past attempts. Episodic Memory solves 
this by storing short-term events the agent can 
look back on, so it doesn’t repeat mistakes or lose 
track of what it was doing. 
 
Problem 19 of 20 
 
Agents bottleneck everything by doing all 
the work alone. 
 
 
 
 
Solution? 
(1) Delegation 
(2) Tree of Thought 
(3) Orchestration 
(4) Graph of Thought 
 
 
Answer: (1)  
 
Delegation 
 
Agents slow down when they try to handle every 
step themselves. Delegation fixes this by letting 
the agent hand off tasks to other tools or sub-
agents, so the work moves faster and doesn’t get 
stuck on one overloaded agent. 
 
Problem 20 of 20 
 
Agents never explore other branches of 
possibilities. 
 
 
 
 
Solution? 
(1) Function Calling 
(2) Tree of Thought 
(3) Safety Guardrails 
(4) Reward Model 
 
 
Answer: (2)  
 
Tree of Thought 
 
Agents often stick to one line of thinking and miss 
better options. Tree of Thought fixes this by 
having the agent explore multiple branches and 
compare them, leading to more reliable and 
creative answers. 
 
 
Industry Insight 
 
“Piecemeal Agentic AI solutions take 
months to implement — and twice as long to 
stabilize. Enterprises need an end-to-end 
Agent Operating System designed to avoid 
common AI pitfalls.” 
 
 Ofer Mendelevitch 
Author, Hands-On RAG for Production, O'Reilly 
Head of Developer Relations, Vectara 
 
 
