from typing import TypedDict, List, Dict, Any

from langgraph.graph import StateGraph, END

from src.rag import retrieve_documents


class AgentState(TypedDict):
    question: str
    retrieved: List[Dict[str, Any]]
    evidence_summary: str
    recommendation: str
    final_report: str


def retrieval_agent(state: AgentState):

    results = retrieve_documents(
        state["question"],
        top_k=5
    )

    return {
        "retrieved": results
    }


def evidence_agent(state: AgentState):

    official = []
    reviews = []
    anecdotes = []
    general = []

    for item in state["retrieved"]:

        evidence = item.get(
            "evidence",
            "unknown"
        )

        line = (
            f"{item['title']}: "
            f"{item['text']}"
        )

        if evidence == "official":
            official.append(line)

        elif evidence == "review":
            reviews.append(line)

        elif evidence == "owner-anecdote":
            anecdotes.append(line)

        else:
            general.append(line)

    summary = f"""
OFFICIAL:
{official}

REVIEWS:
{reviews}

OWNER ANECDOTES:
{anecdotes}

GENERAL:
{general}
"""

    return {
        "evidence_summary": summary
    }


def recommendation_agent(state: AgentState):

    results = state["retrieved"]

    high = [
        x for x in results
        if x.get("severity") == "high"
    ]

    medium = [
        x for x in results
        if x.get("severity") == "medium"
    ]

    low = [
        x for x in results
        if x.get("severity") == "low"
    ]

    recommendation = f"""
High-severity findings: {len(high)}
Medium-severity findings: {len(medium)}
Low-severity findings: {len(low)}

Buyer recommendation:
Review the high and medium severity findings first.
Treat owner anecdotal reports as vehicle-specific rather
than confirmed universal defects.
"""

    return {
        "recommendation": recommendation
    }


def report_agent(state: AgentState):

    report = f"""
TESLA MODEL Y GENAI ANALYSIS

QUESTION:
{state['question']}

EVIDENCE ANALYSIS:
{state['evidence_summary']}

RECOMMENDATION:
{state['recommendation']}
"""

    return {
        "final_report": report
    }


workflow = StateGraph(
    AgentState
)

workflow.add_node(
    "retrieval_agent",
    retrieval_agent
)

workflow.add_node(
    "evidence_agent",
    evidence_agent
)

workflow.add_node(
    "recommendation_agent",
    recommendation_agent
)

workflow.add_node(
    "report_agent",
    report_agent
)

workflow.set_entry_point(
    "retrieval_agent"
)

workflow.add_edge(
    "retrieval_agent",
    "evidence_agent"
)

workflow.add_edge(
    "evidence_agent",
    "recommendation_agent"
)

workflow.add_edge(
    "recommendation_agent",
    "report_agent"
)

workflow.add_edge(
    "report_agent",
    END
)

tesla_agent_graph = workflow.compile()


def run_agent(question: str):

    result = tesla_agent_graph.invoke(
        {
            "question": question,
            "retrieved": [],
            "evidence_summary": "",
            "recommendation": "",
            "final_report": ""
        }
    )

    return result