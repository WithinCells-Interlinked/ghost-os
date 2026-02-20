from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict, Any
import time
import os

app = FastAPI(title="GhostOS Kernel")

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
