from typing import Dict, Any
import time

class AgentExecutor:
    def __init__(self, state_manager, dry_run=False):
        self.state_manager = state_manager
        self.dry_run = dry_run

    def execute(self, agent_id: str, input_data: Dict[str, Any], agent_info: Dict[str, Any]) -> Dict[str, Any]:
        print(f"[{'DRY-RUN' if self.dry_run else 'EXEC'}] Agent: {agent_id}")

        next_agent = agent_info.get("next")[0] if agent_info.get("next") else None
        self.state_manager.transition_to(agent_id, next_agent)

        if self.dry_run:
            time.sleep(0.1)
            handoff = {"status": "SUCCESS", "mode": "dry-run"}
        else:
            # Simulate real execution
            handoff = {
                "status": "SUCCESS",
                "agent": agent_id,
                "output_schema": agent_info.get("output_schema"),
                "timestamp": time.time()
            }

        self.state_manager.add_artifact(f"{agent_id}_handoff", handoff)
        return handoff
