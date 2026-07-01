from app.tracing.trace_store import save_trace
import json
from app.evaluation.evaluator import evaluate_answer
from app.guardrails.pre_guard import validate_query
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from app.core.events import publish
from app.agents.tool_router import select_tool
from app.tools.calculator_tool import calculate
from app.tools.pdf_tool import pdf_search
from app.tools.memory_tool import memory_search
from app.agents.planner import create_plan
from typing import TypedDict
from app.observability.tracer import trace_start, trace_end

from langgraph.graph import StateGraph, END
from pydantic import BaseModel

from app.llm.manager import llm
import time

from app.retrieval.router import retrieve

from app.memory.context import build_memory_context
from app.memory.short_term import add_message

from app.memory.fact_extractor import extract_fact
from app.memory.semantic_store import save_fact
from typing import TypedDict, List, Dict, Any

from app.retrieval.formatter import (
    format_retrieval_context
)


def initialize_state_node(state):

    state["trace"] = []
    state.setdefault("logs", [])
    state.setdefault("citations", [])
    state.setdefault("metrics", {})

    return state


def init_node(state):

    state["logs"] = []

    state["metrics"] = {
        "start_time": time.time()
    }

    state["logs"].append(
        "Workflow Started"
    )

    return state


class ChatRequest(BaseModel):
    query: str
    session_id: str


class AgentState(TypedDict):

    query: str
    session_id: str

    route: str
    plan: list

    selected_tool: str

    memory_context: str
    retrieval_context: str

    research: str
    critique: str
    answer: str

    facts: list
    citations: list
    logs: list
    metrics: dict

    # ------------------------
    # Evaluation
    # ------------------------

    evaluation: dict

    groundedness: float

    completeness: float

    confidence: float

    hallucination_risk: str

    trace: list

    llm_metrics: list

    total_tokens: int

    prompt_tokens: int

    completion_tokens: int


def tool_router_node(state):

    trace_start(
        state,
        "tool_router"
    )

    try:

        print(">>> TOOL ROUTER NODE")

        tool = select_tool(
            state["query"]
        ).strip().lower()

        print(
            "Selected Tool =",
            repr(tool)
        )

        state["selected_tool"] = tool

        state["metrics"]["tool"] = tool

        state["logs"].append(
            f"Tool Selected: {tool}"
        )

        trace_end(state)

        return state

    except Exception as e:

        trace_end(
            state,
            status="failed",
            error=str(e)
        )

        raise


def tool_execution_node(state):

    trace_start(
        state,
        "tool_execution"
    )

    try:

        print("=" * 60)
        print(">>> TOOL EXECUTION NODE")
        print("TOOL =", repr(state["selected_tool"]))
        print("=" * 60)

        tool = state["selected_tool"]

        state["route"] = "research"

        if tool == "calculator":

            state["answer"] = str(
                calculate(state["query"])
            )

            state["route"] = "direct"

        elif tool == "memory":

            state["answer"] = str(
                memory_search(state["query"])
            )

            state["route"] = "direct"

        elif tool == "pdf":

            state["retrieval_context"] = str(
                pdf_search(
                    state["query"],
                    session_id=state.get("session_id")
                )
            )

        print("ROUTE =", state["route"])

        trace_end(state)

        return state

    except Exception as e:

        trace_end(
            state,
            status="failed",
            error=str(e)
        )

        raise


def planner_node(state):

    trace_start(
        state,
        "planner"
    )

    try:

        state["logs"].append(
            "Planner Started"
        )

        if "metrics" not in state:
            state["metrics"] = {}

        publish(
            "planner_started",
            "Planner started"
        )

        plan = create_plan(
            state["query"]
        )

        state["plan"] = plan

        state["metrics"]["task_count"] = len(plan)

        state["logs"].append(
            f"Planner Created {len(plan)} Tasks"
        )

        publish(
            "planner_finished",
            f"{len(plan)} tasks created",
            {
                "tasks": len(plan)
            }
        )

        trace_end(state)

        return state

    except Exception as e:

        trace_end(
            state,
            status="failed",
            error=str(e)
        )

        raise


