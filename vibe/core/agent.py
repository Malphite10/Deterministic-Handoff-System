import json
from pathlib import Path
from vibe.core.firewall import Firewall


class MistralVibeAgent:
    def __init__(self, config_path: str = "vibe.config.json"):
        self.config_path = Path(config_path)
        self.config = self.load_config()
        self.name = self.config.get("agent_name", "Main Assistant")
        self.mode = self.config.get("mode", "cloud")
        policy_file = self.config.get("firewall", {}).get(
            "policy_file", "config/network-policy.json"
        )
        self.firewall = Firewall(policy_file)

    def load_config(self) -> dict[str, any]:
        if self.config_path.exists():
            return json.loads(self.config_path.read_text())
        return {}

    def run_task(self, prompt: str) -> str:
        print(f"[{self.name}] Running in {self.mode} mode...")
        print(f"[{self.name}] Validating network access for task...")
        return f"Task '{prompt}' processed by {self.name}."

    def validate_dependency(self, package_name: str) -> bool:
        """Simulate dependency check."""
        print(f"[{self.name}] Checking dependency: {package_name}")
        return True
