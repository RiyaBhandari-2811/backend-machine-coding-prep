# AI Engineering — agents, RAG, LLM optimization & MLOps

Companion to [backend_machine_coding_roadmap_readme.md](backend_machine_coding_roadmap_readme.md). Section 13 of the roadmap covers *GenAI basics* (call an LLM, stream, high-level RAG). **This file is the depth** — the stuff the NetApp-style AI/ML Engineer JD actually tests: building agents, production RAG, LLM cost optimization, and MLOps.

> **Your gap honesty:** you have real **integration** experience (Claude AI Playground, MCP, LangChain/LangGraph, RAG in Niyam AI). The gaps to close here are **agent design depth, advanced RAG, cost optimization, and MLOps/eval**. Build one small thing per section — hands-on beats reading.

Default stack: **Python + FastAPI**, LangChain/LangGraph, a vector DB (Chroma/pgvector/FAISS), and **Streamlit/Gradio** for fast demos.

---

## 1. LLM fundamentals you must be able to explain

| Term | 10-second answer |
|---|---|
| **Token** | Sub-word unit; billing + context limits are measured in tokens (~4 chars ≈ 1 token) |
| **Context window** | Max tokens (input + output) a model can handle in one call |
| **Temperature** | Randomness. 0 = deterministic, higher = creative |
| **System vs user prompt** | System sets role/rules; user is the request |
| **Structured output** | Force JSON (schema / tool-calling / `response_format`) so code can parse it |
| **Embedding** | Vector representation of text; similar meaning → close vectors |

**Interview trap:** context window ≠ memory. The model is stateless; *you* resend history each call. That's why long chats get expensive (you pay for the whole history every turn).

---

## 2. AI Agents (NetApp: "agents that reason, plan, use tools, execute multi-step tasks")

An **agent** = an LLM in a loop that can call **tools** and decide the next step until the task is done.

**The core agent loop (know this cold):**
```
1. Give the LLM: the goal + available tools (name, description, args schema)
2. LLM responds with either: a tool call  OR  a final answer
3. If tool call → you execute the tool → feed the result back
4. Repeat until the LLM returns a final answer (or you hit a step limit)
```

**ReAct pattern** = Reason + Act: the model alternates "Thought → Action → Observation" until done. This is the mental model behind most agent frameworks.

**Key design decisions:**
- **Tool design** — clear name, description, and typed args (this is 80% of whether an agent works). Bad tool descriptions = agent picks wrong tool.
- **Step/loop limit** — always cap iterations to avoid infinite loops and runaway cost.
- **Planning** — for multi-step tasks, have the model produce a plan first, then execute steps (plan-and-execute vs pure ReAct).
- **State/memory** — short-term (conversation) vs long-term (vector store of past facts).
- **Multi-agent** — orchestrator + specialist agents (LangGraph models this as a graph of nodes).

**Build it:** a FastAPI endpoint with a 2-tool agent (e.g. `search_docs`, `calculator`) using LangGraph, capped at 5 steps, returning the final answer + the trace of tool calls. **Tie to your Niyam AI** (sequential agent workflow, Google ADK) in interviews.

