#!/usr/bin/env python3
"""
Basic Usage Example
===================

Demonstrates how to use Nonstop Agent programmatically.
"""

import asyncio
from pathlib import Path

from nonstop_agent import run_autonomous_agent


async def main():
    """Run the autonomous agent on a new project."""

    # Define project directory
    project_dir = Path("./my_project")

    # Run the agent
    await run_autonomous_agent(
        project_dir=project_dir,
        model="claude-sonnet-4-5-20250929",
        max_iterations=5,  # Limit iterations for demo
        analyze_first=False,  # New project
        resume=False,
    )


if __name__ == "__main__":
    asyncio.run(main())
