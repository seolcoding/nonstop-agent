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
DEFAULT_MODEL = "claude-opus-4-5-20251101"


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
        print("=" * 60)
        print("⚠️  CLAUDE_CODE_OAUTH_TOKEN 환경변수가 설정되지 않았습니다.")
        print("=" * 60)
        print()
        print("OAuth 토큰을 발급받으세요:")
        print()
        print("  1. 토큰 발급:")
        print("     $ claude setup-token")
        print()
        print("  2. 환경변수 설정:")
        print('     $ export CLAUDE_CODE_OAUTH_TOKEN="your-token-here"')
        print()
        print("  3. 영구 설정 (선택):")
        print('     $ echo \'export CLAUDE_CODE_OAUTH_TOKEN="your-token"\' >> ~/.zshrc')
        print()
        print("=" * 60)
        print()
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