**MCP (you've done this):** Model Context Protocol = a standard way to expose tools/data to an LLM/agent over a server, so the same tools work across clients. You secured MCP adapters at Roche — strong talking point.

---

## 3. RAG — from basic to advanced (NetApp: "hybrid search, re-ranking, agentic retrieval")

**Basic RAG flow:**
```
Ingest:  documents → chunk → embed → store in vector DB
Query:   user question → embed → similarity search → top-k chunks
Answer:  stuff chunks + question into prompt → LLM answers with citations
```

**Chunking (matters more than people think):**
- Fixed-size with **overlap** (e.g. 500 tokens, 50 overlap) so context isn't cut mid-idea.
- Or semantic/structural chunking (by heading/paragraph).
- Store **metadata** (source, title, page) so you can cite and filter.

**Advanced RAG (the differentiators NetApp names):**
| Technique | What / why |
|---|---|
| **Hybrid search** | Combine **keyword (BM25)** + **vector** search, then merge — catches exact terms vectors miss (IDs, error codes) |
| **Re-ranking** | Retrieve top-50 cheaply, then a cross-encoder re-ranks to the best top-5 before sending to the LLM |
| **Query rewriting** | LLM rephrases/expands the query before retrieval (fixes vague questions) |
| **Agentic retrieval** | An agent decides *what* and *how many times* to retrieve (multi-hop questions) |
| **Dynamic KB** | Keep the index fresh — incremental re-embed on new/changed docs |

**Evaluation (don't skip):** measure **retrieval** (did we fetch the right chunks? recall/precision) separately from **generation** (is the answer grounded/faithful? faithfulness, answer-relevance). Tools: RAGAS, or LLM-as-judge.

**Build it:** FastAPI `/ask` over ~20 docs in pgvector: chunk+embed on ingest, hybrid search + a re-rank step, answer with source citations. This single project demonstrates 70% of the JD.

---

## 4. LLM optimization & cost (NetApp + your interview Q)

You *will* be asked this. The levers:

| Lever | How |
|---|---|
| **Model selection** | Use the smallest model that's good enough (GPT-4o-mini / Haiku for routing/simple tasks, big models only when needed). *You already did this with GPT-4o mini in RiyaBot.* |
| **Prompt/context size** | Shorter prompts, trim history, summarize old turns, RAG instead of stuffing whole docs |
| **Output tokens** | Cap `max_tokens`; ask for concise/structured output |
| **Caching** | **Prompt caching** (reuse a cached system prompt/context) + **response caching** (Redis: same question → cached answer) |
| **Routing** | Cheap model classifies, routes hard cases to the expensive model |
| **Batching** | Batch embeddings/requests where latency allows |
| **Streaming** | Doesn't cut cost but improves perceived latency (time-to-first-token) |

**Cost math to say out loud:** cost ≈ (input tokens + output tokens) × price-per-token, **every call**. Long chat histories dominate cost → summarize or window them.

**Your honest line:** "I apply practical levers — smaller models, RAG to shrink context, and Redis caching — and I'm going deeper on formal optimization (prompt caching, routing, token budgeting)."

---

## 5. MLOps / LLMOps (NetApp: "training, evaluation, deployment, monitoring")

You're not expected to train foundation models, but know the lifecycle:

- **Eval** — build an eval set (golden Q→A pairs); run **offline evals** on every prompt/model change (regression testing for prompts). **LLM-as-judge** scores quality at scale.
- **Prompt versioning** — treat prompts like code: version them, A/B test, roll back. (Tools: Langfuse, PromptLayer.)
- **Observability** — trace every LLM call: inputs, outputs, tokens, latency, cost, tool calls. **Langfuse** (you've seen it at Roche) does this.
- **Monitoring in prod** — track latency, cost/request, error rate, and **quality drift**; alert on spikes.
- **Fine-tuning (awareness)** — when prompting/RAG isn't enough: collect labeled data → fine-tune a smaller model for a narrow task. You do **prompting + RAG**, not fine-tuning — say so honestly.
- **Guardrails** — input/output validation, PII redaction, prompt-injection defense, refusal handling.

**Build it:** add Langfuse (or just structured logging) to your RAG app so every call logs tokens/latency/cost; write 5 golden eval cases and a tiny script that scores answers.

---

## 6. Streamlit / Gradio (NetApp: "turn ideas into working demos quickly")

Fast way to put a UI on a Python AI service without React. Worth 30 minutes so you can say you've used them.

- **Gradio** — fastest for ML demos: `gr.ChatInterface(fn)` gives a chat UI in ~5 lines. Great for model/agent demos.
- **Streamlit** — fastest for data apps/dashboards: `st.chat_input`, `st.write`, charts. Great for RAG demos with source display.

**Build it:** wrap your RAG `/ask` function in a Gradio `ChatInterface` — instant demo. (For production/user-facing, you'd use React + FastAPI; Streamlit/Gradio are for POCs, which is exactly what NetApp's incubation team wants.)

---

## 7. Serving AI in production (fault-tolerant, low-latency)

- **Streaming** responses (SSE / `StreamingResponse` in FastAPI) for time-to-first-token.
- **Timeouts + retries with backoff** on provider calls; **fallback model** if primary fails.
- **Rate limiting** and queueing for burst traffic.
- **Async** FastAPI endpoints so one slow LLM call doesn't block the worker.
- **Caching** (section 4) for repeat queries.
- **Idempotency** for retried generation requests.

---

## 8. What to actually build this week (priority order)

1. **RAG API with citations** (FastAPI + pgvector/Chroma) — covers chunking, embeddings, retrieval, grounded answers. *Highest ROI.*
2. **A 2-tool agent** (LangGraph, step-capped) returning answer + tool trace.
3. Add **hybrid search + re-ranking** to #1.
4. Add **Redis response caching + token/latency logging** to #1 (cost story).
5. Wrap #1 in **Gradio** for a demo.
6. Write **5 golden eval cases** + an LLM-as-judge scoring script.

If you build 1–4, you can speak credibly to 80% of the NetApp JD and have real artifacts to show.

---

## 9. Honest gap-map for the NetApp JD

| JD asks | You have | To build |
|---|---|---|
| AI agents (reason/plan/tools) | Niyam AI sequential agents, MCP | the step-capped tool agent (§2) |
| LLM optimization & cost | smaller models, caching | prompt caching, routing, token budgeting (§4) |
| Advanced RAG | basic RAG (Niyam), ChromaDB exposure | hybrid search + re-ranking + eval (§3) |
| Fine-tuning foundation models | ❌ (prompting/RAG only) | awareness only — be honest |
| MLOps pipelines | Langfuse exposure | eval set + monitoring (§5) |
| React AI front ends | ✅ strong | agent/chat/eval UIs (see frontend TESTING + Tier 5) |
| Python APIs to agents/retrieval | ✅ FastAPI | the RAG/agent endpoints above |
| Streamlit/Gradio | ❌ | 30-min Gradio demo (§6) |
| Docker/K8s/CI/observability | Docker/CI ✅, K8s light | roadmap §11 |
| Multi-modal / edge / distributed training | ❌ | nice-to-have, skip for now |

Be honest about the ❌ rows in interviews — "growing into it" beats faking it.
