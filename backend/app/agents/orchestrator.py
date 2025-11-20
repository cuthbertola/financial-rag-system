from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.core.config import get_settings
from app.agents.research_agent import ResearchAgent
from app.agents.financial_agent import FinancialAgent
from app.agents.summary_agent import SummaryAgent

settings = get_settings()

class AgentState(TypedDict):
    """State passed between agents in the graph."""
    question: str
    agent_type: str
    response: str
    context: str

class OrchestratorAgent:
    """Orchestrator that routes queries to specialized agents using LangGraph."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Initialize specialized agents
        self.research_agent = ResearchAgent()
        self.financial_agent = FinancialAgent()
        self.summary_agent = SummaryAgent()
        
        # Create routing prompt
        self.router_prompt = ChatPromptTemplate.from_template("""
Analyze the following question and determine which agent should handle it.

Question: {question}

Available agents:
1. research - For factual questions, data retrieval, and information lookup
2. financial - For calculations, financial ratios, metrics, and numerical analysis
3. summary - For summarization, executive briefs, and condensing information

Respond with ONLY the agent name (research, financial, or summary).

Agent:""")
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _route_question(self, state: AgentState) -> AgentState:
        """Determine which agent should handle the question."""
        response = self.llm.invoke(
            self.router_prompt.format(question=state["question"])
        )
        agent_type = response.content.strip().lower()
        
        # Validate agent type
        if agent_type not in ["research", "financial", "summary"]:
            agent_type = "research"  # Default fallback
        
        state["agent_type"] = agent_type
        return state
    
    def _call_agent(self, state: AgentState) -> AgentState:
        """Call the appropriate specialized agent."""
        question = state["question"]
        agent_type = state["agent_type"]
        
        if agent_type == "financial":
            response = self.financial_agent.analyze(question)
        elif agent_type == "summary":
            response = self.summary_agent.summarize(question)
        else:  # research
            response = self.research_agent.ask(question)
        
        state["response"] = response
        return state
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("router", self._route_question)
        workflow.add_node("agent", self._call_agent)
        
        # Add edges
        workflow.set_entry_point("router")
        workflow.add_edge("router", "agent")
        workflow.add_edge("agent", END)
        
        return workflow.compile()
    
    def process(self, question: str) -> dict:
        """Process a question through the multi-agent system."""
        initial_state = {
            "question": question,
            "agent_type": "",
            "response": "",
            "context": ""
        }
        
        result = self.graph.invoke(initial_state)
        
        return {
            "question": result["question"],
            "agent_used": result["agent_type"],
            "response": result["response"]
        }
