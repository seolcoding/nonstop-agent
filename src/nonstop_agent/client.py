"""
Claude Agent SDK Client Configuration
======================================

Functions for creating and configuring the Claude Agent SDK client.

Reference: https://platform.claude.com/docs/en/agent-sdk/python
"""

import os
from pathlib import Path
from typing import Optional

from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, HookMatcher

from .security import bash_security_hook


# Default system prompt for autonomous coding
DEFAULT_SYSTEM_PROMPT = """You are an expert autonomous coding agent.
You work continuously across multiple sessions to complete complex projects.
You follow best practices and write production-quality code."""


def create_client(
    project_dir: Path,
    model: str,
    resume_session_id: Optional[str] = None,
    system_prompt: Optional[str] = None,
    allowed_tools: Optional[list[str]] = None,
    mcp_servers: Optional[dict] = None,
) -> ClaudeSDKClient:
    """
    Create a Claude Agent SDK client with multi-layered security.

    Args:
        project_dir: Directory for the project
        model: Claude model to use
        resume_session_id: Optional session ID to resume previous session
        system_prompt: Optional custom system prompt
        allowed_tools: Optional list of allowed tools
        mcp_servers: Optional MCP server configuration

    Returns:
        Configured ClaudeSDKClient

    Security layers (defense in depth):
    1. Sandbox - OS-level bash command isolation
    2. Permissions - File operations restricted to project_dir
    3. Security hooks - Bash commands validated against allowlist
    """
    project_dir.mkdir(parents=True, exist_ok=True)

    print("Security configuration:")
    print("  - Sandbox: enabled (with autoAllowBash)")
    print(f"  - Working directory: {project_dir.resolve()}")
    print("  - Bash: allowlist validated via PreToolUse hook")
    print("  - Permission mode: acceptEdits")
    if resume_session_id:
        print(f"  - Resuming session: {resume_session_id}")
    print()

    # Default tools if not specified
    if allowed_tools is None:
        allowed_tools = [
            "Read",
            "Write",
            "Edit",
            "Glob",
            "Grep",
            "Bash",
            "WebFetch",
            "WebSearch",
            "TodoWrite",
        ]

    # Build options
    options = ClaudeAgentOptions(
        model=model,
        system_prompt=system_prompt or DEFAULT_SYSTEM_PROMPT,
        allowed_tools=allowed_tools,
        mcp_servers=mcp_servers or {},
        hooks={
            "PreToolUse": [
                HookMatcher(matcher="Bash", hooks=[bash_security_hook]),
            ],
        },
        max_turns=1000,
        cwd=str(project_dir.resolve()),

        # Load CLAUDE.md from project directory
        setting_sources=["project"],

        # Session management
        resume=resume_session_id,
        fork_session=False,

        # Enable file checkpointing for rewind capability
        enable_file_checkpointing=True,

        # Permission mode: "default", "acceptEdits", "plan", "bypassPermissions"
        permission_mode="acceptEdits",

        # Sandbox configuration (macOS/Linux)
        sandbox={
            "enabled": True,
            "autoAllowBashIfSandboxed": True,
            "network": {
                "allowLocalBinding": True,  # Allow dev servers
            }
        },
    )

    return ClaudeSDKClient(options=options)
