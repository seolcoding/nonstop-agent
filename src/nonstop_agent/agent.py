"""
Agent Session Logic
===================

Core agent interaction functions for running autonomous coding sessions.

Reference:
- https://platform.claude.com/docs/en/agent-sdk/python
- https://platform.claude.com/docs/en/agent-sdk/sessions
"""

import asyncio
import json
from pathlib import Path
from typing import Optional

from claude_agent_sdk import (
    query,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    ToolResultBlock,
    ResultMessage,
)

from .client import create_options
from .progress import print_session_header, print_progress_summary, save_session_id
from .prompts import (
    get_initializer_prompt,
    get_coding_prompt,
    get_existing_project_prompt,
    copy_spec_to_project,
)


# Configuration
AUTO_CONTINUE_DELAY_SECONDS = 3
SESSION_FILE = "claude_session.json"


def load_last_session_id(project_dir: Path) -> Optional[str]:
    """Load the last session ID for resumption."""
    session_file = project_dir / SESSION_FILE
    if session_file.exists():
        try:
            with open(session_file) as f:
                data = json.load(f)
                return data.get("session_id")
        except (json.JSONDecodeError, IOError):
            pass
    return None


async def run_agent_session(
    prompt: str,
    project_dir: Path,
    model: str,
    resume_session_id: Optional[str] = None,
    system_prompt: Optional[str] = None,
) -> tuple[str, str, Optional[str]]:
    """
    Run a single agent session using Claude Agent SDK.

    Args:
        prompt: The prompt to send
        project_dir: Project directory path
        model: Claude model to use
        resume_session_id: Optional session ID to resume
        system_prompt: Optional custom system prompt

    Returns:
        (status, response_text, session_id) where status is:
        - "continue" if agent should continue working
        - "error" if an error occurred
    """
    print("Sending prompt to Claude Agent SDK...\n")

    options = create_options(
        project_dir=project_dir,
        model=model,
        resume_session_id=resume_session_id,
        system_prompt=system_prompt,
    )

    session_id = None
    response_text = ""

    try:
        async for msg in query(prompt=prompt, options=options):
            # Handle AssistantMessage (text and tool use)
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        response_text += block.text
                        print(block.text, end="", flush=True)
                    elif isinstance(block, ToolUseBlock):
                        print(f"\n[Tool: {block.name}]", flush=True)
                        if hasattr(block, "input"):
                            input_str = str(block.input)
                            if len(input_str) > 200:
                                print(f"   Input: {input_str[:200]}...", flush=True)
                            else:
                                print(f"   Input: {input_str}", flush=True)

            # Handle tool results
            elif hasattr(msg, 'content') and isinstance(msg.content, list):
                for block in msg.content:
                    if isinstance(block, ToolResultBlock):
                        is_error = getattr(block, "is_error", False)
                        result_content = getattr(block, "content", "")

                        if "blocked" in str(result_content).lower():
                            print(f"   [BLOCKED] {result_content}", flush=True)
                        elif is_error:
                            error_str = str(result_content)[:500]
                            print(f"   [Error] {error_str}", flush=True)
                        else:
                            print("   [Done]", flush=True)

            # Handle result message (final message with session info)
            if isinstance(msg, ResultMessage):
                if hasattr(msg, 'session_id'):
                    session_id = msg.session_id
                if hasattr(msg, 'total_cost_usd'):
                    print(f"\nSession cost: ${msg.total_cost_usd:.4f}")

        print("\n" + "-" * 70 + "\n")

        # Save session ID for future resumption
        if session_id:
            save_session_id(project_dir, session_id)

        return "continue", response_text, session_id

    except Exception as e:
        print(f"Error during agent session: {e}")
        return "error", str(e), session_id


async def run_autonomous_agent(
    project_dir: Path,
    model: str,
    max_iterations: Optional[int] = None,
    analyze_first: bool = False,
    resume: bool = False,
    system_prompt: Optional[str] = None,
) -> None:
    """
    Run the autonomous agent loop.

    Args:
        project_dir: Directory for the project
        model: Claude model to use
        max_iterations: Maximum number of iterations (None for unlimited)
        analyze_first: Whether to analyze existing project first
        resume: Whether to resume from last session
        system_prompt: Optional custom system prompt
    """
    print("\n" + "=" * 70)
    print("  NONSTOP AGENT")
    print("=" * 70)
    print(f"\nProject directory: {project_dir}")
    print(f"Model: {model}")
    if max_iterations:
        print(f"Max iterations: {max_iterations}")
    else:
        print("Max iterations: Unlimited")
    if analyze_first:
        print("Mode: Analyze existing project first")
    if resume:
        print("Mode: Resume from last session")
    print()

    project_dir.mkdir(parents=True, exist_ok=True)

    # Check for session resumption
    resume_session_id = None
    if resume:
        resume_session_id = load_last_session_id(project_dir)
        if resume_session_id:
            print(f"Resuming session: {resume_session_id}")
        else:
            print("No previous session found, starting fresh")

    # Determine session type
    tests_file = project_dir / "feature_list.json"
    is_first_run = not tests_file.exists() and not resume_session_id
    needs_analysis = analyze_first and is_first_run

    if needs_analysis:
        print("=" * 70)
        print("  EXISTING PROJECT ANALYSIS MODE")
        print("  Will analyze, run tests, then create feature_list.json")
        print("=" * 70)
        print()
    elif is_first_run:
        print("Fresh start - will use initializer agent")
        print()
        print("=" * 70)
        print("  NOTE: First session may take 10-20+ minutes!")
        print("  The agent is generating detailed test cases.")
        print("=" * 70)
        print()
        copy_spec_to_project(project_dir)
    else:
        print("Continuing existing project")
        print_progress_summary(project_dir)

    # Main loop
    iteration = 0
    current_session_id = resume_session_id

    while True:
        iteration += 1

        if max_iterations and iteration > max_iterations:
            print(f"\nReached max iterations ({max_iterations})")
            break

        # Determine prompt type
        if needs_analysis:
            prompt_type = "analysis"
            needs_analysis = False
        elif is_first_run:
            prompt_type = "initializer"
            is_first_run = False
        else:
            prompt_type = "coding"

        print_session_header(iteration, prompt_type)

        # Choose prompt
        if prompt_type == "analysis":
            prompt = get_existing_project_prompt()
        elif prompt_type == "initializer":
            prompt = get_initializer_prompt()
        else:
            prompt = get_coding_prompt()

        # Run the session
        status, response, session_id = await run_agent_session(
            prompt=prompt,
            project_dir=project_dir,
            model=model,
            resume_session_id=current_session_id if iteration == 1 else None,
            system_prompt=system_prompt,
        )

        if session_id:
            current_session_id = session_id

        if status == "continue":
            print(f"\nAgent will auto-continue in {AUTO_CONTINUE_DELAY_SECONDS}s...")
            print_progress_summary(project_dir)
            await asyncio.sleep(AUTO_CONTINUE_DELAY_SECONDS)
        elif status == "error":
            print("\nSession encountered an error, retrying...")
            await asyncio.sleep(AUTO_CONTINUE_DELAY_SECONDS)

        if max_iterations is None or iteration < max_iterations:
            print("\nPreparing next session...\n")
            await asyncio.sleep(1)

    # Final summary
    print("\n" + "=" * 70)
    print("  SESSION COMPLETE")
    print("=" * 70)
    print(f"\nLast session ID: {current_session_id}")
    print("To resume later: --resume")
    print_progress_summary(project_dir)
    print("\nDone!")
