from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from uuid import UUID, uuid4

class AgentResourceSpec(BaseModel):
    cpu_limit: Optional[str] = "100m"
    memory_limit: Optional[str] = "128Mi"

class AgentState(BaseModel):
    status: str = "PENDING" # PENDING, RUNNING, COMPLETED, FAILED
    last_heartbeat: Optional[datetime] = None

class Agent(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    start_command: str # The actual command to run the agent
    persona_id: str # Link to a persona definition
    tool_ids: List[str] = []
    state: AgentState = Field(default_factory=AgentState)
    resources: AgentResourceSpec = Field(default_factory=AgentResourceSpec)
    created_at: datetime = Field(default_factory=datetime.utcnow)

