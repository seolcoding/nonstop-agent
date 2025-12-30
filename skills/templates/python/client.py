"""
Claude Agent SDK Client Configuration
======================================

Functions for creating and configuring the Claude Agent SDK client.

Reference: https://platform.claude.com/docs/en/agent-sdk/python
"""

import os
from pathlib import Path

# NOTE: SDK was renamed from claude_code_sdk to claude_agent_sdk
# Reference: https://pypi.org/project/claude-agent-sdk/
from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, HookMatcher

from security import bash_security_hook


# MCP tools configuration (customize based on your needs)
MCP_TOOLS = [
    {{MCP_TOOLS}}
]

# Built-in tools - choose from:
# Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch, Task, NotebookEdit, TodoWrite
BUILTIN_TOOLS = [
    {{BUILTIN_TOOLS}}
]


def create_client(
    project_dir: Path,
    model: str,
    resume_session_id: str | None = None
) -> ClaudeSDKClient:
    """
    Create a Claude Agent SDK client with multi-layered security.

    Args:
        project_dir: Directory for the project
        model: Claude model to use
        resume_session_id: Optional session ID to resume previous session

    Returns:
        Configured ClaudeSDKClient

    Security layers (defense in depth):
    1. Sandbox - OS-level bash command isolation
    2. Permissions - File operations restricted to project_dir
    3. Security hooks - Bash commands validated against allowlist
    """
    # Claude Agent SDK uses bundled Claude Code CLI for authentication
    # The CLI checks CLAUDE_CODE_OAUTH_TOKEN environment variable
    # Reference: https://pypi.org/project/claude-agent-sdk/
    oauth_token = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN")

    if not oauth_token:
        print("Warning: CLAUDE_CODE_OAUTH_TOKEN not found in environment.")
        print("  The SDK will attempt to use existing Claude Code CLI authentication.")
        print("  If authentication fails, set: export CLAUDE_CODE_OAUTH_TOKEN='your-token'")
        print()
    else:
        print("Authentication: CLAUDE_CODE_OAUTH_TOKEN found")

    project_dir.mkdir(parents=True, exist_ok=True)

    print("Security configuration:")
    print("  - Sandbox: enabled (with autoAllowBash)")
    print(f"  - Working directory: {project_dir.resolve()}")
    print("  - Bash: allowlist validated via PreToolUse hook")
    print("  - Permission mode: acceptEdits")
    if resume_session_id:
        print(f"  - Resuming session: {resume_session_id}")
    print()

    # Build options
    # Reference: https://platform.claude.com/docs/en/agent-sdk/python
    options = ClaudeAgentOptions(
        model=model,
        system_prompt="{{SYSTEM_PROMPT}}",
        allowed_tools=[
            *BUILTIN_TOOLS,
            *MCP_TOOLS,
        ],
        mcp_servers={
            {{MCP_SERVERS}}
        },
        hooks={
            "PreToolUse": [
                HookMatcher(matcher="Bash", hooks=[bash_security_hook]),
            ],
        },
        max_turns=1000,
        cwd=str(project_dir.resolve()),

        # Load CLAUDE.md from project directory
        # Options: "user" (~/.claude), "project" (.claude/), "local" (.claude/local)
        # Must include "project" to load CLAUDE.md files
        setting_sources=["project"],

        # Session management - resume from previous session
        resume=resume_session_id,

        # Fork to new session ID when resuming (optional)
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
