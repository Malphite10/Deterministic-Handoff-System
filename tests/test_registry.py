from runtime.registry import AgentRegistry
import json
import os

def test_registry_load(tmp_path):
    reg_file = tmp_path / "registry.json"
    data = {"agent1": {"next": ["agent2"]}}
    with open(reg_file, 'w') as f:
        json.dump(data, f)

    registry = AgentRegistry(registry_path=str(reg_file))
    assert registry.get_next_agents("agent1") == ["agent2"]

def test_get_agent_info():
    registry = AgentRegistry()
    info = registry.get_agent_info("00-creative-director")
    assert info["id"] == "00-creative-director"