def memory_node(state):

    trace_start(
        state,
        "memory"
    )

    try:

        state["logs"].append(
            "Memory Loaded"
        )

        memory = build_memory_context(
            state["session_id"]
        )

        state["memory_context"] = memory

        trace_end(state)

        return state

    except Exception as e:

        trace_end(
            state,
            status="failed",
            error=str(e)
        )

        raise


def retrieval_node(state):

    trace_start(
        state,
        "retrieval"
    )

    try:

        start = time.time()

        print("RETRIEVAL STARTED")

        publish(
            "retrieval_started",
            "Searching knowledge..."
        )

        tasks = state["plan"]

        all_docs = []
        citations = []

        # ----------------------------
        # Retrieve one task
        # ----------------------------

        def retrieve_task(task):
            return retrieve(
                task,
                state["session_id"]
            )

        # ----------------------------
        # Run all retrievals in parallel
        # ----------------------------

        with ThreadPoolExecutor(max_workers=4) as executor:

            results = list(
                executor.map(
                    retrieve_task,
                    tasks
                )
            )

        # ----------------------------
        # Merge + Remove Duplicates
        # ----------------------------

        seen = set()

        for result in results:

            for doc in result["local"]:

                key = (
                    doc.get("source"),
                    doc.get("chunk_id")
                )

                if key in seen:
                    continue

                seen.add(key)

                all_docs.append(doc)

        # ----------------------------
        # Sort by score
        # ----------------------------

        all_docs.sort(
            key=lambda x: x.get("score", 0.0),
            reverse=True
        )

        all_docs = all_docs[:10]

        # ----------------------------
        # Build citations
        # ----------------------------

        citations = []

        for doc in all_docs:

            citations.append(
                {
                    "source": doc.get("source"),
                    "chunk_id": doc.get("chunk_id")
                }
            )

        state["citations"] = citations

        print("=" * 60)
        print("AFTER RETRIEVAL")
        print(state["citations"])
        print("=" * 60)

        if not all_docs:

            state["retrieval_context"] = "[]"

        else:

            state["retrieval_context"] = format_retrieval_context(
                all_docs
            )

        publish(
            "retrieval_finished",
            f"{len(all_docs)} unique documents found",
            {
                "documents": len(all_docs)
            }
        )

        print("RETRIEVAL CONTEXT CREATED")

        print(
            "Unique Docs:",
            len(all_docs)
        )

        print(
            "Retrieval Time:",
            round(
                time.time() - start,
                2
            ),
            "seconds"
        )

        print("=" * 80)
        print(state["retrieval_context"])
        print("=" * 80)

        print("=" * 60)
        print("CITATIONS")
        print(state["citations"])
        print("=" * 60)

        trace_end(state)

        return state

    except Exception as e:

        trace_end(
            state,
            status="failed",
            error=str(e)
        )

        raise


def fact_extraction_node(state):

    trace_start(
        state,
        "fact_extraction"
    )

    try:

        state["logs"].append(
            "Fact Extraction Started"
        )

        fact = extract_fact(
            state["answer"]
        )

        if fact == "NONE":

            state["facts"] = []

        else:

            state["facts"] = [fact]

        trace_end(state)

        return state

    except Exception as e:

        trace_end(
            state,
            status="failed",
            error=str(e)
        )

        raise


