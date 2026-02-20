from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any
import time
import os
from . import schemas, lifecycle
from uuid import UUID

app = FastAPI(title="GhostOS Kernel")


# In-memory database for agents
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
        "identity": "Cells"
    }

@app.post("/agents/", response_model=schemas.Agent)
def create_agent(agent: schemas.Agent):
    """
    Create a new agent instance.
    """
    db.append(agent)
    return agent

@app.get("/agents/", response_model=List[schemas.Agent])
def list_agents():
    """
    List all running agent instances.
    """
    return db

@app.get("/agents/{agent_id}", response_model=schemas.Agent)
def get_agent(agent_id: UUID):
    """
    Get a specific agent by its ID.
    """
    for agent in db:
        if agent.id == agent_id:
            return agent
    raise HTTPException(status_code=404, detail="Agent not found")

@app.post("/agents/{agent_id}/start", response_model=schemas.Agent)
async def start_agent_endpoint(agent_id: UUID, background_tasks: BackgroundTasks):
    """
    Start a specific agent.
    """
    agent = get_agent(agent_id) # Re-use existing get_agent logic
    if agent.state.status == "RUNNING":
        raise HTTPException(status_code=400, detail="Agent is already running.")
    
    background_tasks.add_task(lifecycle.start_agent, agent)
    return agent

@app.post("/agents/{agent_id}/stop", response_model=schemas.Agent)
async def stop_agent_endpoint(agent_id: UUID, background_tasks: BackgroundTasks):
    """
    Stop a specific agent.
    """
    agent = get_agent(agent_id)
    if agent.state.status != "RUNNING":
        raise HTTPException(status_code=400, detail="Agent is not running.")
        
    background_tasks.add_task(lifecycle.stop_agent, agent)
    return agent

@app.delete("/agents/{agent_id}", status_code=204)
def terminate_agent(agent_id: UUID):
    """
    Terminate an agent.
    """
    agent_to_terminate = None
    for agent in db:
        if agent.id == agent_id:
            agent_to_terminate = agent
            break
    if not agent_to_terminate:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    db.remove(agent_to_terminate)
    return {}

@app.post("/directives")
def queue_directive(directive: SystemDirective):
    directives_log.append(directive.dict())
    return {"status": "accepted", "id": directive.id}

@app.get("/directives")
def list_directives():
    return directives_log

@app.get("/state")
def get_system_state():
    return {
        "uptime": time.time(),
        "active_projects": ["EchoVault", "FlowSync", "Aetheria", "GhostOS"],
        "resource_usage": "nominal",
        "quota_warning": True # Vercel limit hit
    }
