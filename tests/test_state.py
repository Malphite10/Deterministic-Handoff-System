import pytest
import os
import json
from runtime.state import StateManager

def test_state_initialization(tmp_path):
    state_file = tmp_path / "state.json"
    manager = StateManager(state_path=str(state_file))
    assert manager.state["status"] == "INITIALIZED"
    assert manager.state["project_id"] == "default"

def test_state_transition(tmp_path):
    state_file = tmp_path / "state.json"
    manager = StateManager(state_path=str(state_file))
    manager.transition_to("00-creative-director", next_agent="01-research")
    assert manager.state["current_agent"] == "00-creative-director"
    assert manager.state["next_agent"] == "01-research"
    assert len(manager.state["history"]) == 1
    assert manager.state["history"][0]["to"] == "00-creative-director"

def test_add_artifact(tmp_path):
    state_file = tmp_path / "state.json"
    manager = StateManager(state_path=str(state_file))
    manager.add_artifact("test_art", {"key": "value"})
    assert manager.state["artifacts"]["test_art"] == {"key": "value"}
