#!/usr/bin/env python3
"""
Autonomous Agent - Main Entry Point
====================================

{{AGENT_DESCRIPTION}}

Usage:
    # New project
    uv run python main.py --project-dir ./my_project

    # Existing project (analyze first)
    uv run python main.py --project-dir ./existing --analyze-first

    # Resume last session
    uv run python main.py --project-dir ./my_project --resume

    # Limit iterations
    uv run python main.py --project-dir ./my_project --max-iterations 5

Reference:
- https://platform.claude.com/docs/en/agent-sdk/overview
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
"""

import argparse
import asyncio
import os
from pathlib import Path

from agent import run_autonomous_agent


# Configuration
DEFAULT_MODEL = "{{MODEL}}"  # claude-opus-4-5-20251101


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="{{AGENT_DESCRIPTION}}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path("./project"),
        help="Directory for the project (default: ./project)",
    )

    parser.add_argument(
        "--max-iterations",
        type=int,
        default=None,
        help="Maximum number of agent iterations (default: unlimited)",
    )

    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Claude model to use (default: {DEFAULT_MODEL})",
    )

    parser.add_argument(
        "--analyze-first",
        action="store_true",
        help="Analyze existing project before starting (for existing codebases)",
    )

    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from the last session (uses saved session ID)",
    )

    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_args()

    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("\nGet your API key from: https://console.anthropic.com/")
        print("\nThen set it:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        return

    # Run the agent
    try:
        asyncio.run(
            run_autonomous_agent(
                project_dir=args.project_dir,
                model=args.model,
                max_iterations=args.max_iterations,
                analyze_first=args.analyze_first,
                resume=args.resume,
            )
        )
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        print("To resume, run with --resume flag")
    except Exception as e:
        print(f"\nFatal error: {e}")
        raise


if __name__ == "__main__":
    main()
