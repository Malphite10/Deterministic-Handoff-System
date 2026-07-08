import json
from pathlib import Path
from datetime import datetime, UTC
from jsonschema import validate, ValidationError


class AgentExecutor:
    def __init__(self, state_manager, dry_run: bool = False):
        self.state_manager = state_manager
        self.dry_run = dry_run
        self.schema_dir = Path("agents/schemas")
        self.approved_sources_path = Path("config/approved-sources.json")

    def _load_schema(self, schema_name: str) -> dict[str, any]:
        path = self.schema_dir / schema_name
        if not path.exists():
            if not schema_name.endswith(".json"):
                path = self.schema_dir / f"{schema_name}.json"
            if not path.exists():
                raise FileNotFoundError(f"Schema not found: {path}")
        return json.loads(path.read_text())

    def _validate_handoff(self, handoff: dict[str, any], schema_name: str):
        if not schema_name:
            return
        schema = self._load_schema(schema_name)
        validate(instance=handoff, schema=schema)

    def _check_blockers(self, handoff: dict[str, any]):
        if blockers := handoff.get("blockers", []):
            raise ValueError(f"Agent BLOCKED: {blockers}")

    def _validate_supply_chain(self, handoff: dict[str, any]):
        if handoff.get("agent") != "05-github-supply-chain":
            return

        if not self.approved_sources_path.exists():
            return

        approved = json.loads(self.approved_sources_path.read_text())
        npm_approved = approved.get("npm_packages", [])

        outputs = handoff.get("outputs", {})
        dependencies = outputs.get("recommended_versions", {})

        for name in dependencies.keys():
            if name not in npm_approved:
                raise ValueError(f"BLOCKED: {name} not in approved list")

    def execute(
        self, agent_id: str, input_data: dict[str, any], agent_info: dict[str, any]
    ) -> dict[str, any]:
        print(f"[{'DRY-RUN' if self.dry_run else 'EXEC'}] Agent: {agent_id}")
        self.state_manager.update_stage(agent_id)

        input_schema = agent_info.get("input_schema")
        if input_data and input_schema:
            try:
                self._validate_handoff(input_data, input_schema)
                print("  [VALID] Input schema check passed")
            except ValidationError as e:
                print(f"  [ERROR] Input validation failed: {e.message}")
                self.state_manager.add_error(f"Input validation failed for {agent_id}")
                return {
                    "status": "FAILED",
                    "reason": f"Input validation failed: {e.message}",
                }

        handoff = self._mock_execution(agent_id, input_data, agent_info)

        try:
            if output_schema := agent_info.get("output_schema"):
                self._validate_handoff(handoff, output_schema)
                print("  [VALID] Output schema check passed")

            self._check_blockers(handoff)

            if agent_id == "05-github-supply-chain":
                self._validate_supply_chain(handoff)
                print("  [VALID] Supply chain source validation passed")

            handoff["status"] = "SUCCESS"
        except (ValidationError, ValueError) as e:
            msg = getattr(e, "message", str(e))
            print(f"  [ERROR] Output validation/policy failed: {msg}")
            handoff["status"] = "FAILED"
            handoff["reason"] = msg
            self.state_manager.add_error(
                f"Output validation failed for {agent_id}: {msg}"
            )
            return handoff

        self.state_manager.add_artifact(f"{agent_id}_handoff", handoff)
        return handoff

    def _mock_execution(
        self, agent_id: str, input_data: dict[str, any], agent_info: dict[str, any]
    ) -> dict[str, any]:
        now = datetime.now(UTC).isoformat().replace("+00:00", "Z")
        next_list = agent_info.get("next")
        next_agent = next_list[0] if next_list and len(next_list) > 0 else None

        base = {
            "agent": agent_id,
            "version": "1.0.0",
            "timestamp": now,
            "inputs": {},
            "tasks": [f"Completed work for {agent_id}"],
            "outputs": {},
            "handoff": {"next_agent": next_agent},
            "blockers": [],
        }

        match agent_id:
            case "00-creative-director":
                base["inputs"] = {"strategy": "Market Expansion", "timeline": "Q1"}
                base["outputs"] = {
                    "brief": "A visionary project to expand market presence.",
                    "target_audience": "Tech-savvy entrepreneurs",
                    "success_criteria": ["100% security", "Zero downtime"],
                }
            case "01-research":
                base["inputs"] = {
                    "upstream_package": input_data if input_data else {},
                    "upstream_agent": "00-creative-director",
                }
                base["outputs"] = {
                    "market_insights": "High demand for AI agents.",
                    "competitor_analysis": [{"name": "CompA", "strength": "UX"}],
                    "template_recommendations": ["SaaS Starter"],
                }
            case "02-product":
                base["inputs"] = {
                    "opportunity_report": input_data if input_data else {},
                    "research_package": input_data if input_data else {},
                }
                base["outputs"] = {
                    "information_architecture": {"pages": ["Home", "Dashboard"]},
                    "user_flows": ["Login -> Dashboard"],
                    "feature_list": ["Agent Handoff", "Deterministic Workflows"],
                    "cms_schema": {"type": "object", "properties": {}},
                }
            case "03-design":
                base["inputs"] = {"product_spec": input_data if input_data else {}}
                base["outputs"] = {
                    "figma_url": "https://www.figma.com/file/123",
                    "design_tokens": {"colors": {"primary": "#000"}},
                    "component_inventory": ["Hero", "FeatureGrid"],
                    "responsive_breakpoints": {"mobile": 320, "desktop": 1280},
                }
            case "04-content":
                base["inputs"] = {"design_package": input_data if input_data else {}}
                base["outputs"] = {
                    "copy": {"hero": "Vibe with Mistral"},
                    "seo_keywords": ["AI", "Vibe"],
                }
            case "05-github-supply-chain":
                base["inputs"] = {
                    "design_package": input_data if input_data else {},
                    "dependencies_list": ["react", "next"],
                }
                base["outputs"] = {
                    "approved": True,
                    "security_score": 95,
                    "maintenance_score": 90,
                    "recommended_versions": {"react": "18.2.0", "next": "14.0.0"},
                    "integration_notes": ["Ensure pinned versions in lockfile"],
                }
            case "06-builder":
                base["inputs"] = {
                    "design_package": input_data if input_data else {},
                    "github_approval": input_data if input_data else {},
                }
                base["outputs"] = {
                    "source_code_url": "https://github.com/vibe/app",
                    "component_status": {"Hero": "Built"},
                    "build_artifacts": ["main.js", "style.css"],
                }
            case "07-integration":
                base["inputs"] = {"build_package": input_data if input_data else {}}
                base["outputs"] = {"integration_status": "COMPLETED"}
            case "08-qa":
                base["inputs"] = {
                    "integration_package": input_data if input_data else {}
                }
                base["outputs"] = {
                    "status": "approved",
                    "score": 98,
                    "passed_tests": ["UI", "Security", "Performance"],
                }
            case "09-email":
                base["inputs"] = {"qa_report": input_data if input_data else {}}
                base["outputs"] = {
                    "emails": [
                        {
                            "type": "launch",
                            "subject": "We are live!",
                            "body": "Check out VibeAI",
                        }
                    ]
                }
            case "10-launch":
                base["inputs"] = {
                    "qa_sign_off": input_data if input_data else {},
                    "email_campaign": input_data if input_data else {},
                }
                base["outputs"] = {
                    "live_url": "https://vibe.ai",
                    "seo_metadata": {"title": "VibeAI"},
                    "og_tags": {"image": "https://vibe.ai/og.png"},
                    "release_notes": "First release of VibeAI",
                }
                base["handoff"] = {"status": "COMPLETE"}
            case "11-memory":
                base["inputs"] = {"launch_package": input_data if input_data else {}}
                base["outputs"] = {
                    "new_patterns_stored": 5,
                    "knowledge_graph_updated": True,
                }
                base["handoff"] = {"status": "COMPLETE"}

        return base