def store_memory_node(state: AgentState):

    trace_start(
        state,
        "Store Memory"
    )

    try:

        state["logs"].append(
            "Memory Stored"
        )

        # ---------------------------------
        # Save conversation history
        # ---------------------------------

        add_message(
            state["session_id"],
            "user",
            state["query"]
        )

        add_message(
            state["session_id"],
            "assistant",
            state["answer"]
        )

        # ---------------------------------
        # Save extracted facts
        # ---------------------------------

        for fact in state.get("facts", []):

            if fact.strip():

                save_fact(
                    fact,
                    state.get(
                        "session_id",
                        "global"
                    )
                )

        # ---------------------------------
        # Metrics
        # ---------------------------------

        state["metrics"]["total_time"] = round(
            time.time()
            - state["metrics"]["start_time"],
            2
        )

        publish(
            "memory_saved",
            "Conversation stored"
        )

        trace_end(state)

        # ---------------------------------
        # Print execution trace
        # ---------------------------------

        print("\n")
        print("=" * 80)
        print("EXECUTION TRACE")
        print("=" * 80)

        for item in state["trace"]:

            print(
                f"{item['node']:<20}"
                f"{item['status']:<12}"
                f"{item['duration']} sec"
            )

            if item["error"]:

                print(
                    "   ERROR:",
                    item["error"]
                )

        print("=" * 80)

        trace = {

            "query": state["query"],

            "answer": state["answer"],

            "session_id": state["session_id"],

            "logs": state.get("logs", []),

            "metrics": state.get("metrics", {}),

            "evaluation": state.get("evaluation", {}),

            "citations": state.get("citations", []),

            "trace": state.get("trace", []),

        }

        save_trace(trace)

        return state

    except Exception as e:

        trace_end(
            state,
            status="failed",
            error=str(e),
        )

        raise


def researcher_node(state):

    trace_start(
        state,
        "researcher"
    )

    try:

        state["logs"].append(
            "Research Agent Started"
        )

        publish(
            "research_started",
            "Research agent thinking..."
        )

        response = llm.invoke(f"""
You are a senior research analyst.

User Question:
{state["query"]}

Retrieved Context:
{state["retrieval_context"]}

Your job:

- Answer ONLY the user's question.
- Extract only relevant facts.
- Do NOT copy large passages.
- Do NOT repeat sentences.
- Keep the research concise.
- Mention the source and chunk after each important fact.
- If the retrieved context does not contain sufficient information or is '[]', respond EXACTLY with:
'I couldn't find relevant information in the uploaded documents.'

Return bullet points only.
""")

        state["research"] = response.content

        print("RESEARCH CREATED")

        state["logs"].append(
            "Research Agent Finished"
        )

        publish(
            "research_finished",
            "Research completed"
        )

        trace_end(state)

        return state

    except Exception as e:

        trace_end(
            state,
            status="failed",
            error=str(e)
        )

        raise


def critic_node(state):

    trace_start(
        state,
        "critic"
    )

    try:

        state["logs"].append(
            "Critic Started"
        )

        publish(
            "critic_started",
            "Critic reviewing answer..."
        )

        print("CRITIC STARTED")

        prompt = f"""
You are a senior reviewer.

Review the following research.

Return ONLY:

- Missing facts
- Incorrect facts
- Weak citations
- Suggested improvements

Do NOT rewrite the report.
Do NOT repeat the research.

Research:

{state["research"]}
"""

        response = llm.invoke(prompt)

        state["critique"] = response.content

        print("CRITIQUE CREATED")

        state["logs"].append(
            "Critic Finished"
        )

        publish(
            "critic_finished",
            "Critique completed"
        )

        trace_end(state)

        return state

    except Exception as e:

        trace_end(
            state,
            status="failed",
            error=str(e)
        )

        raise


