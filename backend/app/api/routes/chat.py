from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.agents.orchestrator import OrchestratorAgent
from app.core.langfuse_config import get_langfuse

router = APIRouter(prefix="/chat", tags=["chat"])
orchestrator = OrchestratorAgent()

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    session_id: str
    sources: List[str]

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        langfuse = get_langfuse()
        
        # Create main trace for the entire chat interaction
        trace = None
        if langfuse:
            trace = langfuse.trace(
                name="chat_interaction",
                input={"message": request.message, "session_id": request.session_id},
                metadata={"session_id": request.session_id}
            )
            print(f"✅ Langfuse trace created")
        else:
            print("⚠️ Langfuse not initialized")
        
        # Process through orchestrator
        result = orchestrator.process(request.message)
        
        agent_used = result.get("agent_used", "unknown")
        response_text = result.get("response", "I couldn't process your request.")
        
        response = ChatResponse(
            response=response_text,
            session_id=request.session_id,
            sources=[f"Agent used: {agent_used}"]
        )
        
        if langfuse and trace:
            trace.update(
                output={
                    "response": response_text,
                    "agent_used": agent_used
                },
                metadata={
                    "agent": agent_used,
                    "session_id": request.session_id
                }
            )
            print(f"✅ Langfuse trace updated with agent: {agent_used}")
        
        return response
        
    except Exception as e:
        if langfuse and trace:
            trace.update(
                output={"error": str(e)},
                level="ERROR"
            )
        print(f"❌ Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    return {"status": "ok"}
