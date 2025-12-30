#!/usr/bin/env python3
"""
Existing Project Example
========================

Demonstrates how to use Nonstop Agent with an existing codebase.
"""

import asyncio
from pathlib import Path

from nonstop_agent import run_autonomous_agent


async def main():
    """Analyze and continue work on an existing project."""

    # Point to existing project
    project_dir = Path("/path/to/existing/project")

    # Run with analyze-first mode
    await run_autonomous_agent(
        project_dir=project_dir,
        model="claude-sonnet-4-5-20250929",
        max_iterations=10,
        analyze_first=True,  # Analyze existing codebase first
        resume=False,
    )


async def resume_session():
    """Resume from a previous session."""

    project_dir = Path("/path/to/existing/project")

    await run_autonomous_agent(
        project_dir=project_dir,
        model="claude-sonnet-4-5-20250929",
        max_iterations=10,
        analyze_first=False,
        resume=True,  # Resume from last session
    )


if __name__ == "__main__":
    # First run: analyze the project
    asyncio.run(main())

    # Later: resume where we left off
    # asyncio.run(resume_session())
