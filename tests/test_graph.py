from runtime.graph import ExecutionGraph
from runtime.registry import AgentRegistry
import json

def test_execution_order(tmp_path):
    reg_file = tmp_path / "registry.json"
    data = {
        "A": {"next": ["B"]},
        "B": {"next": ["C"]},
        "C": {"next": None}
    }
    with open(reg_file, 'w') as f:
        json.dump(data, f)

    registry = AgentRegistry(registry_path=str(reg_file))
    graph = ExecutionGraph(registry)
    order = graph.get_execution_order("A")
    assert order == ["A", "B", "C"]
