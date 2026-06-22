import json
import os
from typing import Dict, Any, Optional

class AgentRegistry:
    def __init__(self, registry_path: str = "agents/registry.json"):
        self.registry_path = registry_path
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict[str, Any]:
        if os.path.exists(self.registry_path):
            with open(self.registry_path, 'r') as f:
                return json.load(f)
        return {}

    def get_agent_info(self, agent_id: str) -> Dict[str, Any]:
        return self.registry.get(agent_id, {})

    def get_next_agents(self, current_agent: str) -> Optional[list]:
        return self.get_agent_info(current_agent).get("next")
