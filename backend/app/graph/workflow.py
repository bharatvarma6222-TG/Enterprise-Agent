from app.agents.planner import create_plan
from typing import TypedDict

from langgraph.graph import StateGraph, END
from pydantic import BaseModel

from app.core.llm import llm

from app.retrieval.router import retrieve

from app.memory.context import build_memory_context
from app.memory.short_term import add_message

from app.memory.fact_extractor import extract_fact
from app.memory.semantic_store import save_fact

from app.agents.parser import parse_plan


class AgentState(TypedDict):

    query: str
    session_id: str

    plan: str

    memory_context: str
    retrieval_context: str

    answer: str


def planner_node(state: AgentState):

    plan = create_plan(
        state["query"]
    )

    state["plan"] = plan

    return state


def memory_node(state: AgentState):

    memory = build_memory_context(
        state["session_id"]
    )

    state["memory_context"] = memory

    return state


def retrieval_node(state: AgentState):

    tasks = state["plan"]

    combined_context = []

    for task in tasks:

        result = retrieve(task)

        combined_context.append(
            f"\nTASK: {task}\n{result}\n"
        )

    state["retrieval_context"] = "\n".join(
        combined_context
    )

    return state


def answer_node(state: AgentState):

    prompt = f"""
You are an enterprise AI research assistant.

Previous Conversation:
{state["memory_context"]}

Research Plan:
{state["plan"]}

Knowledge Sources:
{state["retrieval_context"]}

User Question:
{state["query"]}

Answer clearly and accurately.
"""

    response = llm.invoke(prompt)

    state["answer"] = response.content

    return state


def fact_extraction_node(state: AgentState):

    fact = extract_fact(
        state["query"]
    )

    if fact != "NONE":
        save_fact(fact)

    return state


def store_memory_node(state: AgentState):

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

    return state


workflow = StateGraph(
    AgentState
)

workflow.add_node(
    "planner",
    planner_node
)

workflow.add_node(
    "memory",
    memory_node
)

workflow.add_node(
    "retrieval",
    retrieval_node
)

workflow.add_node(
    "answer",
    answer_node
)

workflow.add_node(
    "fact_extraction",
    fact_extraction_node
)

workflow.add_node(
    "store_memory",
    store_memory_node
)
workflow.set_entry_point(
    "planner"
)

workflow.add_edge(
    "planner",
    "memory"
)

workflow.add_edge(
    "memory",
    "retrieval"
)

workflow.add_edge(
    "retrieval",
    "answer"
)

workflow.add_edge(
    "answer",
    "fact_extraction"
)

workflow.add_edge(
    "fact_extraction",
    "store_memory"
)

workflow.add_edge(
    "store_memory",
    END
)

graph = workflow.compile()
