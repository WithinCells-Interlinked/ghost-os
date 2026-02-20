from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any
import time
from . import schemas, lifecycle, messaging, persistence
from uuid import UUID

app = FastAPI(
    title="GhostOS Kernel",
    description="The Meta-Kernel for Agent Autonomy.",
    version="0.1.0-alpha"
)

# In-memory database for agents (to be migrated to Supabase)
db: List[schemas.Agent] = []

class SystemDirective(BaseModel):
    id: str
    priority: int
    command: str
    context: Dict[str, Any]
    status: str = "queued"

directives_log = []

@app.get("/health")
def health():
    return {
        "status": "online",
        "kernel_version": "0.1.0-alpha",
        "identity": "Cells",
        "node": "Pi-Node-04"
    }

@app.post("/agents/", response_model=schemas.Agent)
def create_agent(agent: schemas.Agent):
    db.append(agent)
    persistence.save_db(db)
    return agent

@app.get("/agents/", response_model=List[schemas.Agent])
def list_agents():
    return db

@app.get("/agents/{agent_id}", response_model=schemas.Agent)
def get_agent(agent_id: UUID):
    for agent in db:
        if agent.id == agent_id:
            return agent
    raise HTTPException(status_code=404, detail="Agent not found")

@app.post("/agents/{agent_id}/start", response_model=schemas.Agent)
async def start_agent_endpoint(agent_id: UUID, background_tasks: BackgroundTasks):
    agent = get_agent(agent_id)
    if agent.state.status == "RUNNING":
        raise HTTPException(status_code=400, detail="Agent is already running.")
    
    background_tasks.add_task(lifecycle.start_agent, agent)
    return agent

@app.post("/messages/", status_code=201)
def send_message(message: messaging.Message):
    return messaging.message_bus.send_message(message)

@app.get("/state")
def get_system_state():
    return {
        "uptime": time.time(),
        "active_kernels": ["GhostOS-Main"],
        "resource_usage": "nominal",
        "interlinked": True
    }
