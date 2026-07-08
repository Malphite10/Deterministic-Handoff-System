import json
from pathlib import Path
from jsonschema import validate, ValidationError


class HandoffValidator:
    def __init__(
        self,
        schema_dir: str = "agents/schemas",
        approved_sources_path: str = "config/approved-sources.json",
    ):
        self.schema_dir = Path(schema_dir)
        self.approved_sources_path = Path(approved_sources_path)

    def load_schema(self, schema_name: str) -> dict[str, any]:
        if not schema_name.endswith(".json"):
            schema_name += ".json"
        path = self.schema_dir / schema_name
        if not path.exists():
            raise FileNotFoundError(f"Schema not found: {path}")
        return json.loads(path.read_text())

    def validate_package(self, package: dict[str, any], schema_name: str) -> bool:
        """Strictly validates a handoff package against its schema."""
        try:
            schema = self.load_schema(schema_name)
            validate(instance=package, schema=schema)

            if package.get("blockers"):
                print(
                    f"Validation FAILED: Package contains blockers: {package.get('blockers')}"
                )
                return False

            return True
        except ValidationError as e:
            print(f"Validation FAILED: {e.message}")
            return False
        except Exception as e:
            print(f"Validation ERROR: {str(e)}")
            return False

    def validate_supply_chain(self, package: dict[str, any]) -> bool:
        """Validates that all dependencies in a package are approved."""
        if package.get("agent") != "05-github-supply-chain":
            return True

        if not self.approved_sources_path.exists():
            print(
                "Warning: approved-sources.json not found. Skipping source validation."
            )
            return True

        approved = json.loads(self.approved_sources_path.read_text())
        npm_approved = approved.get("npm_packages", [])
        outputs = package.get("outputs", {})
        dependencies = outputs.get("recommended_versions", {})

        for name in dependencies.keys():
            if name not in npm_approved:
                print(f"Source validation FAILED: {name} not in approved list")
                return False

        return True


def validate_handoff_file(file_path: str, schema_name: str) -> bool:
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found: {file_path}")
        return False

    package = json.loads(path.read_text())
    validator = HandoffValidator()

    if not validator.validate_package(package, schema_name):
        return False

    if not validator.validate_supply_chain(package):
        return False

    print(f"Package {file_path} is VALID.")
    return True
