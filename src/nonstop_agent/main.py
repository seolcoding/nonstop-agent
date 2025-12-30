#!/usr/bin/env python3
"""
Nonstop Agent - Main Entry Point
=================================

Long-running autonomous agent that works continuously across sessions.

Usage:
    # New project
    uv run nonstop-agent --project-dir ./my_project

    # Existing project (analyze first)
    uv run nonstop-agent --project-dir ./existing --analyze-first

    # Resume last session
    uv run nonstop-agent --project-dir ./my_project --resume

    # Limit iterations
    uv run nonstop-agent --project-dir ./my_project --max-iterations 5

Reference:
- https://platform.claude.com/docs/en/agent-sdk/overview
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
"""

import argparse
import asyncio
import os
from pathlib import Path

from .agent import run_autonomous_agent


# Configuration
DEFAULT_MODEL = "claude-sonnet-4-5-20250929"


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Nonstop Agent - Long-running autonomous coding agent",
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

    parser.add_argument(
        "--system-prompt",
        type=str,
        default=None,
        help="Custom system prompt for the agent",
    )

    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_args()

    # Check for authentication
    oauth_token = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN")
    if not oauth_token:
        print("Note: CLAUDE_CODE_OAUTH_TOKEN not set.")
        print("  The SDK will use existing Claude Code CLI authentication.")
        print("  If authentication fails, run: claude login")
        print()

    # Run the agent
    try:
        asyncio.run(
            run_autonomous_agent(
                project_dir=args.project_dir,
                model=args.model,
                max_iterations=args.max_iterations,
                analyze_first=args.analyze_first,
                resume=args.resume,
                system_prompt=args.system_prompt,
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
