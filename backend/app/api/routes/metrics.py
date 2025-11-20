from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.database import get_db, Document
from datetime import datetime, timedelta
import random

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("/summary")
async def get_metrics_summary(db: Session = Depends(get_db)):
    """Get system metrics summary."""
    
    # Get document stats
    total_documents = db.query(func.count(Document.id)).scalar() or 0
    total_chunks = db.query(func.sum(Document.num_chunks)).scalar() or 0
    
    # Simulated metrics (in production, these would come from Langfuse API or database)
    # For demo purposes, we're showing what the dashboard would look like
    metrics = {
        "total_queries": random.randint(50, 150),
        "avg_response_time": round(random.uniform(1.5, 3.5), 2),
        "total_cost": round(random.uniform(0.50, 2.00), 4),
        "success_rate": round(random.uniform(92, 98), 1),
        "cost_per_query": round(random.uniform(0.01, 0.05), 4),
        "fastest_query": round(random.uniform(0.8, 1.5), 2),
        "slowest_query": round(random.uniform(4.0, 6.0), 2),
        "total_documents": total_documents,
        "total_chunks": total_chunks,
        "total_input_tokens": random.randint(50000, 150000),
        "total_output_tokens": random.randint(20000, 80000),
        "agent_usage": {
            "research": random.randint(30, 60),
            "financial": random.randint(20, 40),
            "summary": random.randint(15, 35)
        },
        "agent_percentages": {}
    }
    
    # Calculate agent percentages
    total_agent_queries = sum(metrics["agent_usage"].values())
    if total_agent_queries > 0:
        metrics["agent_percentages"] = {
            agent: (count / total_agent_queries) * 100
            for agent, count in metrics["agent_usage"].items()
        }
    
    return metrics
