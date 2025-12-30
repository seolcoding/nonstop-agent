"""
Security Hooks for Nonstop Agent
=================================

Pre-tool-use hooks that validate bash commands for security.
Uses an allowlist approach - only explicitly permitted commands can run.

Reference: https://platform.claude.com/docs/en/agent-sdk/hooks
"""

from __future__ import annotations

import os
import re
import shlex
from typing import Any

# Type aliases for hook functions (from claude_agent_sdk)
HookInput = dict[str, Any]
HookContext = Any
HookJSONOutput = dict[str, Any]


# Allowed commands - customize based on your needs
ALLOWED_COMMANDS = {
    # File inspection
    "ls",
    "cat",
    "head",
    "tail",
    "wc",
    "grep",
    "find",
    "echo",
    # File operations
    "cp",
    "mkdir",
    "chmod",  # Validated separately
    # Directory
    "pwd",
    # Node.js
    "npm",
    "npx",
    "node",
    "yarn",
    "pnpm",
    # Python
    "python",
    "python3",
    "pip",
    "uv",
    "pytest",
    # Version control
    "git",
    # Process management
    "ps",
    "lsof",
    "sleep",
    "pkill",  # Validated separately
    # Script execution
    "init.sh",
}

COMMANDS_NEEDING_EXTRA_VALIDATION = {"pkill", "chmod", "init.sh"}


def add_allowed_command(command: str) -> None:
    """Add a command to the allowlist."""
    ALLOWED_COMMANDS.add(command)


def remove_allowed_command(command: str) -> None:
    """Remove a command from the allowlist."""
    ALLOWED_COMMANDS.discard(command)


def is_command_allowed(command_string: str) -> bool:
    """
    Check if a command string is allowed by the security policy.

    Args:
        command_string: The full command string to check

    Returns:
        True if all commands in the string are allowed, False otherwise
    """
    commands = extract_commands(command_string)

    if not commands:
        return False

    for cmd in commands:
        if cmd not in ALLOWED_COMMANDS:
            return False

    return True


def split_command_segments(command_string: str) -> list[str]:
    """Split a compound command into individual command segments."""
    segments = re.split(r"\s*(?:&&|\|\|)\s*", command_string)

    result = []
    for segment in segments:
        sub_segments = re.split(r'(?<!["\'])\s*;\s*(?!["\'])', segment)
        for sub in sub_segments:
            sub = sub.strip()
            if sub:
                result.append(sub)

    return result


def extract_commands(command_string: str) -> list[str]:
    """Extract command names from a shell command string."""
    commands = []

    segments = re.split(r'(?<!["\'])\s*;\s*(?!["\'])', command_string)

    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue

        try:
            tokens = shlex.split(segment)
        except ValueError:
            return []

        if not tokens:
            continue

        expect_command = True

        for token in tokens:
            if token in ("|", "||", "&&", "&"):
                expect_command = True
                continue

            if token in (
                "if", "then", "else", "elif", "fi", "for", "while",
                "until", "do", "done", "case", "esac", "in", "!", "{", "}",
            ):
                continue

            if token.startswith("-"):
                continue

            if "=" in token and not token.startswith("="):
                continue

            if expect_command:
                cmd = os.path.basename(token)
                commands.append(cmd)
                expect_command = False

    return commands


def validate_pkill_command(command_string: str) -> tuple[bool, str]:
    """Validate pkill commands - only allow killing dev-related processes."""
    allowed_process_names = {"node", "npm", "npx", "vite", "next", "python", "uvicorn"}

    try:
        tokens = shlex.split(command_string)
    except ValueError:
        return False, "Could not parse pkill command"

    if not tokens:
        return False, "Empty pkill command"

    args = [t for t in tokens[1:] if not t.startswith("-")]

    if not args:
        return False, "pkill requires a process name"

    target = args[-1]
    if " " in target:
        target = target.split()[0]

    if target in allowed_process_names:
        return True, ""
    return False, f"pkill only allowed for dev processes: {allowed_process_names}"


def validate_chmod_command(command_string: str) -> tuple[bool, str]:
    """Validate chmod commands - only allow making files executable."""
    try:
        tokens = shlex.split(command_string)
    except ValueError:
        return False, "Could not parse chmod command"

    if not tokens or tokens[0] != "chmod":
        return False, "Not a chmod command"

    mode = None
    files = []

    for token in tokens[1:]:
        if token.startswith("-"):
            return False, "chmod flags are not allowed"
        elif mode is None:
            mode = token
        else:
            files.append(token)

    if mode is None:
        return False, "chmod requires a mode"

    if not files:
        return False, "chmod requires at least one file"

    if not re.match(r"^[ugoa]*\+x$", mode):
        return False, f"chmod only allowed with +x mode, got: {mode}"

    return True, ""


def validate_init_script(command_string: str) -> tuple[bool, str]:
    """Validate init.sh script execution."""
    try:
        tokens = shlex.split(command_string)
    except ValueError:
        return False, "Could not parse init script command"

    if not tokens:
        return False, "Empty command"

    script = tokens[0]

    if script == "./init.sh" or script.endswith("/init.sh"):
        return True, ""

    return False, f"Only ./init.sh is allowed, got: {script}"


def get_command_for_validation(cmd: str, segments: list[str]) -> str:
    """Find the specific command segment that contains the given command."""
    for segment in segments:
        segment_commands = extract_commands(segment)
        if cmd in segment_commands:
            return segment
    return ""


def _deny(reason: str) -> HookJSONOutput:
    """Helper to create a deny response in the correct format."""
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


async def bash_security_hook(
    input_data: HookInput,
    tool_use_id: str | None,
    context: HookContext,
) -> HookJSONOutput:
    """
    Pre-tool-use hook that validates bash commands using an allowlist.

    Reference: https://platform.claude.com/docs/en/agent-sdk/hooks

    Args:
        input_data: Dict with tool_name and tool_input
        tool_use_id: Unique identifier for this tool use
        context: Hook context with additional information

    Returns:
        Empty dict to allow, or hookSpecificOutput with permissionDecision="deny" to block
    """
    if input_data.get("tool_name") != "Bash":
        return {}

    command = input_data.get("tool_input", {}).get("command", "")
    if not command:
        return {}

    commands = extract_commands(command)

    if not commands:
        return _deny(f"Could not parse command: {command}")

    segments = split_command_segments(command)

    for cmd in commands:
        if cmd not in ALLOWED_COMMANDS:
            return _deny(f"Command '{cmd}' is not in the allowed list")

        if cmd in COMMANDS_NEEDING_EXTRA_VALIDATION:
            cmd_segment = get_command_for_validation(cmd, segments)
            if not cmd_segment:
                cmd_segment = command

            if cmd == "pkill":
                allowed, reason = validate_pkill_command(cmd_segment)
                if not allowed:
                    return _deny(reason)
            elif cmd == "chmod":
                allowed, reason = validate_chmod_command(cmd_segment)
                if not allowed:
                    return _deny(reason)
            elif cmd == "init.sh":
                allowed, reason = validate_init_script(cmd_segment)
                if not allowed:
                    return _deny(reason)

    return {}
