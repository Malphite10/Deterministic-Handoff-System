import argparse
import sys
from vibe.core.agent import MistralVibeAgent


def main():
    parser = argparse.ArgumentParser(description="Mistral Vibe - Main Assistant CLI")
    parser.add_argument(
        "command", choices=["run", "setup", "check"], help="Command to execute"
    )
    parser.add_argument("--prompt", help="Prompt for the 'run' command")
    parser.add_argument("--pkg", help="Package to check for 'check' command")

    args = parser.parse_args()

    agent = MistralVibeAgent()

    if args.command == "run":
        if not args.prompt:
            print("Error: --prompt is required for 'run' command.")
            sys.exit(1)
        print(agent.run_task(args.prompt))
    elif args.command == "check":
        if not args.pkg:
            print("Error: --pkg is required for 'check' command.")
            sys.exit(1)
        allowed = agent.validate_dependency(args.pkg)
        print(f"Package {args.pkg} allowed: {allowed}")
    elif args.command == "setup":
        from vibe.setup.install import setup

        setup()


if __name__ == "__main__":
    main()
