from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage
import operator
from app.agents.research_agent import research_agent
from app.agents.financial_agent import financial_agent
from app.agents.summary_agent import summary_agent
from app.core.langfuse_config import get_langfuse

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    query: str
    agent_used: str
    context: str

def route_query(state: AgentState) -> str:
    """Route the query to the appropriate agent based on keywords"""
    langfuse = get_langfuse()
    query = state["query"].lower()
    
    # Track routing decision
    if langfuse:
        trace = langfuse.trace(
            name="query_routing",
            input={"query": query}
        )
    
    agent = "research"
    
    if any(word in query for word in ["calculate", "compute", "ratio", "margin", "percentage", "growth rate"]):
        agent = "financial"
    elif any(word in query for word in ["summarize", "summary", "overview", "key points"]):
        agent = "summary"
    
    if langfuse:
        trace.update(output={"selected_agent": agent})
    
    return agent

def call_research_agent(state: AgentState) -> AgentState:
    langfuse = get_langfuse()
    
    if langfuse:
        span = langfuse.span(
            name="research_agent_execution",
            input={"query": state["query"], "context": state.get("context", "")}
        )
    
    result = research_agent(state["query"], state.get("context", ""))
    state["agent_used"] = "research"
    
    if langfuse:
        span.end(output={"response": result})
    
    return state

def call_financial_agent(state: AgentState) -> AgentState:
    langfuse = get_langfuse()
    
    if langfuse:
        span = langfuse.span(
            name="financial_agent_execution",
            input={"query": state["query"], "context": state.get("context", "")}
        )
    
    result = financial_agent(state["query"], state.get("context", ""))
    state["agent_used"] = "financial"
    
    if langfuse:
        span.end(output={"response": result})
    
    return state

def call_summary_agent(state: AgentState) -> AgentState:
    langfuse = get_langfuse()
    
    if langfuse:
        span = langfuse.span(
            name="summary_agent_execution",
            input={"query": state["query"], "context": state.get("context", "")}
        )
    
    result = summary_agent(state["query"], state.get("context", ""))
    state["agent_used"] = "summary"
    
    if langfuse:
        span.end(output={"response": result})
    
    return state

# Build the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("research", call_research_agent)
workflow.add_node("financial", call_financial_agent)
workflow.add_node("summary", call_summary_agent)

# Add conditional routing from START
workflow.set_conditional_entry_point(
    route_query,
    {
        "research": "research",
        "financial": "financial",
        "summary": "summary"
    }
)

# All agents end after execution
workflow.add_edge("research", END)
workflow.add_edge("financial", END)
workflow.add_edge("summary", END)

# Compile the graph
agent_graph = workflow.compile()
