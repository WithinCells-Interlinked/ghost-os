import subprocess
import json
from . import schemas

def _run_pm2_command(command: list[str]) -> dict:
    """Helper to run a PM2 command and parse its JSON output."""
    try:
        # PM2 commands are executed via the pm2 executable
        result = subprocess.run(['pm2'] + command, capture_output=True, text=True, check=True)
        # PM2's JSON output isn't always clean, find the start of the JSON array
        json_start = result.stdout.find('[')
        if json_start == -1:
            return {}
        return json.loads(result.stdout[json_start:])
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Error executing PM2 command: {e}")
        return {"error": str(e)}

def start_process(agent: schemas.Agent) -> dict:
    """Starts a new agent process using PM2."""
    script = agent.start_command # Assuming start_command is part of the agent model
    name = str(agent.id)
    return _run_pm2_command(['start', script, '--name', name])

def stop_process(agent_id: str) -> dict:
    """Stops an agent process using PM2."""
    return _run_pm2_command(['stop', agent_id])

def get_process_status(agent_id: str) -> dict:
    """Gets the status of an agent process from PM2."""
    processes = _run_pm2_command(['jlist'])
    if 'error' in processes:
        return processes
    for p in processes:
        if p.get('name') == agent_id:
            return p
    return {}
