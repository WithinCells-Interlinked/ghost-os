from . import schemas, process_manager
import asyncio
from uuid import UUID

async def start_agent(agent: schemas.Agent):
    """
    Starts an agent process using the process manager.
    """

    print(f"Starting agent {agent.name} ({agent.id}) via Process Manager...")
    result = process_manager.start_process(agent)
    if result.get("error"):
        agent.state.status = "FAILED"
        print(f"Agent {agent.name} failed to start. Error: {result['error']}")
    else:
        agent.state.status = "RUNNING"
        agent.state.last_heartbeat = asyncio.get_event_loop().time()
        print(f"Agent {agent.name} is now RUNNING.")
    return agent

async def stop_agent(agent: schemas.Agent):
    """
    Stops an agent process using the process manager.
    """
    print(f"Stopping agent {agent.name} ({agent.id}) via Process Manager...")
    process_manager.stop_process(str(agent.id))
    agent.state.status = "COMPLETED"
    print(f"Agent {agent.name} has been stopped.")
    return agent

async def monitor_agents(db: list[schemas.Agent]):
    """
    Placeholder for a monitoring loop that checks agent health.
    """
    while True:
        print("Monitoring agents...")
        for agent in db:
            if agent.state.status == "RUNNING":
                # Check heartbeat, resource usage, etc.
                pass
        await asyncio.sleep(60) # Check every minute
