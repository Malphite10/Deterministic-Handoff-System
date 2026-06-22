from typing import List, Dict, Any
from runtime.registry import AgentRegistry

class ExecutionGraph:
    def __init__(self, registry: AgentRegistry):
        self.registry = registry

    def get_execution_order(self, start_node: str = "00-creative-director") -> List[str]:
        order = []
        current = start_node
        while current:
            order.append(current)
            current = self.registry.get_next_agent(current)
        return order
