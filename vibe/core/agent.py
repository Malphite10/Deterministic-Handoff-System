import os
import json
from .firewall import Firewall

class MistralVibeAgent:
    def __init__(self, config_path="vibe.config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.name = self.config.get("agent_name", "Main Assistant")
        self.mode = self.config.get("mode", "cloud")
        self.firewall = Firewall(self.config.get("firewall", {}).get("policy_file", "config/network-policy.json"))

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return json.load(f)
        return {}

    def run_task(self, prompt):
        print(f"[{self.name}] Running in {self.mode} mode...")
        # Simulate check before action
        print(f"[{self.name}] Validating network access for task...")
        # Placeholder for actual LLM call and network interception
        return f"Task '{prompt}' processed by {self.name}."

    def validate_dependency(self, package_name):
        """Simulate dependency check."""
        print(f"[{self.name}] Checking dependency: {package_name}")
        # In a real implementation, this would check against approved-sources.json
        return True
