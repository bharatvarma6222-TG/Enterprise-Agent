from pydantic import BaseModel
from langgraph.graph import StateGraph
from langgraph.graph import END
from app.core.llm import llm
from app.tools.tavily_tool import search_web
from typing import TypedDict


class AgentState(TypedDict):
    query: str
    web_results: str
    answer: str


def search_node(state: AgentState):

    results = search_web(
        state["query"]
    )

    state["web_results"] = str(results)

    return state


def answer_node(state: AgentState):

    prompt = f"""
    You are an AI research assistant.

    Answer ONLY using the search results.

    User Question:
    {state['query']}

    Search Results:
    {state['web_results']}
    """

    response = llm.invoke(prompt)

    state["answer"] = response.content

    return state


workflow = StateGraph(AgentState)

workflow.add_node(
    "search",
    search_node
)

workflow.add_node(
    "answer",
    answer_node
)

workflow.set_entry_point("search")

workflow.add_edge(
    "search",
    "answer"
)

workflow.add_edge(
    "answer",
    END
)

graph = workflow.compile()


class ChatRequest(BaseModel):
    query: str
