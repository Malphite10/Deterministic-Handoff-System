import json
import os
from typing import Dict, List, Any

class StateManager:
    def __init__(self, state_path: str = "artifacts/current/state.json"):
        self.state_path = state_path
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if os.path.exists(self.state_path):
            with open(self.state_path, 'r') as f:
                return json.load(f)
        return {
            "project_id": "",
            "current_stage": "idle",
            "completed_stages": [],
            "artifacts": {},
            "errors": [],
            "scores": {}
        }

    def save_state(self):
        os.makedirs(os.path.dirname(self.state_path), exist_ok=True)
        with open(self.state_path, 'w') as f:
            json.dump(self.state, f, indent=2)

    def update_stage(self, stage: str):
        self.state["current_stage"] = stage
        if stage not in self.state["completed_stages"] and stage != "idle":
            self.state["completed_stages"].append(stage)
        self.save_state()

    def add_artifact(self, name: str, data: Any):
        self.state["artifacts"][name] = data
        self.save_state()

    def add_error(self, error: str):
        self.state["errors"].append(error)
        self.save_state()

    def update_score(self, key: str, value: float):
        self.state["scores"][key] = value
        self.save_state()
