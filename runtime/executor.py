from typing import Dict, Any
import time

class AgentExecutor:
    def __init__(self, state_manager, dry_run=False):
        self.state_manager = state_manager
        self.dry_run = dry_run

    def execute(self, agent_id: str, input_data: Dict[str, Any], agent_info: Dict[str, Any]) -> Dict[str, Any]:
        print(f"[{'DRY-RUN' if self.dry_run else 'EXEC'}] Agent: {agent_id}")
        self.state_manager.update_stage(agent_id)

        if self.dry_run:
            time.sleep(0.1)
            handoff = {
                "status": "SUCCESS",
                "mode": "dry-run",
                "agent": agent_id,
                "timestamp": time.time()
            }
        else:
            # Simulate real execution
            handoff = {
                "status": "SUCCESS",
                "agent": agent_id,
                "output_schema": agent_info.get("output_schema"),
                "output": f"Mock output from {agent_id}",
                "timestamp": time.time()
            }

        self.state_manager.add_artifact(f"{agent_id}_handoff", handoff)
        return handoff
