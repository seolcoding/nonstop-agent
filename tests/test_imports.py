"""
Import Tests
============

Verify that all module imports work correctly.
These tests catch API changes in dependencies early.
"""

import pytest


class TestImports:
    """Test that all modules import without errors."""

    def test_import_main_package(self):
        """Test main package imports."""
        from nonstop_agent import run_autonomous_agent, create_options, bash_security_hook
        assert callable(run_autonomous_agent)
        assert callable(create_options)
        assert callable(bash_security_hook)

    def test_import_agent_module(self):
        """Test agent module imports."""
        from nonstop_agent.agent import run_autonomous_agent, run_agent_session
        assert callable(run_autonomous_agent)
        assert callable(run_agent_session)

    def test_import_client_module(self):
        """Test client module imports."""
        from nonstop_agent.client import create_options, DEFAULT_SYSTEM_PROMPT
        assert callable(create_options)
        assert isinstance(DEFAULT_SYSTEM_PROMPT, str)

    def test_import_security_module(self):
        """Test security module imports."""
        from nonstop_agent.security import (
            bash_security_hook,
            is_command_allowed,
            ALLOWED_COMMANDS,
        )
        assert callable(bash_security_hook)
        assert callable(is_command_allowed)
        assert isinstance(ALLOWED_COMMANDS, set)

    def test_import_progress_module(self):
        """Test progress module imports."""
        from nonstop_agent.progress import (
            print_session_header,
            print_progress_summary,
            save_session_id,
        )
        assert callable(print_session_header)
        assert callable(print_progress_summary)
        assert callable(save_session_id)

    def test_import_prompts_module(self):
        """Test prompts module imports."""
        from nonstop_agent.prompts import (
            get_initializer_prompt,
            get_coding_prompt,
            get_existing_project_prompt,
        )
        assert callable(get_initializer_prompt)
        assert callable(get_coding_prompt)
        assert callable(get_existing_project_prompt)


class TestSDKImports:
    """Test Claude Agent SDK imports."""

    def test_import_claude_agent_sdk(self):
        """Test that claude_agent_sdk is importable."""
        try:
            from claude_agent_sdk import query, ClaudeAgentOptions
            assert callable(query)
            assert ClaudeAgentOptions is not None
        except ImportError as e:
            pytest.skip(f"claude-agent-sdk not installed: {e}")

    def test_import_sdk_types(self):
        """Test SDK type imports."""
        try:
            from claude_agent_sdk import (
                AssistantMessage,
                TextBlock,
                ToolUseBlock,
                ResultMessage,
            )
            assert AssistantMessage is not None
            assert TextBlock is not None
            assert ToolUseBlock is not None
            assert ResultMessage is not None
        except ImportError as e:
            pytest.skip(f"claude-agent-sdk not installed: {e}")

    def test_import_hook_matcher(self):
        """Test HookMatcher import."""
        try:
            from claude_agent_sdk import HookMatcher
            assert HookMatcher is not None
        except ImportError as e:
            pytest.skip(f"claude-agent-sdk not installed: {e}")


class TestSecurityAllowlist:
    """Test security allowlist functionality."""

    def test_basic_commands_allowed(self):
        """Test that basic safe commands are allowed."""
        from nonstop_agent.security import is_command_allowed

        safe_commands = ["ls", "cat", "echo", "pwd", "git status"]
        for cmd in safe_commands:
            assert is_command_allowed(cmd), f"Command should be allowed: {cmd}"

    def test_dangerous_commands_blocked(self):
        """Test that dangerous commands are blocked."""
        from nonstop_agent.security import is_command_allowed

        dangerous_commands = ["rm -rf /", "sudo rm", ":(){ :|:& };:"]
        for cmd in dangerous_commands:
            assert not is_command_allowed(cmd), f"Command should be blocked: {cmd}"

    def test_python_uv_allowed(self):
        """Test that Python/uv commands are allowed."""
        from nonstop_agent.security import is_command_allowed

        python_commands = ["uv run pytest", "uv add requests", "python --version"]
        for cmd in python_commands:
            assert is_command_allowed(cmd), f"Command should be allowed: {cmd}"