def writer_node(state):

    trace_start(
        state,
        "writer"
    )

    try:

        state["logs"].append(
            "Writer Started"
        )

        publish(
            "writer_started",
            "Generating answer..."
        )

        print("WRITER STARTED")

        prompt = f"""
You are an Enterprise AI Assistant.

You answer naturally like ChatGPT.

You have access to:

==============================
Conversation Memory
==============================
{state.get("memory_context", "")}

==============================
Retrieved Knowledge
==============================
{state.get("retrieval_context", "")}

==============================
Research
==============================
{state.get("research", "")}

==============================
Critique
==============================
{state.get("critique", "")}

==============================
User Question
==============================
{state["query"]}

--------------------------------------------------

Instructions:

1. ALWAYS answer the user's question directly.

2. If the user simply greets you,
respond naturally.

Example:

User:
Hi

Assistant:
Hello! How can I help you today?

3. If the question is general knowledge
and retrieved knowledge is empty,
answer using your own knowledge.

Example:
"What is Gmail?"

Do NOT say
"I couldn't find relevant information."

4. If retrieved knowledge exists,
use it as the PRIMARY source.

5. If retrieved knowledge conflicts with
your own knowledge,
prefer the retrieved documents.

6. If the user asks for a report,
research,
summary,
analysis,
comparison,
or detailed explanation,
produce a structured report.

7. Otherwise answer conversationally.

8. Never invent citations.

9. Never invent document names.

10. Cite uploaded documents whenever used using

[Source: filename | Chunk: id]

11. If uploaded documents do not contain the answer,
and the question is NOT document-specific,
answer from your own knowledge.

12. If the user explicitly asks something about
their uploaded files,
and nothing relevant was found,
say exactly:

I couldn't find relevant information in the uploaded documents.

Never mention missing retrieval unless the question
is specifically about uploaded documents.
"""

        answer = ""

        print("STARTING STREAM")

        for chunk in llm.stream(prompt):

            token = chunk.content or ""

            answer += token

            publish(
                "token",
                token
            )

        print("STREAM FINISHED")

        print("=" * 60)
        print("WRITER NODE")
        print(state.keys())
        print(state.get("citations"))
        print("=" * 60)

        citation_text = "\n\nSources Used:\n"

        seen = set()

        for citation in state.get("citations", []):

            source = Path(
                citation.get("source", "Unknown")
            ).name

            chunk_id = citation.get(
                "chunk_id",
                "Unknown"
            )

            key = (
                source,
                chunk_id
            )

            if key in seen:
                continue

            seen.add(key)

            citation_text += (
                f"- {source} (Chunk {chunk_id})\n"
            )

        if not seen:

            citation_text += (
                "- No uploaded document citations\n"
            )

        state["answer"] = answer + citation_text

        print("=" * 80)
        print(state["answer"])
        print("=" * 80)

        state["logs"].append(
            "Writer Finished"
        )

        publish(
            "writer_finished",
            "Answer generated",
            {
                "answer": state["answer"]
            }
        )

        trace_end(state)

        return state

    except Exception as e:

        trace_end(
            state,
            status="failed",
            error=str(e)
        )

        raise


def evaluator_node(state):

    trace_start(
        state,
        "evaluator"
    )

    try:

        state["logs"].append(
            "Evaluator Started"
        )

        publish(
            "evaluation_started",
            "Evaluating answer..."
        )

        try:

            result = evaluate_answer(
                state["query"],
                state["retrieval_context"],
                state["answer"],
            )

            data = json.loads(result)

        except Exception:

            data = {
                "groundedness": 5,
                "completeness": 5,
                "hallucination": "Unknown",
                "confidence": 50,
            }

        state["evaluation"] = data

        state["groundedness"] = data["groundedness"]
        state["completeness"] = data["completeness"]
        state["confidence"] = data["confidence"]
        state["hallucination_risk"] = data["hallucination"]

        state["logs"].append(
            "Evaluator Finished"
        )

        publish(
            "evaluation_finished",
            "Evaluation completed",
            data
        )

        trace_end(state)

        return state

    except Exception as e:

        trace_end(
            state,
            status="failed",
            error=str(e)
        )

        raise


def guardrail_node(state):

    trace_start(
        state,
        "guardrail"
    )

    try:

        state["logs"].append(
            "Guardrail Started"
        )

        publish(
            "guardrail_started",
            "Running guardrails"
        )

        ok, message = validate_query(
            state["query"]
        )

        if not ok:

            state["answer"] = message
            state["route"] = "blocked"

        else:

            state["route"] = "continue"

        publish(
            "guardrail_finished",
            "Guardrails passed"
        )

        trace_end(state)

        return state

    except Exception as e:

        trace_end(
            state,
            status="failed",
            error=str(e)
        )

        raise


