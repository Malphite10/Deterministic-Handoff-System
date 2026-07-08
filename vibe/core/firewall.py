import fnmatch
import json
import os


class Firewall:
    def __init__(self, policy_path="config/network-policy.json"):
        self.policy_path = policy_path
        self.allowlist = set()
        self.denylist = set()
        self.patterns = []
        self.load_policy()

    def load_policy(self):
        if not os.path.exists(self.policy_path):
            return

        with open(self.policy_path, "r") as f:
            policy = json.load(f)
            self.allowlist.update(policy.get("default_allowlist", []))
            self.allowlist.update(policy.get("custom_allowlist", []))
            self.denylist.update(policy.get("denylist", []))

            # Pattern matching with wildcards
            if policy.get("pattern_matching", {}).get("wildcards_supported", False):
                # In a real system, we'd store these patterns for fnmatch
                self.patterns = [p for p in self.allowlist if "*" in p]

    def is_allowed(self, domain):
        # Denylist takes precedence
        if domain in self.denylist:
            return False

        # Exact match in allowlist
        if domain in self.allowlist:
            return True

        # Pattern match (wildcards)
        for pattern in self.patterns:
            if fnmatch.fnmatch(domain, pattern):
                return True

        return False


class MCPIsolation:
    """Each MCP server has its own network allowlist."""

    def __init__(self, mcp_config_path="mcp-server/mcp.json"):
        self.mcp_config_path = mcp_config_path
        self.servers = {}
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.mcp_config_path):
            return
        with open(self.mcp_config_path, "r") as f:
            data = json.load(f)
            self.servers = data.get("servers", {})

    def is_allowed(self, server_name, domain):
        server = self.servers.get(server_name)
        if not server:
            return False
        return domain in server.get("allowlist", [])
