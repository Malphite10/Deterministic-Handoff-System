from runtime.state import StateManager
from runtime.registry import AgentRegistry
from runtime.graph import ExecutionGraph
from runtime.executor import AgentExecutor

class Orchestrator:
    def __init__(self):
        self.state_manager = StateManager()
        self.registry = AgentRegistry()
        self.graph = ExecutionGraph(self.registry)
        self.executor = AgentExecutor(self.state_manager)

    def run(self):
        print("Starting Orchestrator...")
        execution_order = self.graph.get_execution_order()

        current_input = {}
        for agent_id in execution_order:
            result = self.executor.execute(agent_id, current_input)
            if result.get("status") != "SUCCESS":
                print(f"Agent {agent_id} failed. Stopping execution.")
                self.state_manager.add_error(f"{agent_id} failed")
                break
            current_input = result

        print("Workflow completed.")

if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.run()