def blocked_node(state):

    trace_start(
        state,
        "blocked"
    )

    try:

        print("=" * 60)
        print("BLOCKED NODE")
        print("Reason:")
        print(state.get("answer"))
        print("=" * 60)

        state["logs"].append(
            "Request Blocked"
        )

        publish(
            "guardrail_blocked",
            state.get(
                "answer",
                "Request blocked"
            )
        )

        trace_end(state)

        return state

    except Exception as e:

        trace_end(
            state,
            status="failed",
            error=str(e)
        )

        raise


workflow = StateGraph(AgentState)

# =====================================================
# ENTRY
# =====================================================

workflow.set_entry_point("initialize")

# =====================================================
# NODES
# =====================================================

workflow.add_node("initialize", initialize_state_node)
workflow.add_node("guardrail", guardrail_node)
workflow.add_node("blocked", blocked_node)
workflow.add_node("init", init_node)
workflow.add_node("planner", planner_node)
workflow.add_node("memory", memory_node)
workflow.add_node("tool_router", tool_router_node)
workflow.add_node("tool_execution", tool_execution_node)
workflow.add_node("retrieval", retrieval_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("critic", critic_node)
workflow.add_node("writer", writer_node)
workflow.add_node("evaluator", evaluator_node)
workflow.add_node("fact_extraction", fact_extraction_node)
workflow.add_node("store_memory", store_memory_node)


# =====================================================
# NORMAL EDGES
# =====================================================

workflow.add_edge("initialize", "guardrail")

# =====================================================
# GUARDRAIL ROUTING
# =====================================================


def guardrail_condition(state):

    print("=" * 60)
    print("GUARDRAIL EDGE")
    print("route =", repr(state["route"]))
    print("=" * 60)

    return state["route"]


workflow.add_conditional_edges(
    "guardrail",
    guardrail_condition,
    {
        "continue": "init",
        "blocked": "blocked",
    },
)
workflow.add_edge("blocked", END)

# =====================================================
# NORMAL FLOW
# =====================================================

workflow.add_edge("init", "planner")
workflow.add_edge("planner", "memory")
workflow.add_edge("memory", "tool_router")

# =====================================================
# TOOL ROUTER
# =====================================================


def tool_router_condition(state):

    print("=" * 60)
    print("TOOL ROUTER EDGE")
    print("selected_tool =", repr(state["selected_tool"]))
    print("=" * 60)

    return state["selected_tool"]


workflow.add_conditional_edges(
    "tool_router",
    tool_router_condition,
    {
        "calculator": "tool_execution",
        "memory": "tool_execution",
        "pdf": "retrieval",
        "search": "retrieval",
    },
)

# =====================================================
# TOOL EXECUTION
# =====================================================


def tool_execution_condition(state):

    print("=" * 60)
    print("TOOL EXECUTION EDGE")
    print("route =", repr(state["route"]))
    print("=" * 60)

    return state["route"]


workflow.add_conditional_edges(
    "tool_execution",
    tool_execution_condition,
    {
        "direct": "store_memory",
        "research": "researcher",
    },
)

# =====================================================
# RETRIEVAL PIPELINE
# =====================================================

workflow.add_edge("retrieval", "researcher")
workflow.add_edge("researcher", "critic")
workflow.add_edge("critic", "writer")

# =====================================================
# MEMORY PIPELINE
# =====================================================

workflow.add_edge("writer", "evaluator")
workflow.add_edge("evaluator", "fact_extraction")
workflow.add_edge("fact_extraction", "store_memory")
workflow.add_edge("store_memory", END)

# =====================================================
# COMPILE
# =====================================================

graph = workflow.compile()
